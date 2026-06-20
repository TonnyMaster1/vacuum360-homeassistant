"""Select platform for 360 Vacuum."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


FAN_MODES = {
    "Silencieux": "quiet",
    "Standard": "auto",
    "Puissant": "strong",
    "Max": "max",
}

WATER_LEVELS = {
    "Bas": 1,
    "Moyen": 2,
    "Élevé": 3,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""
    data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            Vacuum360FanSelect(data["api"], entry),
            Vacuum360WaterSelect(data["api"], entry),
        ]
    )


class Vacuum360FanSelect(SelectEntity):
    """Fan mode select."""

    _attr_options = list(FAN_MODES.keys())

    def __init__(self, api, entry: ConfigEntry) -> None:
        """Initialize fan select."""
        self._api = api
        self._attr_unique_id = f"{entry.data['sn']}_fan_mode"
        self._attr_name = "360 Aspiration"
        self._attr_current_option = "Standard"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["sn"])},
        }

    async def async_select_option(self, option: str) -> None:
        """Change fan mode."""
        self._attr_current_option = option
        await self._api.async_set_fan_mode(FAN_MODES[option])
        self.async_write_ha_state()


class Vacuum360WaterSelect(SelectEntity):
    """Water level select."""

    _attr_options = list(WATER_LEVELS.keys())

    def __init__(self, api, entry: ConfigEntry) -> None:
        """Initialize water select."""
        self._api = api
        self._attr_unique_id = f"{entry.data['sn']}_water_level"
        self._attr_name = "360 Eau"
        self._attr_current_option = "Moyen"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["sn"])},
        }

    async def async_select_option(self, option: str) -> None:
        """Change water level."""
        self._attr_current_option = option
        await self._api.async_set_water_level(WATER_LEVELS[option])
        self.async_write_ha_state()