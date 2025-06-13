from robyn import Robyn
from src.server.routes.routes_user import user_route
from src.server.routes.routes_tasks import tasks_route
from src.database import init as init_db
from tortoise import Tortoise
from robyn import Response
import logging

app = Robyn(__file__)


# Include user routes
app.include_router(user_route)
app.include_router(tasks_route)


@app.startup_handler
async def startup():
    """Initialize database on startup."""
    await init_db()


@app.shutdown_handler
async def shutdown():
    """Close database connections on shutdown."""
    await Tortoise.close_connections()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.after_request()
async def log_response(response: Response):
    logging.info(f"Sending response: %s", response)
    return response
