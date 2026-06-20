"""Cloud API client for 360 Vacuum."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from .models import Vacuum360Status

_LOGGER = logging.getLogger(__name__)


class Vacuum360ApiError(Exception):
    """Base exception."""


class Vacuum360AuthError(Vacuum360ApiError):
    """Authentication error."""


@dataclass
class Vacuum360Device:
    """360 device."""

    sn: str
    name: str
    model: str | None = None


class Vacuum360Api:
    """360 cloud API client."""

    def __init__(self, username: str, password: str, sn: str | None = None) -> None:
        """Initialize API."""
        self.username = username
        self.password = password
        self.sn = sn
        self.token: str | None = None

    async def async_login(self) -> bool:
        """Temporary login placeholder."""
        if not self.username or not self.password:
            raise Vacuum360AuthError("Missing username or password")

        self.token = "temporary-token"
        _LOGGER.warning(">>> 360 LOGIN OK <<<")
        return True

    async def async_get_devices(self) -> list[Vacuum360Device]:
        """Temporary device discovery."""
        if self.token is None:
            raise Vacuum360AuthError("Not authenticated")

        _LOGGER.warning(">>> 360 GET DEVICES <<<")

        return [
            Vacuum360Device(
                sn="360TY820103026954",
                name="Aspirateur !",
                model="X80-L",
            )
        ]

    async def async_get_status(self) -> Vacuum360Status:
        """Return robot status placeholder."""
        if self.token is None:
            raise Vacuum360AuthError("Not authenticated")

        _LOGGER.warning(">>> GET STATUS <<<")

        return Vacuum360Status(
            battery=98,
            state="cleaning",
            fan_mode="strong",
            water_level=3,
            map_id=3,
            map_name="Sous-sol",
            clean_area=47.2,
            clean_time=53,
            wifi=-52,
            dock=False,
            error=None,
        )

    async def async_send_command(
        self,
        info_type: int,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Temporary command transport."""
        if self.token is None:
            raise Vacuum360AuthError("Not authenticated")

        _LOGGER.warning(">>> 360 SEND COMMAND <<<")
        _LOGGER.warning("SN: %s", self.sn)
        _LOGGER.warning("infoType: %s", info_type)
        _LOGGER.warning("data: %s", data)

        return {
            "sn": self.sn,
            "infoType": info_type,
            "data": data,
            "success": False,
            "message": "Cloud transport not implemented yet",
        }

    async def async_start(self) -> dict[str, Any]:
        """Start cleaning."""
        _LOGGER.warning(">>> START CLEAN <<<")
        return await self.async_send_command(
            21005,
            {"mode": "smartClean", "globalCleanTimes": 1},
        )

    async def async_pause(self) -> dict[str, Any]:
        """Pause cleaning."""
        _LOGGER.warning(">>> PAUSE <<<")
        return await self.async_send_command(21017, {"cmd": "pause"})

    async def async_continue(self) -> dict[str, Any]:
        """Resume cleaning."""
        _LOGGER.warning(">>> CONTINUE <<<")
        return await self.async_send_command(21017, {"cmd": "continue"})

    async def async_return_to_base(self) -> dict[str, Any]:
        """Return robot to dock."""
        _LOGGER.warning(">>> RETURN HOME <<<")
        return await self.async_send_command(21012, {"cmd": "start"})

    async def async_locate(self) -> dict[str, Any]:
        """Locate robot."""
        _LOGGER.warning(">>> LOCATE <<<")
        return await self.async_send_command(21020, {"ctrlCode": 3010})

    async def async_set_fan_mode(self, mode: str) -> dict[str, Any]:
        """Set fan mode."""
        _LOGGER.warning(">>> SET FAN MODE: %s <<<", mode)
        return await self.async_send_command(
            21022,
            {"cmd": mode, "cleanType": "total"},
        )

    async def async_set_water_level(self, level: int) -> dict[str, Any]:
        """Set water level."""
        _LOGGER.warning(">>> SET WATER LEVEL: %s <<<", level)
        return await self.async_send_command(
            21024,
            {"cmd": "setWaterPump", "value": level, "cleanType": "total"},
        )