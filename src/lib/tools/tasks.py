from datetime import date
import os
import httpx
from langchain_core.tools import tool
from src.database.models.enums import Priority, TaskStatus
from src.server.schemas.task_schemas import TaskCreate

from typing import Annotated


def create_client():
    base_url = os.getenv("API")
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNWRmN2MzMzUtYzNlOC00MWY0LWE3NWQtZTgyNzUxMDJkM2QxIn0.xtujKp1QvlI4GrRefMkiHKC83MVh9MI5c1F5HR53_c4",
    }
    return httpx.AsyncClient(base_url=base_url, headers=headers)


@tool
async def get_today_tasks():
    """Get today's tasks."""
    client = create_client()
    due_date_from = date.today().isoformat()
    response = await client.get(
        "/tasks/",
        params={
            "due_date_from": due_date_from,
            "due_date_to": due_date_from,
        },
    )
    return response.json()


@tool
async def create_task(
    title: Annotated[str, "The title of the task"],
    description: Annotated[str, "The description of the task"],
    due_date: Annotated[date, "The due date of the task"],
    due_time: Annotated[str, "The due time of the task"],
    priority: Annotated[Priority, "The priority of the task"],
    completion_percentage: Annotated[int, "The completion percentage of the task"],
    estimated_duration: Annotated[int, "The estimated duration of the task"],
):
    """
    Create a new task/todo item.
    - Need to check the date and time before creating the task.
    - If the date and time are in the past, return an error.
    - If the date and time are in the future, create the task.
    """
    client = create_client()
    response = await client.post(
        "/tasks/",
        json={
            "title": title,
            "description": description,
            "due_date": due_date.isoformat(),
            "due_time": due_time,
            "priority": priority,
            "completion_percentage": completion_percentage,
            "estimated_duration": estimated_duration,
        },
    )
    return response.json()
