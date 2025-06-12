from robyn import Robyn
from src.server.routes.user_routes import user_route
from src.database import init as init_db
from tortoise import Tortoise

app = Robyn(__file__)

# Include user routes
app.include_router(user_route)


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
