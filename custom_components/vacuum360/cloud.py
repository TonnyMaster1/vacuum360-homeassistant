"""360 Cloud client."""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://q.smart.360.cn"


class Vacuum360Cloud:
    """360 cloud transport."""

    def __init__(self, session: ClientSession, qid: str, sid: str) -> None:
        self._session = session
        self._qid = qid
        self._sid = sid

    @property
    def _cookies(self) -> dict[str, str]:
        return {
            "qid": self._qid,
            "sid": self._sid,
        }

    async def async_send_command(
        self,
        sn: str,
        info_type: int,
        data: dict[str, Any] | str | None,
    ) -> dict[str, Any]:
        """Send command to 360 cloud."""
        url = f"{BASE_URL}/clean/cmd/send"

        payload = {
            "sn": sn,
            "infoType": info_type,
            "data": json.dumps(data) if isinstance(data, dict) else data or "",
            "taskid": str(uuid.uuid4()),
        }

        _LOGGER.warning(">>> CLOUD SEND <<<")
        _LOGGER.warning("url=%s", url)
        _LOGGER.warning("payload=%s", payload)

        async with self._session.post(
            url,
            data=payload,
            cookies=self._cookies,
            headers={
                "User-Agent": "360Robot/1.0",
                "lang": "fr_CA",
            },
        ) as response:
            text = await response.text()
            _LOGGER.warning("cloud response=%s", text)

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "errno": -1,
                    "errmsg": "Invalid JSON response",
                    "raw": text,
                }