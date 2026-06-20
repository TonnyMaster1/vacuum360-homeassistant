"""Coordinator for 360 Vacuum."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class Vacuum360Coordinator(DataUpdateCoordinator):
    """360 Vacuum coordinator."""

    def __init__(self, hass, api) -> None:
        """Initialize coordinator."""
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name="360 Vacuum",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch vacuum data."""
        return await self.api.async_get_status()