"""Zabbix provisioning orchestrator for PC Guardian Ubuntu.

The provisioner manages reusable monitoring objects only: Host Group,
Template Group, Template, Items, Triggers, and Graphs. It never creates,
links, modifies, or deletes Zabbix hosts, and it never creates Zabbix Actions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config import load_config  # noqa: E402
from core.logger import setup_logger  # noqa: E402
from zabbix.provisioning.api import ZabbixAPI  # noqa: E402
from zabbix.provisioning.create_graphs import ensure_graphs  # noqa: E402
from zabbix.provisioning.create_hostgroup import ensure_hostgroup  # noqa: E402
from zabbix.provisioning.create_items import ensure_items  # noqa: E402
from zabbix.provisioning.create_template import (  # noqa: E402
    ensure_template,
    ensure_template_group,
)
from zabbix.provisioning.create_triggers import ensure_triggers  # noqa: E402


def validate_api_config(api_config: dict[str, Any]) -> None:
    """Validate required Zabbix API settings before provisioning."""
    if not api_config.get("enabled", False):
        raise RuntimeError("Zabbix API está deshabilitada: zabbix.api.enabled=false")

    required_parameters = (
        "url",
        "token",
        "host_group",
        "template_group",
        "template_name",
    )
    placeholders = {"CHANGE_ME", "YOUR_TOKEN", "TOJEN"}

    for parameter in required_parameters:
        value = str(api_config.get(parameter, "")).strip()
        if value and value not in placeholders:
            continue
        raise RuntimeError(f"No se ha configurado zabbix.api.{parameter}")


def _log_object_state(
    logger: Any,
    object_name: str,
    display_name: str,
    object_id: str,
    created: bool,
) -> None:
    """Log whether a Zabbix provisioning object was created or reused."""
    if created:
        logger.success(
            "%s creado: %s | id=%s",
            object_name,
            display_name,
            object_id,
        )
    else:
        logger.info(
            "%s existente: %s | id=%s",
            object_name,
            display_name,
            object_id,
        )


def main() -> None:
    """Provision reusable Ubuntu Desktop monitoring objects in Zabbix."""
    config = load_config()
    logger = setup_logger(config)
    logger.info("Iniciando aprovisionamiento Zabbix")

    try:
        api_config = config.get("zabbix", {}).get("api", {})
        validate_api_config(api_config)

        logger.info("Conectando con Zabbix API: %s", api_config["url"])
        api = ZabbixAPI(
            url=api_config["url"],
            token=api_config["token"],
            verify_tls=bool(api_config.get("verify_tls", True)),
        )
        logger.success(
            "Conexión con Zabbix API establecida | versión=%s",
            api.version(),
        )

        logger.info("Verificando Host Group: %s", api_config["host_group"])
        host_group_id, created = ensure_hostgroup(
            api,
            api_config["host_group"],
        )
        _log_object_state(
            logger,
            "Host Group",
            api_config["host_group"],
            host_group_id,
            created,
        )

        logger.info(
            "Verificando Template Group: %s",
            api_config["template_group"],
        )
        template_group_id, created = ensure_template_group(
            api,
            api_config["template_group"],
        )
        _log_object_state(
            logger,
            "Template Group",
            api_config["template_group"],
            template_group_id,
            created,
        )

        logger.info("Verificando Template: %s", api_config["template_name"])
        template_id, created = ensure_template(
            api,
            api_config["template_name"],
            template_group_id,
        )
        _log_object_state(
            logger,
            "Template",
            api_config["template_name"],
            template_id,
            created,
        )

        logger.info("Verificando Items del Template...")
        total_items, created_items, updated_items = ensure_items(
            api,
            template_id,
            config.get("watchlist", []),
        )
        existing_items = total_items - created_items - updated_items
        logger.info(
            "Items verificados | definidos=%d | creados=%d | actualizados=%d | existentes=%d",
            total_items,
            created_items,
            updated_items,
            existing_items,
        )

        logger.info("Verificando Triggers del Template...")
        total_triggers, created_triggers, updated_triggers = ensure_triggers(
            api,
            template_id,
            api_config["template_name"],
        )
        existing_triggers = total_triggers - created_triggers - updated_triggers
        logger.info(
            "Triggers verificados | definidos=%d | creados=%d | actualizados=%d | existentes=%d",
            total_triggers,
            created_triggers,
            updated_triggers,
            existing_triggers,
        )

        logger.info("Verificando Graphs del Template...")
        total_graphs, created_graphs = ensure_graphs(api, template_id)
        logger.info(
            "Graphs verificados | definidos=%d | creados=%d | existentes=%d",
            total_graphs,
            created_graphs,
            total_graphs - created_graphs,
        )

        logger.success("Aprovisionamiento Zabbix completado correctamente")
        logger.info("Host Group disponible: %s", api_config["host_group"])
        logger.info(
            "Template Group disponible: %s",
            api_config["template_group"],
        )
        logger.info("Template disponible: %s", api_config["template_name"])
        logger.info("Items disponibles: %d", total_items)
        logger.info("Triggers disponibles: %d", total_triggers)
        logger.info("Graphs disponibles: %d", total_graphs)
        logger.info("Los hosts deberán crearse manualmente en Zabbix")
        logger.info(
            "Para cada host seleccionar Host Group '%s' y Template '%s'",
            api_config["host_group"],
            api_config["template_name"],
        )
    except KeyboardInterrupt:
        logger.warning("Aprovisionamiento Zabbix interrumpido por el usuario")
        raise SystemExit(130) from None
    except Exception:
        logger.exception("Error durante el aprovisionamiento Zabbix")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
