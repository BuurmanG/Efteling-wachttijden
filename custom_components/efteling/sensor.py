from __future__ import annotations

import re

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN, PARK_ID
from .coordinator import EftelingCoordinator


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("'", "")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EftelingCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    entities = []

    for attraction_id, attraction in coordinator.data.items():
        entities.append(
            EftelingWaitSensor(
                coordinator,
                attraction_id,
            )
        )

        entities.append(
            EftelingStatusSensor(
                coordinator,
                attraction_id,
            )
        )

    async_add_entities(entities)


class EftelingBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: EftelingCoordinator,
        attraction_id: str,
    ) -> None:
        super().__init__(coordinator)

        self.attraction_id = attraction_id

    @property
    def attraction(self):
        return self.coordinator.data.get(self.attraction_id, {})

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, PARK_ID)},
            name="Efteling",
            manufacturer="Efteling",
            configuration_url=(
                "https://www.efteling.com/"
            ),
        )


class EftelingWaitSensor(EftelingBaseSensor):
    @property
    def name(self) -> str:
        return (
            f"Efteling "
            f"{self.attraction.get('name', 'Attraction')} "
            f"Wachttijd"
        )

    @property
    def unique_id(self) -> str:
        return (
            f"{DOMAIN}_"
            f"{self.attraction_id}_"
            f"wait_time"
        )

    @property
    def native_unit_of_measurement(self):
        return UnitOfTime.MINUTES

    @property
    def native_value(self):
        queue = self.attraction.get("queue") or {}
        standby = queue.get("STANDBY") or {}

        wait_time = standby.get("waitTime")

        # No wait time available, e.g. attraction closed
        if wait_time is None:
            return 0

        return wait_time


class EftelingStatusSensor(EftelingBaseSensor):
    @property
    def name(self) -> str:
        return (
            f"Efteling "
            f"{self.attraction.get('name', 'Attraction')} "
            f"Status"
        )

    @property
    def unique_id(self) -> str:
        return (
            f"{DOMAIN}_"
            f"{self.attraction_id}_"
            f"status"
        )

    @property
    def native_value(self):
        return self.attraction.get(
            "status",
            "UNKNOWN",
        )