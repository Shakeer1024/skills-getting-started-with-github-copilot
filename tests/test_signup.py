"""Tests for signup and unregister endpoints"""


def test_signup_new_participant(client, reset_activities):
    """Test signing up a new participant"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_to_participants(client, reset_activities):
    """Test that signup adds participant to the activity"""
    # Sign up
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    
    # Verify in activities list
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "test@mergington.edu" in participants
    assert len(participants) == 3  # 2 original + 1 new


def test_signup_duplicate_participant(client, reset_activities):
    """Test that duplicate signups are rejected"""
    # First signup
    response1 = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Duplicate signup
    response2 = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_duplicate_existing_participant(client, reset_activities):
    """Test that signing up an already registered participant fails"""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant(client, reset_activities):
    """Test removing a participant from an activity"""
    # First sign up
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    
    # Then unregister
    response = client.delete(
        "/activities/Chess Club/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "test@mergington.edu" in data["message"]
    
    # Verify removed from activities list
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "test@mergington.edu" not in participants


def test_unregister_removes_existing_participant(client, reset_activities):
    """Test unregistering an existing participant"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify removed
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants
    assert len(participants) == 1  # Only daniel left


def test_unregister_not_signed_up(client, reset_activities):
    """Test unregistering a participant who is not signed up"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_multiple_signups_and_unregisters(client, reset_activities):
    """Test multiple signup and unregister operations"""
    # Sign up multiple people
    client.post("/activities/Programming Class/signup?email=user1@mergington.edu")
    client.post("/activities/Programming Class/signup?email=user2@mergington.edu")
    client.post("/activities/Programming Class/signup?email=user3@mergington.edu")
    
    # Check we have 5 participants (2 original + 3 new)
    response = client.get("/activities")
    participants = response.json()["Programming Class"]["participants"]
    assert len(participants) == 5
    
    # Unregister one
    client.delete("/activities/Programming Class/unregister?email=user2@mergington.edu")
    
    # Check we have 4 participants
    response = client.get("/activities")
    participants = response.json()["Programming Class"]["participants"]
    assert len(participants) == 4
    assert "user2@mergington.edu" not in participants
