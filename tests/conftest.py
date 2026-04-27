import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to known state before each test"""
    from src import app as app_module
    
    app_module.activities = {
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
        "Soccer Team": {
            "description": "Practice teamwork and compete against other schools in soccer",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["laura@mergington.edu", "david@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and lap practice for all levels",
            "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
            "max_participants": 18,
            "participants": ["nina@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["chloe@mergington.edu", "jack@mergington.edu"]
        },
        "Drama Club": {
            "description": "Rehearse scenes, practice acting, and prepare stage performances",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "matthew@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science challenges and build hands-on projects",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["zoe@mergington.edu", "brandon@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking through debate",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["sarah@mergington.edu", "alex@mergington.edu"]
        }
    }
    yield
