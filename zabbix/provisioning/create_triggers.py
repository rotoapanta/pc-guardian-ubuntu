"""Zabbix trigger provisioning for Ubuntu Desktop monitoring.

This module creates and synchronizes the triggers associated with the
Ubuntu Desktop template.

Zabbix internally stores trigger functions using numeric function IDs.
To make provisioning idempotent, trigger expressions are requested in
expanded form whenever possible.

Legacy trigger descriptions are also detected and migrated to the
current template-based naming convention.
"""

from __future__ import annotations

import re
from typing import Any

from zabbix.provisioning.definitions import (
    LEGACY_TRIGGER_NAMES,
    TRIGGERS,
)

_FUNCTION_ID_PATTERN = re.compile(r"\{\d+\}")


def _render_template(
    value: str,
    template_name: str,
) -> str:
    """Replace the template placeholder with the configured name.

    Args:
        value: String containing the ``{TEMPLATE}`` placeholder.
        template_name: Current Zabbix template name.

    Returns:
        Rendered string.
    """
    return value.replace(
        "{TEMPLATE}",
        template_name,
    )


def _normalize_expression(
    expression: str,
) -> str:
    """Normalize a trigger expression for comparison.

    Args:
        expression: Trigger expression.

    Returns:
        Expression without insignificant whitespace.
    """
    return re.sub(
        r"\s+",
        "",
        expression,
    )


def _contains_internal_function_ids(
    expression: str,
) -> bool:
    """Check whether Zabbix returned internal function identifiers.

    Args:
        expression: Trigger expression returned by Zabbix.

    Returns:
        True when internal function IDs such as ``{44282}``
        are detected.
    """
    return bool(_FUNCTION_ID_PATTERN.search(expression))


def _build_legacy_names(
    template_name: str,
) -> dict[str, str]:
    """Build mappings from legacy to current trigger descriptions.

    Args:
        template_name: Current Zabbix template name.

    Returns:
        Dictionary mapping old descriptions to current descriptions.
    """
    return {
        legacy_name: _render_template(
            current_name,
            template_name,
        )
        for legacy_name, current_name in LEGACY_TRIGGER_NAMES.items()
    }


def _find_trigger(
    triggers_by_name: dict[str, dict[str, Any]],
    desired_name: str,
    legacy_names: dict[str, str],
) -> dict[str, Any] | None:
    """Find an existing trigger by current or legacy description.

    Args:
        triggers_by_name: Existing triggers indexed by description.
        desired_name: Desired current trigger description.
        legacy_names: Mapping of legacy descriptions.

    Returns:
        Existing trigger dictionary or ``None``.
    """
    current_trigger = triggers_by_name.get(desired_name)

    if current_trigger is not None:
        return current_trigger

    for legacy_name, current_name in legacy_names.items():
        if current_name != desired_name:
            continue

        legacy_trigger = triggers_by_name.get(legacy_name)

        if legacy_trigger is not None:
            return legacy_trigger

    return None


def _expression_changed(
    current_expression: str,
    desired_expression: str,
) -> bool:
    """Determine whether a trigger expression must be updated.

    Zabbix may return internal function IDs instead of the original
    human-readable expression. In that case, textual comparison is not
    reliable and the expression is considered synchronized.

    Args:
        current_expression: Expression returned by Zabbix.
        desired_expression: Expression defined by PC Guardian.

    Returns:
        True when the expressions are reliably determined to differ.
    """
    if _contains_internal_function_ids(current_expression):
        return False

    return _normalize_expression(current_expression) != _normalize_expression(desired_expression)


def ensure_triggers(
    api: Any,
    template_id: str,
    template_name: str,
) -> tuple[int, int, int]:
    """Create and synchronize Zabbix template triggers.

    Existing triggers are matched by their current description first.
    Legacy trigger descriptions are also detected to avoid duplicates.

    Args:
        api: Authenticated Zabbix API client.
        template_id: Zabbix template identifier.
        template_name: Current Zabbix template name.

    Returns:
        Tuple containing:
            - Total trigger definitions.
            - Number of triggers created.
            - Number of triggers updated.
    """
    existing_triggers = api.call(
        "trigger.get",
        {
            "output": [
                "triggerid",
                "description",
                "expression",
                "priority",
            ],
            "templateids": [
                template_id,
            ],
            "expandExpression": True,
        },
    )

    triggers_by_name: dict[str, dict[str, Any]] = {
        trigger["description"]: trigger for trigger in existing_triggers
    }

    legacy_names = _build_legacy_names(template_name)

    created = 0
    updated = 0

    for (
        description_template,
        expression_template,
        priority,
    ) in TRIGGERS:
        desired_description = _render_template(
            description_template,
            template_name,
        )

        desired_expression = _render_template(
            expression_template,
            template_name,
        )

        existing_trigger = _find_trigger(
            triggers_by_name,
            desired_description,
            legacy_names,
        )

        if existing_trigger is None:
            api.call(
                "trigger.create",
                {
                    "description": desired_description,
                    "expression": desired_expression,
                    "priority": priority,
                },
            )

            created += 1
            continue

        current_description = existing_trigger.get(
            "description",
            "",
        )

        current_expression = existing_trigger.get(
            "expression",
            "",
        )

        current_priority = int(
            existing_trigger.get(
                "priority",
                0,
            )
        )

        description_changed = current_description != desired_description

        priority_changed = current_priority != priority

        expression_changed = _expression_changed(
            current_expression,
            desired_expression,
        )

        if not (description_changed or priority_changed or expression_changed):
            continue

        update_payload: dict[str, Any] = {
            "triggerid": existing_trigger["triggerid"],
            "description": desired_description,
            "priority": priority,
        }

        if expression_changed:
            update_payload["expression"] = desired_expression

        api.call(
            "trigger.update",
            update_payload,
        )

        updated += 1

    return (
        len(TRIGGERS),
        created,
        updated,
    )
