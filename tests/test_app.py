import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    # Assuming "Chess Club" has participants, but to test, maybe use an activity with space
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    # Second should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Chess%20Club/signup?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]