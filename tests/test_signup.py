"""Test suite for signup endpoint functionality using AAA pattern"""


def test_signup_success(client):
    """Test successful signup adds participant to activity
    
    Arrange: Define new student email and activity
    Act: POST signup request with email and activity
    Assert: Verify response success and participant added to activity
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_multiple_students_same_activity(client):
    """Test that multiple students can sign up for the same activity
    
    Arrange: Prepare two different students
    Act: Sign up both students to the same activity
    Assert: Verify both students are in the participants list
    """
    # Arrange
    activity_name = "Programming Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants


def test_signup_duplicate_email_fails(client):
    """Test that signing up with duplicate email returns 400 error
    
    Arrange: Use an email already signed up for activity
    Act: POST signup request with duplicate email
    Assert: Verify 400 status and error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for nonexistent activity returns 404 error
    
    Arrange: Define a non-existent activity name
    Act: POST signup request to non-existent activity
    Assert: Verify 404 status and error message
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_response_message_format(client):
    """Test that signup response contains properly formatted message
    
    Arrange: Define email and activity
    Act: POST signup request
    Assert: Verify message format contains both email and activity name
    """
    # Arrange
    activity_name = "Art Studio"
    email = "testuser@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert activity_name in message
