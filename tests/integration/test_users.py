import pytest
import json


@pytest.mark.asyncio
async def test_get_users(client):
    """Test getting all users - should return empty list initially."""
    response = await client.get("/users/")
    assert response.status_code == 200

    # Parse JSON response
    users = json.loads(response.text)
    assert isinstance(users, list)
    assert len(users) == 0


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    """Test getting a user by ID that doesn't exist."""
    response = await client.get("/users/1")
    assert response.status_code == 404

    # Robyn returns plain text error messages by default
    assert "not found" in response.text.lower()
