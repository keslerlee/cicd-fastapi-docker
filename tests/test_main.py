from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "UP"
    assert "uptime_seconds" in json_data

def test_validate_payload_valid():
    payload = {"batch_id": "BATCH-001", "record_count": 150, "status": "active"}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    assert response.json()["is_valid_status"] is True
    assert response.json()["processed_records"] == 150

def test_validate_payload_invalid_count():
    payload = {"batch_id": "BATCH-002", "record_count": -5, "status": "active"}
    response = client.post("/validate", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "record_count cannot be negative"