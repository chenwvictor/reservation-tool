from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass
class ProviderMatch:
    provider: str
    canonical_url: str
    external_id: str | None = None


class DeepLinkBuilder:
    @staticmethod
    def resy_search(name: str, city: str) -> str:
        return f"https://resy.com/cities/{city.lower()}?query={quote_plus(name)}"

    @staticmethod
    def opentable_search(name: str, city: str) -> str:
        return f"https://www.opentable.com/s?term={quote_plus(name + ' ' + city)}"


class ResyAdapter:
    """Use official API only when authorized credentials are available."""

    def __init__(self, api_key: str = "", base_url: str = "") -> None:
        self.api_key = api_key
        self.base_url = base_url

    def search(self, name: str, city: str) -> ProviderMatch:
        if self.api_key and self.base_url:
            # TODO: implement official partner API request with credentials.
            # Expected sample response shape in tests:
            # {"results": [{"id": "123", "name": "Atomix", "url": "https://resy.com/..."}]}
            return ProviderMatch(provider="resy", canonical_url=f"{self.base_url}/search/{quote_plus(name)}")
        return ProviderMatch(provider="resy", canonical_url=DeepLinkBuilder.resy_search(name, city))


class OpenTableAdapter:
    """Use official API/sandbox only when authorized credentials are available."""

    def __init__(self, api_key: str = "", base_url: str = "") -> None:
        self.api_key = api_key
        self.base_url = base_url

    def search(self, name: str, city: str) -> ProviderMatch:
        if self.api_key and self.base_url:
            # TODO: implement official API request with credentials.
            # Expected sample response shape in tests:
            # {"restaurants": [{"rid": "abc", "name": "Vetri", "reserve_url": "https://opentable.com/..."}]}
            return ProviderMatch(provider="opentable", canonical_url=f"{self.base_url}/search/{quote_plus(name)}")
        return ProviderMatch(provider="opentable", canonical_url=DeepLinkBuilder.opentable_search(name, city))
