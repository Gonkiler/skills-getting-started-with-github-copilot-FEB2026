import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store original activities data for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and school games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Join our orchestra and string ensemble for performances",
        "schedule": "Thursdays, 3:45 PM - 5:15 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills in competitive debate",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 10,
        "participants": ["nathan@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore physics, chemistry, and biology through hands-on experiments",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Fixture that provides a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Automatically reset activities to original state before each test"""
    # Store original state before test
    original = copy.deepcopy(activities)
    yield
    # Restore original state after test
    activities.clear()
    activities.update(original)
