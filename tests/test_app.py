from src import app as app_module


def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == app_module.INITIAL_ACTIVITIES


def test_signup_adds_new_participant(client):
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {"message": "Signed up newstudent@mergington.edu for Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "newstudent@mergington.edu" in participants


def test_signup_rejects_duplicate_participant(client):
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_returns_404_for_missing_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_existing_participant(client):
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete("/activities/Chess%20Club/signup?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not signed up for this activity"}