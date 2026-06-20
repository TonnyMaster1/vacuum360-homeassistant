"""Config flow for 360 Vacuum."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from .api import Vacuum360Api, Vacuum360AuthError
from .const import DOMAIN


class Vacuum360ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 360 Vacuum."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api = Vacuum360Api(
                username=user_input["username"],
                password=user_input["password"],
            )

            try:
                await api.async_login()
                devices = await api.async_get_devices()
            except Vacuum360AuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"
            else:
                device = devices[0]

                await self.async_set_unique_id(device.sn)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=device.name,
                    data={
                        "username": user_input["username"],
                        "password": user_input["password"],
                        "sn": device.sn,
                        "name": device.name,
                        "model": device.model,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )