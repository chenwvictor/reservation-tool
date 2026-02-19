from __future__ import annotations

from urllib.parse import urlencode

from .models import BookingRequest, Provider, Restaurant


class ProviderAdapter:
    def build_deeplink(self, restaurant: Restaurant, request: BookingRequest) -> str:
        raise NotImplementedError


class ResyAdapter(ProviderAdapter):
    def build_deeplink(self, restaurant: Restaurant, request: BookingRequest) -> str:
        params = urlencode({
            "date": request.date_target.isoformat(),
            "seats": request.party_size,
            "time": request.time_window_start,
        })
        base = restaurant.provider_url or "https://resy.com"
        return f"{base}?{params}"


class OpenTableAdapter(ProviderAdapter):
    def build_deeplink(self, restaurant: Restaurant, request: BookingRequest) -> str:
        params = urlencode({
            "date": request.date_target.isoformat(),
            "covers": request.party_size,
            "time": request.time_window_start,
        })
        base = restaurant.provider_url or "https://www.opentable.com"
        return f"{base}?{params}"


def adapter_for(provider: Provider) -> ProviderAdapter:
    if provider == Provider.RESY:
        return ResyAdapter()
    return OpenTableAdapter()
