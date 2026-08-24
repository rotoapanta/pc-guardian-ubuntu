"""Zabbix template-group and template provisioning."""

from __future__ import annotations

from typing import Any


def ensure_template_group(api: Any, group_name: str) -> tuple[str, bool]:
    """Return a template-group ID, creating the group when necessary."""
    rows = api.call(
        "templategroup.get",
        {"output": ["groupid", "name"], "filter": {"name": [group_name]}},
    )
    if rows:
        return rows[0]["groupid"], False
    result = api.call("templategroup.create", {"name": group_name})
    return result["groupids"][0], True


def ensure_template(api: Any, template_name: str, group_id: str) -> tuple[str, bool]:
    """Return a template ID, creating the template when necessary."""
    rows = api.call(
        "template.get",
        {"output": ["templateid", "host", "name"], "filter": {"host": [template_name]}},
    )
    if rows:
        return rows[0]["templateid"], False
    result = api.call(
        "template.create",
        {
            "host": template_name,
            "name": template_name,
            "groups": [{"groupid": group_id}],
        },
    )
    return result["templateids"][0], True
