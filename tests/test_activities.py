"""Tests for activity retrieval endpoints"""


def test_get_activities(client, reset_activities):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure(client, reset_activities):
    """Test that activities have correct structure"""
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_participants_list(client, reset_activities):
    """Test that activities include correct participant list"""
    response = client.get("/activities")
    data = response.json()
    
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


def test_get_activities_max_participants(client, reset_activities):
    """Test that max_participants values are correct"""
    response = client.get("/activities")
    data = response.json()
    
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Programming Class"]["max_participants"] == 20
    assert data["Gym Class"]["max_participants"] == 30
