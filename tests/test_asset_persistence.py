from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_collect_endpoint_saves_local_asset():
    response = client.post("/api/v1/assets/local/collect")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["asset"]["hostname"]
    assert data["asset"]["id"] is not None


def test_saved_assets_endpoint_returns_records():
    client.post("/api/v1/assets/local/collect")

    response = client.get("/api/v1/assets")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["count"] >= 1
    assert isinstance(data["assets"], list)


def test_saved_asset_contains_inventory_information():
    client.post("/api/v1/assets/local/collect")

    response = client.get("/api/v1/assets")
    assets = response.json()["assets"]

    local_asset = next(
        asset
        for asset in assets
        if asset["hostname"]
    )

    assert local_asset["operating_system"]
    assert local_asset["architecture"]
    assert local_asset["memory_total_bytes"] > 0
    assert local_asset["source"] == "local_collector"
    assert local_asset["verification_status"] == "collected"


def test_repeated_collection_does_not_duplicate_local_asset():
    first_response = client.post("/api/v1/assets/local/collect")
    second_response = client.post("/api/v1/assets/local/collect")

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_id = first_response.json()["asset"]["id"]
    second_id = second_response.json()["asset"]["id"]

    assert first_id == second_id