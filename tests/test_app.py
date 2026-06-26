from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "unregister-test@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
