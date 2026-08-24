"""Zabbix item provisioning for Ubuntu Desktop.

This module creates missing items, updates existing item metadata,
and migrates legacy PC Guardian keys to the current base-unit keys.
"""

from __future__ import annotations

import re
from typing import Any

from zabbix.provisioning.definitions import BASE_ITEMS

LEGACY_KEYS = {
    "pcguardian.memory.available": "pcguardian.memory.available.mb",
    "pcguardian.disk.root.free": "pcguardian.disk.root.free.gb",
    "pcguardian.disk.read": "pcguardian.disk.read.mbps",
    "pcguardian.disk.write": "pcguardian.disk.write.mbps",
}


def _safe_component(name: str) -> str:
    """Convert a process name into a Zabbix key component."""
    clean = re.sub(
        r"[^a-z0-9]+",
        ".",
        name.lower(),
    ).strip(".")

    return clean or "unknown"


def build_item_definitions(
    watchlist: list[str],
) -> list[tuple[str, str, int, str]]:
    """Build all base and process item definitions."""
    items = list(BASE_ITEMS)

    for process in watchlist:
        component = _safe_component(process)

        items.extend(
            [
                (
                    f"{process}: CPU",
                    f"pcguardian.process.{component}.cpu",
                    0,
                    "%",
                ),
                (
                    f"{process}: memory",
                    f"pcguardian.process.{component}.memory",
                    0,
                    "%",
                ),
                (
                    f"{process}: instances",
                    f"pcguardian.process.{component}.instances",
                    3,
                    "",
                ),
            ]
        )

    return items


def _needs_update(
    item: dict,
    name: str,
    value_type: int,
    units: str,
) -> bool:
    """Return whether item metadata differs from its definition."""
    return (
        item.get("name") != name
        or int(
            item.get(
                "value_type",
                -1,
            )
        )
        != value_type
        or item.get(
            "units",
            "",
        )
        != units
    )


def ensure_items(
    api: Any,
    template_id: str,
    watchlist: list[str],
) -> tuple[int, int, int]:
    """Create, update, and migrate Zabbix items.

    Args:
        api: Authenticated Zabbix API client.
        template_id: Ubuntu Desktop template ID.
        watchlist: Processes configured for monitoring.

    Returns:
        Tuple containing:
            - total definitions;
            - number of new items created;
            - number of existing items updated/migrated.
    """
    definitions = build_item_definitions(watchlist)

    existing = api.call(
        "item.get",
        {
            "output": [
                "itemid",
                "name",
                "key_",
                "value_type",
                "units",
            ],
            "templateids": [
                template_id,
            ],
        },
    )

    items_by_key = {item["key_"]: item for item in existing}

    created = 0
    updated = 0

    for (
        name,
        key,
        value_type,
        units,
    ) in definitions:
        item = items_by_key.get(key)

        if item is not None:
            if _needs_update(
                item,
                name,
                value_type,
                units,
            ):
                api.call(
                    "item.update",
                    {
                        "itemid": item["itemid"],
                        "name": name,
                        "value_type": value_type,
                        "units": units,
                    },
                )

                updated += 1

            continue

        legacy_key = LEGACY_KEYS.get(key)

        legacy_item = items_by_key.get(legacy_key) if legacy_key else None

        if legacy_item is not None:
            api.call(
                "item.update",
                {
                    "itemid": legacy_item["itemid"],
                    "name": name,
                    "key_": key,
                    "value_type": value_type,
                    "units": units,
                },
            )

            items_by_key.pop(
                legacy_key,
                None,
            )

            legacy_item["key_"] = key
            items_by_key[key] = legacy_item

            updated += 1
            continue

        api.call(
            "item.create",
            {
                "name": name,
                "key_": key,
                "hostid": template_id,
                "type": 2,
                "value_type": value_type,
                "delay": "0",
                "history": "30d",
                "trends": "365d",
                "units": units,
            },
        )

        created += 1

    return (
        len(definitions),
        created,
        updated,
    )
