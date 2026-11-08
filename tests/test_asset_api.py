from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_local_asset_endpoint_returns_success():
    response = client.get("/api/v1/assets/local")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_local_asset_endpoint_returns_asset_information():
    response = client.get("/api/v1/assets/local")

    asset = response.json()["asset"]

    required_fields = [
        "hostname",
        "operating_system",
        "os_release",
        "os_version",
        "architecture",
        "processor",
        "cpu_logical_cores",
        "memory_total_bytes",
        "memory_available_bytes",
        "network_interfaces",
        "disks",
        "collection_timestamp",
    ]

    for field in required_fields:
        assert field in asset


def test_local_asset_endpoint_returns_valid_memory_information():
    response = client.get("/api/v1/assets/local")
    asset = response.json()["asset"]

    assert asset["memory_total_bytes"] > 0
    assert asset["memory_available_bytes"] >= 0
    assert (
        asset["memory_available_bytes"]
        <= asset["memory_total_bytes"]
    )


def test_local_asset_endpoint_returns_valid_network_interfaces():
    response = client.get("/api/v1/assets/local")
    asset = response.json()["asset"]

    assert isinstance(asset["network_interfaces"], list)

    for interface in asset["network_interfaces"]:
        assert isinstance(interface["name"], str)
        assert isinstance(interface["ip_addresses"], list)
        assert isinstance(interface["is_up"], (bool, type(None)))


def test_local_asset_endpoint_returns_valid_disk_information():
    response = client.get("/api/v1/assets/local")
    asset = response.json()["asset"]

    assert isinstance(asset["disks"], list)

    for disk in asset["disks"]:
        assert disk["total_bytes"] > 0
        assert disk["used_bytes"] >= 0
        assert disk["free_bytes"] >= 0
        assert (
            disk["used_bytes"] + disk["free_bytes"]
            <= disk["total_bytes"]
        )