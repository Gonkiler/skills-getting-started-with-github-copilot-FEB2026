"""Test suite for unregister endpoint functionality using AAA pattern"""


def test_unregister_success(client):
    """Test successful unregister removes participant from activity
    
    Arrange: Use a student already signed up for activity
    Act: POST unregister request with email and activity
    Assert: Verify response success and participant removed from activity
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_multiple_participants(client):
    """Test that unregistering one participant doesn't affect others
    
    Arrange: Activity with multiple participants
    Act: Unregister one participant
    Assert: Verify only that participant was removed, others remain
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants


def test_unregister_not_signed_up_fails(client):
    """Test that unregistering someone not signed up returns 400 error
    
    Arrange: Use email not currently signed up
    Act: POST unregister request with non-participant email
    Assert: Verify 400 status and error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"  # Not signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from nonexistent activity returns 404 error
    
    Arrange: Define non-existent activity name
    Act: POST unregister request to non-existent activity
    Assert: Verify 404 status and error message
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_response_message_format(client):
    """Test that unregister response contains properly formatted message
    
    Arrange: Define email and activity with existing participant
    Act: POST unregister request
    Assert: Verify message format contains both email and activity name
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert activity_name in message


def test_signup_then_unregister_cycle(client):
    """Test signup followed by unregister in same session
    
    Arrange: Fresh activity state
    Act: Sign up new student, then unregister them
    Assert: Verify student is added then removed correctly
    """
    # Arrange
    activity_name = "Debate Team"
    email = "cycletest@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Signup successful
    assert signup_response.status_code == 200
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
    
    # Act - Unregister
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert - Unregister successful
    assert unregister_response.status_code == 200
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]
