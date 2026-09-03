from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import DEFAULT_NAME, DOMAIN


class EftelingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )