import os
import pytest
from fastapi.testclient import TestClient
from src.server.app import app
from tortoise import Tortoise


@pytest.fixture
def client():
    """Create a test client for FastAPI."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    await Tortoise.close_connections()
