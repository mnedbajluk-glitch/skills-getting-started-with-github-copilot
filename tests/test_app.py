"""Tests for the Mergington High School Activities API"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_contains_correct_structure(self, client):
        """Test that activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_contains_participants(self, client):
        """Test that activities contain the initial participants"""
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds participant to activity"""
        new_email = "newstudent@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={new_email}")
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert new_email in data["Chess Club"]["participants"]

    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """Test that signup to non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered_returns_400(self, client):
        """Test that duplicate signup returns 400"""
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_with_different_case_email(self, client):
        """Test signup with different case email (case-sensitive)"""
        response = client.post(
            "/activities/Chess Club/signup?email=NewStudent@mergington.edu"
        )
        
        assert response.status_code == 200
        
        # Verify it's treated as different email
        response2 = client.post(
            "/activities/Chess Club/signup?email=NewStudent@mergington.edu"
        )
        assert response2.status_code == 400

    def test_signup_to_activity_at_capacity(self, client):
        """Test signup to activity when there are available spots"""
        # Gym Class has 30 spots, 2 participants, so should have 28 spots available
        response = client.post(
            "/activities/Gym Class/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200


class TestUnregister:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client):
        """Test successful unregistration from activity"""
        response = client.post(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes participant"""
        client.post(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test unregister from non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered_returns_400(self, client):
        """Test unregister when student is not registered returns 400"""
        response = client.post(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_after_signup(self, client):
        """Test full signup then unregister flow"""
        email = "testflow@mergington.edu"
        
        # Sign up
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        # Verify signup
        response2 = client.get("/activities")
        assert email in response2.json()["Chess Club"]["participants"]
        
        # Unregister
        response3 = client.post(f"/activities/Chess Club/unregister?email={email}")
        assert response3.status_code == 200
        
        # Verify unregister
        response4 = client.get("/activities")
        assert email not in response4.json()["Chess Club"]["participants"]


class TestRoot:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
