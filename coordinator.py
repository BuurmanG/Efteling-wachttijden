from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import API_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class EftelingCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

        super().__init__(
            hass,
            _LOGGER,
            name="Efteling",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )

    async def _async_update_data(self):
        try:
            timeout = aiohttp.ClientTimeout(total=30)

            async with aiohttp.ClientSession(
                timeout=timeout
            ) as session:
                async with session.get(API_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

            live_data = data.get("liveData", [])

            return {
                item["id"]: item
                for item in live_data
                if item.get("entityType") == "ATTRACTION"
            }

        except Exception as err:
            raise UpdateFailed(
                f"Unable to retrieve Efteling data: {err}"
            ) from err