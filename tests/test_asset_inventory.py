
from datetime import datetime

from backend.asset_inventory import collect_local_asset


def test_local_asset_has_required_fields():
    asset = collect_local_asset()

    required_fields = [
        "hostname",
        "operating_system",
        "os_release",
        "os_version",
        "architecture",
        "cpu_logical_cores",
        "memory_total_bytes",
        "memory_available_bytes",
        "network_interfaces",
        "disks",
        "collection_timestamp",
    ]

    for field in required_fields:
        assert field in asset


def test_hostname_is_not_empty():
    asset = collect_local_asset()

    assert isinstance(asset["hostname"], str)
    assert asset["hostname"]


def test_operating_system_is_detected():
    asset = collect_local_asset()

    assert asset["operating_system"] in [
        "Windows",
        "Linux",
        "Darwin",
    ]


def test_memory_values_are_valid():
    asset = collect_local_asset()

    assert asset["memory_total_bytes"] > 0

    assert (
        0 <= asset["memory_available_bytes"]
        <= asset["memory_total_bytes"]
    )


def test_cpu_count_is_valid():
    asset = collect_local_asset()

    assert asset["cpu_logical_cores"] is None or (
        asset["cpu_logical_cores"] > 0
    )


def test_collection_timestamp_is_valid():
    asset = collect_local_asset()

    timestamp = datetime.fromisoformat(
        asset["collection_timestamp"]
    )

    assert timestamp.tzinfo is not None


def test_network_interfaces_have_valid_structure():
    asset = collect_local_asset()

    assert isinstance(asset["network_interfaces"], list)

    for interface in asset["network_interfaces"]:
        assert "name" in interface
        assert "ip_addresses" in interface
        assert isinstance(interface["ip_addresses"], list)


def test_disk_inventory_has_valid_structure():
    asset = collect_local_asset()

    assert isinstance(asset["disks"], list)

    for disk in asset["disks"]:
        assert disk["total_bytes"] >= 0
        assert disk["used_bytes"] >= 0
        assert disk["free_bytes"] >= 0