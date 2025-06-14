from datetime import date
import os
import httpx
from langchain_core.tools import tool
from src.database.models.enums import Priority, TaskStatus

from typing import Annotated, Optional


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
async def get_tasks_filtered(
    due_date_from: Annotated[Optional[date], "The due date from"],
    due_date_to: Annotated[Optional[date], "The due date to"],
    status: Annotated[Optional[TaskStatus], "The status of the task"],
    priority: Annotated[Optional[Priority], "The priority of the task"],
    completion_percentage: Annotated[
        Optional[int], "The completion percentage of the task"
    ],
    estimated_duration: Annotated[Optional[int], "The estimated duration of the task"],
):
    """Get tasks filtered by the given parameters."""
    client = create_client()
    params = {}
    if due_date_from:
        params["due_date_from"] = due_date_from.isoformat()
    if due_date_to:
        params["due_date_to"] = due_date_to.isoformat()
    if status:
        params["status"] = status.value
    if priority:
        params["priority"] = priority.value
    if completion_percentage:
        params["completion_percentage"] = completion_percentage
    if estimated_duration:
        params["estimated_duration"] = estimated_duration
    response = await client.get(
        "/tasks/",
        params=params,
    )
    return response.json()


@tool
async def get_task_by_id(task_id: str):
    """Get a task by its ID."""
    client = create_client()
    response = await client.get(f"/tasks/{task_id}")
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
