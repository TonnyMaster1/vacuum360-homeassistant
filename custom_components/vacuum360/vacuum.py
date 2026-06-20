"""Vacuum platform for 360 Vacuum."""

from __future__ import annotations

from homeassistant.components.vacuum import StateVacuumEntity, VacuumEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


FAN_MODE_MAP = {
    "quiet": "Silencieux",
    "auto": "Standard",
    "strong": "Puissant",
    "max": "Max",
}

STATE_IDLE = "idle"
STATE_CLEANING = "cleaning"
STATE_PAUSED = "paused"
STATE_DOCKED = "docked"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the 360 vacuum entity."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities([Vacuum360Entity(coordinator, data["api"], entry)])


class Vacuum360Entity(CoordinatorEntity, StateVacuumEntity):
    """Representation of a 360 vacuum."""

    _attr_supported_features = (
        VacuumEntityFeature.START
        | VacuumEntityFeature.PAUSE
        | VacuumEntityFeature.RETURN_HOME
        | VacuumEntityFeature.LOCATE
        | VacuumEntityFeature.FAN_SPEED
    )

    _attr_fan_speed_list = ["Silencieux", "Standard", "Puissant", "Max"]

    def __init__(self, coordinator, api, entry: ConfigEntry) -> None:
        """Initialize the vacuum."""
        super().__init__(coordinator)
        self._api = api

        self._attr_unique_id = entry.data["sn"]
        self._attr_name = entry.data["name"]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["sn"])},
            "name": entry.data["name"],
            "manufacturer": "360",
            "model": entry.data.get("model"),
        }

    @property
    def state(self) -> str:
        """Return the state of the vacuum."""
        state = self.coordinator.data.state

        if state == "cleaning":
            return STATE_CLEANING

        if state == "paused":
            return STATE_PAUSED

        if state == "docked":
            return STATE_DOCKED

        return STATE_IDLE

    @property
    def fan_speed(self) -> str | None:
        """Return current fan speed."""
        return FAN_MODE_MAP.get(self.coordinator.data.fan_mode)

    async def async_start(self) -> None:
        """Start cleaning."""
        await self._api.async_start()
        await self.coordinator.async_request_refresh()

    async def async_pause(self) -> None:
        """Pause cleaning."""
        await self._api.async_pause()
        await self.coordinator.async_request_refresh()

    async def async_return_to_base(self, **kwargs) -> None:
        """Return to base."""
        await self._api.async_return_to_base()
        await self.coordinator.async_request_refresh()

    async def async_locate(self, **kwargs) -> None:
        """Locate robot."""
        await self._api.async_locate()

    async def async_set_fan_speed(self, fan_speed: str, **kwargs) -> None:
        """Set fan speed."""
        reverse_map = {
            "Silencieux": "quiet",
            "Standard": "auto",
            "Puissant": "strong",
            "Max": "max",
        }

        await self._api.async_set_fan_mode(reverse_map[fan_speed])
        await self.coordinator.async_request_refresh()