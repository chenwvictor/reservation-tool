from __future__ import annotations

from datetime import date, datetime

import typer
from rich.console import Console
from rich.table import Table
from sqlmodel import select

from .booking import execute_booking
from .db import get_session, init_db
from .discovery import refresh_discovery
from .inference import infer_rules
from .models import BookingRequest, DropRule, Job, JobStatus, Restaurant
from .planner import compute_drop_datetime

app = typer.Typer(help="Reservation Drop Tracker + Assisted Booker")
console = Console()


@app.callback()
def _main() -> None:
    init_db()


@app.command()
def refresh() -> None:
    with get_session() as session:
        created = refresh_discovery(session)
    console.print(f"Discovery refreshed. Added {created} new restaurants.")


@app.command()
def infer() -> None:
    with get_session() as session:
        updated = infer_rules(session)
    console.print(f"Inferred drop rules for {updated} restaurants.")


@app.command()
def browse(city: str = typer.Option("NYC", help="NYC or PHL")) -> None:
    with get_session() as session:
        rows = session.exec(select(Restaurant).where(Restaurant.city == city)).all()
        table = Table(title=f"Restaurants - {city}")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Provider")
        table.add_column("Rule")
        table.add_column("Confidence")
        for r in rows:
            rule = session.get(DropRule, r.id)
            rule_text = f"{rule.lead_time_days}d @ {rule.open_time_local}" if rule else "-"
            conf = f"{rule.confidence:.2f}" if rule else "-"
            table.add_row(str(r.id), r.name, r.provider.value, rule_text, conf)
        console.print(table)


@app.command()
def plan(
    restaurant: int = typer.Option(..., "--restaurant"),
    party: int = typer.Option(..., "--party"),
    date_target: date = typer.Option(..., "--date"),
    time_window: str = typer.Option(..., "--time-window", help="HH:MM-HH:MM"),
    mode: str = typer.Option("deeplink"),
    dry_run: bool = typer.Option(True),
) -> None:
    start, end = time_window.split("-")
    with get_session() as session:
        req = BookingRequest(
            restaurant_id=restaurant,
            party_size=party,
            date_target=date_target,
            time_window_start=start,
            time_window_end=end,
            mode=mode,
            dry_run=dry_run,
        )
        session.add(req)
        session.commit()
        session.refresh(req)

        rule = session.get(DropRule, restaurant)
        run_at = compute_drop_datetime(rule, date_target) if rule else datetime.now()
        job = Job(booking_request_id=req.id, run_at=run_at)
        session.add(job)
        session.commit()
        console.print(f"Planned booking request {req.id}. Job {job.id} scheduled for {run_at}.")


@app.command()
def book(
    booking_request_id: int = typer.Option(..., "--request-id"),
    assist: bool = typer.Option(False, "--assist"),
) -> None:
    with get_session() as session:
        req = session.get(BookingRequest, booking_request_id)
        if not req:
            raise typer.BadParameter("Booking request not found")
        restaurant = session.get(Restaurant, req.restaurant_id)
        execute_booking(restaurant, req, assist=assist)


@app.command()
def jobs() -> None:
    with get_session() as session:
        rows = session.exec(select(Job).order_by(Job.run_at.desc())).all()
        table = Table(title="Jobs")
        table.add_column("ID")
        table.add_column("Request")
        table.add_column("Run At")
        table.add_column("Status")
        for row in rows:
            table.add_row(str(row.id), str(row.booking_request_id), str(row.run_at), row.status.value)
        console.print(table)


@app.command()
def edit(restaurant_id: int) -> None:
    with get_session() as session:
        rule = session.get(DropRule, restaurant_id) or DropRule(restaurant_id=restaurant_id)
        lead = typer.prompt("lead_time_days", default=str(rule.lead_time_days or ""))
        open_time = typer.prompt("open_time_local", default=rule.open_time_local or "09:00")
        tz = typer.prompt("timezone", default=rule.timezone)
        rule.lead_time_days = int(lead) if lead else None
        rule.open_time_local = open_time
        rule.timezone = tz
        rule.updated_at = datetime.utcnow()
        session.add(rule)
        session.commit()
        console.print("Drop rule updated.")


@app.command()
def export(path: str = typer.Option("export.csv")) -> None:
    with get_session() as session:
        rows = session.exec(select(Restaurant)).all()
    with open(path, "w", encoding="utf-8") as f:
        f.write("id,name,city,provider\n")
        for r in rows:
            f.write(f"{r.id},{r.name},{r.city.value},{r.provider.value}\n")
    console.print(f"Exported {len(rows)} restaurants to {path}")


if __name__ == "__main__":
    app()
