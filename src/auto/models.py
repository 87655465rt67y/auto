from dataclasses import dataclass


@dataclass(frozen=True)
class BrandItem:
    brand: str
    platform: str
