"""Test suite for basic endpoint functionality using AAA pattern"""


def test_get_root_redirect(client):
    """Test that GET / redirects to the static HTML file
    
    Arrange: Prepare the expected redirect URL
    Act: Make GET request to root
    Assert: Verify 307 status and correct location header
    """
    # Arrange
    expected_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_url


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure
    
    Arrange: Define expected activity structure
    Act: Make GET request to /activities
    Assert: Verify response structure and data integrity
    """
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities_data) > 0
    for activity_name, activity_details in activities_data.items():
        assert isinstance(activity_name, str)
        assert set(activity_details.keys()) == expected_keys
        assert isinstance(activity_details["participants"], list)


def test_get_activities_contains_expected_activities(client):
    """Test that GET /activities contains known activities
    
    Arrange: Define list of expected activities
    Act: Fetch activities from API
    Assert: Verify expected activities are present
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class", "Basketball Team"]
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    for activity in expected_activities:
        assert activity in activities_data
