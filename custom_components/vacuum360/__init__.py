"""The 360 Vacuum integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import Vacuum360Api
from .const import DOMAIN, PLATFORMS
from .coordinator import Vacuum360Coordinator


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the 360 Vacuum integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up 360 Vacuum from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api = Vacuum360Api(
        username=entry.data["username"],
        password=entry.data["password"],
        sn=entry.data["sn"],
    )

    await api.async_login()

    coordinator = Vacuum360Coordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "entry": entry.data,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok