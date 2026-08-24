"""Zabbix template-definition consistency tests."""

from zabbix.provisioning.create_graphs import GRAPH_DEFINITIONS
from zabbix.provisioning.create_items import build_item_definitions
from zabbix.provisioning.definitions import BASE_ITEMS, TRIGGERS


def test_base_item_units() -> None:
    """Capacity and throughput items use Zabbix base units."""
    units = {key: unit for _, key, _, unit in BASE_ITEMS}
    assert units["pcguardian.memory.available"] == "B"
    assert units["pcguardian.disk.root.free"] == "B"
    assert units["pcguardian.disk.read"] == "Bps"
    assert units["pcguardian.disk.write"] == "Bps"
    assert units["pcguardian.cpu.temperature"] == "°C"
    assert units["pcguardian.psi.memory.avg10"] == "%"


def test_default_template_counts() -> None:
    """Default provisioning defines 32 items, 12 triggers, and 7 graphs."""
    definitions = build_item_definitions(["snapd", "firefox", "gnome-shell", "Xorg"])
    assert len(definitions) == 32
    assert len(TRIGGERS) == 12
    assert len(GRAPH_DEFINITIONS) == 7
