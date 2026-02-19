from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from sqlmodel import select

from resy_sniper.booking import execute_booking
from resy_sniper.db import get_session, init_db
from resy_sniper.discovery import run_discovery
from resy_sniper.ingest_seeds import ingest_builtins, ingest_csv
from resy_sniper.inference import infer_rules
from resy_sniper.models import BookingRequest, DropRule, Job, Restaurant
from resy_sniper.planner import compute_drop_datetime

app = typer.Typer(help="Reservation Drop Tracker + Assisted Booker")


@app.callback()
def _init() -> None:
    init_db()


@app.command("ingest-csv")
def ingest_csv_cmd(path: str) -> None:
    with get_session() as session:
        inserted = ingest_csv(session, path)
    typer.echo(f"Ingested {inserted} rows from {path}")


@app.command("ingest-seeds")
def ingest_seeds_cmd() -> None:
    with get_session() as session:
        inserted = ingest_builtins(session)
    typer.echo(f"Ingested {inserted} built-in seeds")


@app.command("refresh")
def refresh(city: Optional[str] = None) -> None:
    with get_session() as session:
        result = run_discovery(session, city=city)
    typer.echo(result)


@app.command("infer")
def infer() -> None:
    with get_session() as session:
        created = infer_rules(session)
    typer.echo(f"Created {created} rules")


@app.command("browse")
def browse(city: str = "NYC") -> None:
    with get_session() as session:
        rows = session.exec(select(Restaurant).where(Restaurant.city == city.upper())).all()
    for r in rows:
        typer.echo(f"[{r.id}] {r.name} | source={r.source} | pop={r.popularity_score:.2f}")


@app.command("plan")
def plan(
    restaurant: int,
    party: int,
    date: str,
    time_window: str,
    mode: str = "deeplink",
    dry_run: bool = True,
    profile: Optional[str] = None,
) -> None:
    parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    with get_session() as session:
        rule = session.exec(select(DropRule).where(DropRule.restaurant_id == restaurant)).first()
        if not rule:
            raise typer.BadParameter("No drop rule for restaurant")
        request = BookingRequest(
            restaurant_id=restaurant,
            party_size=party,
            target_date=parsed_date,
            time_window=time_window,
            mode=mode,
            dry_run=dry_run,
            profile=profile,
        )
        session.add(request)
        session.commit()
        session.refresh(request)

        run_at = compute_drop_datetime(parsed_date, rule.days_ahead, rule.drop_time)
        job = Job(booking_request_id=request.id, run_at=run_at)
        session.add(job)
        session.commit()
    typer.echo(f"Planned request={request.id} job={job.id} run_at={run_at.isoformat()}")


@app.command("book")
def book(
    request_id: int,
    assist: bool = False,
    dry_run: bool = True,
    confirm: bool = False,
) -> None:
    with get_session() as session:
        result = execute_booking(session, request_id=request_id, assist=assist, dry_run=dry_run, user_confirm=confirm)
    typer.echo(f"{result.status}: {result.message}")


@app.command("jobs")
def jobs() -> None:
    with get_session() as session:
        rows = session.exec(select(Job)).all()
    for j in rows:
        typer.echo(f"[{j.id}] request={j.booking_request_id} run_at={j.run_at} status={j.status}")


@app.command("edit")
def edit(restaurant_id: int, days_ahead: Optional[int] = None, drop_time: Optional[str] = None) -> None:
    with get_session() as session:
        rule = session.exec(select(DropRule).where(DropRule.restaurant_id == restaurant_id)).first()
        if not rule:
            raise typer.BadParameter("No rule for restaurant")
        if days_ahead is not None:
            rule.days_ahead = days_ahead
        if drop_time is not None:
            rule.drop_time = datetime.strptime(drop_time, "%H:%M").time()
        rule.manual_override = True
        session.add(rule)
        session.commit()
    typer.echo("Rule updated")


@app.command("export")
def export(path: str = "export.csv") -> None:
    out = Path(path)
    with get_session() as session:
        rows = session.exec(select(Restaurant)).all()
    lines = ["id,name,city,source,popularity_score"]
    for r in rows:
        lines.append(f"{r.id},{r.name},{r.city},{r.source},{r.popularity_score}")
    out.write_text("\n".join(lines), encoding="utf-8")
    typer.echo(f"Exported {len(rows)} restaurants to {path}")


if __name__ == "__main__":
    app()
