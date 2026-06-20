"""Sensor platform for 360 Vacuum."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfArea, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSORS = [
    {"key": "battery", "name": "360 Batterie", "unit": PERCENTAGE},
    {"key": "map_name", "name": "360 Carte active", "unit": None},
    {"key": "clean_area", "name": "360 Surface nettoyée", "unit": UnitOfArea.SQUARE_METERS},
    {"key": "clean_time", "name": "360 Temps nettoyage", "unit": UnitOfTime.MINUTES},
    {"key": "wifi", "name": "360 Wi-Fi", "unit": "dBm"},
    {"key": "state", "name": "360 État brut", "unit": None},
    {"key": "fan_mode", "name": "360 Mode aspiration", "unit": None},
    {"key": "water_level", "name": "360 Niveau eau", "unit": None},
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities(
        [Vacuum360Sensor(coordinator, entry, sensor) for sensor in SENSORS]
    )


class Vacuum360Sensor(CoordinatorEntity, SensorEntity):
    """Generic 360 sensor."""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sensor: dict[str, Any],
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)

        self._key = sensor["key"]
        self._attr_unique_id = f"{entry.data['sn']}_{self._key}"
        self._attr_name = sensor["name"]
        self._attr_native_unit_of_measurement = sensor["unit"]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["sn"])},
        }

    @property
    def native_value(self):
        """Return sensor value."""
        return getattr(self.coordinator.data, self._key, None)