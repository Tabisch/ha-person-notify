"""The eventsubscription integration."""

from __future__ import annotations
import logging

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.core import State
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .const import DOMAIN

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

_PLATFORMS: list[Platform] = [Platform.NOTIFY]

_LOGGER = logging.getLogger(__name__)


async def createEntry(hass: HomeAssistant, person_entity):
    _LOGGER.debug(
        f"Creating notify entity for user {person_entity.attributes['user_id']}"
    )

    domain = "group"
    data = {"user_id": person_entity.attributes["user_id"]}
    version = 1
    minor_version = 1
    title = person_entity.attributes["friendly_name"]
    source = DOMAIN
    discovery_keys = {}
    options = {
        "entities": [],
        "group_type": "notify",
        "hide_members": False,
        "name": person_entity.attributes["friendly_name"],
    }

    entry = ConfigEntry(
        domain=domain,
        data=data,
        version=version,
        minor_version=minor_version,
        title=title,
        source=source,
        discovery_keys=discovery_keys,
        options=options,
        unique_id=None,
        subentries_data=[],
    )

    await hass.config_entries.async_add(entry=entry)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.info(f"The {__name__} component is ready!")

    personList = hass.states.async_entity_ids(domain_filter="person")

    notify_entries = hass.config_entries.async_entries(domain="group")
    already_created_entries = []

    for entry in notify_entries:
        if entry.source == DOMAIN:
            already_created_entries.append(entry)

    for person_id in personList:
        person_entity: State = hass.states.get(entity_id=person_id)

        notifyEnitityExists = False

        for entry in already_created_entries:
            if entry.data["user_id"] == person_entity.attributes["user_id"]:
                _LOGGER.debug(
                    f"Entity for user_id {person_entity.attributes['user_id']} already exists"
                )
                notifyEnitityExists = True

        if notifyEnitityExists:
            continue

        await createEntry(hass=hass, person_entity=person_entity)

    return True
