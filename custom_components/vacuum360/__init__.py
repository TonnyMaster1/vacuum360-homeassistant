"""The 360 Vacuum integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import Vacuum360Api
from .coordinator import Vacuum360Coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.VACUUM,
    Platform.SENSOR,
    Platform.SELECT,
    Platform.BUTTON,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up 360 Vacuum from a config entry."""

    session = async_get_clientsession(hass)

    api = Vacuum360Api(
        username=entry.data["username"],
        password=entry.data["password"],
        sn=entry.data["sn"],
        session=session,
    )

    await api.async_login()

    coordinator = Vacuum360Coordinator(
        hass,
        api,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("vacuum360", {})

    hass.data["vacuum360"][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    _LOGGER.info("360 Vacuum initialized")

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data["vacuum360"].pop(entry.entry_id)

    return unload_ok