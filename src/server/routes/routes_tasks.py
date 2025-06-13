from fastapi import APIRouter


tasks_route = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_route.get("/")
async def get_tasks():
    return {"message": "Hello, World!"}
