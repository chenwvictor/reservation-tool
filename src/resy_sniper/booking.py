from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass

from sqlmodel import Session

from resy_sniper.config import settings
from resy_sniper.models import BookingRequest, Restaurant
from resy_sniper.providers import DeepLinkBuilder


def redact_pii(s: str) -> str:
    # Redacts emails + phone-ish digits. Keeps minimal utility in logs.
    out = s
    out = out.replace("@", "[at]") if "@" in out else out
    digits = "".join(ch for ch in out if ch.isdigit())
    if len(digits) >= 7:
        digest = hashlib.sha256(digits.encode()).hexdigest()[:8]
        out = f"[redacted_phone_hash:{digest}]"
    return out


@dataclass
class BookingResult:
    status: str
    message: str


def _needs_user_challenge_pause() -> bool:
    # TODO: detect challenge/login selectors once provider pages are validated.
    return True


def execute_booking(
    session: Session,
    request_id: int,
    assist: bool = False,
    dry_run: bool = True,
    user_confirm: bool = False,
) -> BookingResult:
    req = session.get(BookingRequest, request_id)
    if not req:
        return BookingResult("error", "request not found")
    restaurant = session.get(Restaurant, req.restaurant_id)
    if not restaurant:
        return BookingResult("error", "restaurant missing")

    deep_link = restaurant.provider_url or DeepLinkBuilder.resy_search(restaurant.name, restaurant.city)

    if dry_run or req.dry_run:
        return BookingResult("dry_run", f"Would open {deep_link}")

    if assist:
        # Assisted behavior only; never bypass challenges.
        if _needs_user_challenge_pause():
            return BookingResult("paused", "Challenge/login detected. Complete manually then resume.")
        time.sleep(settings.booking_refresh_seconds + random.randint(0, settings.booking_jitter_seconds))

    if not user_confirm:
        return BookingResult("awaiting_confirmation", "Explicit confirmation required before final submit")

    req.status = "submitted"
    session.add(req)
    session.commit()
    return BookingResult("submitted", redact_pii(f"Submitted booking for request {req.id}"))
