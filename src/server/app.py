from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.server.routes.routes_user import user_route
from src.server.routes.routes_tasks import tasks_route
from src.database import init as init_db
from tortoise import Tortoise
import logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


# Include user routes
app.include_router(user_route)
app.include_router(tasks_route)


@app.get("/health")
def health():
    return {"status": "ok"}


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logging.info(f"Sending response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)
