"""The eventsubscription integration."""

from __future__ import annotations
import logging

from hawhodid import WhoDid

from homeassistant.core import HomeAssistant, ServiceCall, Event
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.core import State
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
import asyncio

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

    async def handle_send_message_dynamic(call: ServiceCall):
        whodidInstance = WhoDid(hass=call.hass)

        userid = await whodidInstance.getUserId(context=call.context)

        if userid == None:
            return

        notify_entries = call.hass.config_entries.async_entries(domain="group")
        person_notify_entities = []

        for entry in notify_entries:
            if entry.source == "personnotify":
                person_notify_entities.append(entry)

        for entry in person_notify_entities:
            if entry.data["user_id"] == userid:
                _LOGGER.debug(f"Notifiy user with user_id {userid}")

                await call.hass.services.async_call(
                    domain="notify",
                    service="send_message",
                    target={
                        "entity_id": f"{entry.options['group_type']}.{entry.options['name']}"
                    },
                    service_data={"title": "", "message": call.data["message"]},
                )

    hass.services.async_register(
        DOMAIN, "sendmessagedynamic", handle_send_message_dynamic
    )

    return True
