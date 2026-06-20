"""Data models for 360 Vacuum."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vacuum360Status:
    """Current robot status."""

    battery: int
    state: str
    fan_mode: str
    water_level: int
    map_id: int
    map_name: str
    clean_area: float
    clean_time: int
    wifi: int
    dock: bool
    error: str | None