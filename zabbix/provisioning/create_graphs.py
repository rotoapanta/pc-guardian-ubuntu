"""Zabbix graph provisioning for Ubuntu Desktop monitoring.

This module creates reusable graphs associated with the Ubuntu Desktop
template.

Graphs are created only when they do not already exist.
"""

from __future__ import annotations

from typing import Any

GRAPH_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "Ubuntu Desktop: CPU",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.cpu.util",
                "1A7CFF",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: Temperatures",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.cpu.temperature",
                "FF0000",
            ),
            (
                "pcguardian.nvme.temperature",
                "FF9900",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: Memory and Swap",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.memory.util",
                "1A7CFF",
            ),
            (
                "pcguardian.swap.util",
                "FF0000",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: Disk Utilization",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.disk.root.util",
                "00AA00",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: Disk I/O",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.disk.read",
                "1A7CFF",
            ),
            (
                "pcguardian.disk.write",
                "FF0000",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: PSI Pressure",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.psi.cpu.avg10",
                "1A7CFF",
            ),
            (
                "pcguardian.psi.memory.avg10",
                "FF0000",
            ),
            (
                "pcguardian.psi.io.avg10",
                "FF9900",
            ),
        ],
    },
    {
        "name": "Ubuntu Desktop: D-State and i915",
        "width": 900,
        "height": 200,
        "items": [
            (
                "pcguardian.process.dstate.count",
                "FF0000",
            ),
            (
                "pcguardian.process.i915.dstate.count",
                "990099",
            ),
        ],
    },
]


def _get_item_id(
    api: Any,
    template_id: str,
    key: str,
) -> str:
    """Return the Zabbix item ID for a template item key.

    Args:
        api: Authenticated Zabbix API client.
        template_id: Zabbix template identifier.
        key: Zabbix item key.

    Returns:
        Zabbix item identifier.

    Raises:
        RuntimeError: If the requested item cannot be found.
    """
    items = api.call(
        "item.get",
        {
            "output": [
                "itemid",
                "key_",
            ],
            "templateids": [
                template_id,
            ],
            "filter": {
                "key_": [
                    key,
                ],
            },
        },
    )

    if not items:
        raise RuntimeError(
            f"No se encontró el item con key '{key}' en el template id={template_id}"
        )

    return items[0]["itemid"]


def ensure_graphs(
    api: Any,
    template_id: str,
) -> tuple[int, int]:
    """Create missing graphs for the Ubuntu Desktop template.

    Existing graphs are matched by name and are not duplicated.

    Args:
        api: Authenticated Zabbix API client.
        template_id: Zabbix template identifier.

    Returns:
        Tuple containing:
            - Total number of graph definitions.
            - Number of graphs created.
    """
    existing_graphs = api.call(
        "graph.get",
        {
            "output": [
                "graphid",
                "name",
            ],
            "templateids": [
                template_id,
            ],
        },
    )

    existing_names = {graph["name"] for graph in existing_graphs}

    created = 0

    for definition in GRAPH_DEFINITIONS:
        graph_name = definition["name"]

        if graph_name in existing_names:
            continue

        graph_items: list[dict[str, Any]] = []

        for sort_order, item_definition in enumerate(definition["items"]):
            key, color = item_definition

            item_id = _get_item_id(
                api,
                template_id,
                key,
            )

            graph_items.append(
                {
                    "itemid": item_id,
                    "sortorder": sort_order,
                    "color": color,
                    # 2 = Average
                    "calc_fnc": 2,
                    # 5 = Gradient line
                    "drawtype": 5,
                    # 0 = Left Y axis
                    "yaxisside": 0,
                    # 0 = Simple graph item
                    "type": 0,
                }
            )

        api.call(
            "graph.create",
            {
                "name": graph_name,
                "width": int(
                    definition.get(
                        "width",
                        900,
                    )
                ),
                "height": int(
                    definition.get(
                        "height",
                        200,
                    )
                ),
                "gitems": graph_items,
                "show_work_period": 1,
                "show_triggers": 1,
                "show_legend": 1,
                "show_3d": 0,
                "graphtype": 0,
            },
        )

        created += 1

    return (
        len(GRAPH_DEFINITIONS),
        created,
    )
