from __future__ import annotations

import webbrowser

from rich.console import Console

from .models import BookingRequest, Restaurant
from .providers import adapter_for

console = Console()


def execute_booking(restaurant: Restaurant, request: BookingRequest, assist: bool = False) -> None:
    adapter = adapter_for(restaurant.provider)
    url = adapter.build_deeplink(restaurant, request)
    if assist:
        console.print("[yellow]Assist mode selected. Playwright flow is a safe stub in MVP.[/yellow]")
        console.print("Open page, prefill fields, pause for CAPTCHA/login/2FA, ask confirmation before submit.")
    if request.dry_run:
        console.print(f"[cyan]DRY RUN:[/cyan] would open {url}")
        return
    webbrowser.open(url)
    console.print(f"Opened booking link: {url}")
