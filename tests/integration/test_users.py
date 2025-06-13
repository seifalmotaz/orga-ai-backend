def test_get_users(client):
    """Test getting all users - should return empty list initially."""
    response = client.get("/users/")
    assert response.status_code == 200

    # Parse JSON response
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 0


def test_get_user_by_id_not_found(client):
    """Test getting a user by ID that doesn't exist."""
    response = client.get("/users/1")
    assert response.status_code == 404

    # FastAPI returns JSON error messages
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()
