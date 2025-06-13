import pytest
import httpx
import threading
import time
import socket
from src.server.app import app
from tortoise import Tortoise


def is_port_open(host, port):
    """Check if a port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


@pytest.fixture(scope="session")
def test_server():
    """Start a test server in a separate thread for integration testing."""
    port = 8080  # Use the default port that Robyn uses
    host = "127.0.0.1"

    def run_server():
        # Run the Robyn app - it will use its default configuration
        app.start(host=host, port=port)

    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    max_attempts = 30
    for attempt in range(max_attempts):
        if is_port_open(host, port):
            break
        time.sleep(0.5)
    else:
        raise RuntimeError(
            f"Server failed to start on {host}:{port} after {max_attempts * 0.5} seconds"
        )

    # Give it a bit more time to fully initialize
    time.sleep(1)

    yield f"http://{host}:{port}"


@pytest.fixture
async def client(test_server):
    """Create an async HTTP client for testing."""
    base_url = test_server
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    await Tortoise.close_connections()
