"""Zabbix Host Group provisioning.

This module manages the Host Group required by the Ubuntu Desktop
monitoring template.

The module only creates or retrieves the Host Group. It does not
create, modify, search, or link Zabbix hosts.
"""

from __future__ import annotations

from typing import Any


def ensure_hostgroup(
    api: Any,
    group_name: str,
) -> tuple[str, bool]:
    """Ensure that a Zabbix Host Group exists.

    If the Host Group already exists, its ID is returned.
    Otherwise, a new Host Group is created.

    Args:
        api: Authenticated Zabbix API client.
        group_name: Name of the Host Group.

    Returns:
        A tuple containing:
            - Host Group ID.
            - True if the Host Group was created.
            - False if the Host Group already existed.

    Raises:
        RuntimeError: If Zabbix does not return a valid group ID.
    """
    groups = api.call(
        "hostgroup.get",
        {
            "output": [
                "groupid",
                "name",
            ],
            "filter": {
                "name": [group_name],
            },
        },
    )

    if groups:
        group_id = groups[0].get("groupid")

        if not group_id:
            raise RuntimeError(f"Zabbix no devolvió groupid para Host Group: {group_name}")

        return group_id, False

    result = api.call(
        "hostgroup.create",
        {
            "name": group_name,
        },
    )

    group_ids = result.get("groupids", [])

    if not group_ids:
        raise RuntimeError(f"Zabbix no devolvió groupids al crear Host Group: {group_name}")

    return group_ids[0], True
