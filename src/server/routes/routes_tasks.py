from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from uuid import UUID
import math

from src.database.models import User
from src.server.middleware.auth import get_current_user
from src.server.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskPatch,
    TaskResponse,
    TaskListResponse,
    TaskDeleteResponse,
    TaskListQueryParams,
)
from src.server.services.task_service import TaskService
from src.database.models.enums import TaskStatus, Priority


tasks_route = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_to_response(task) -> TaskResponse:
    """Convert a Task model instance to TaskResponse."""
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        due_time=task.due_time,
        status=task.status,
        priority=task.priority,
        completion_percentage=task.completion_percentage,
        estimated_duration=task.estimated_duration,
        actual_duration=task.actual_duration,
        parent_task_id=task.parent_task_id,
        category_id=task.category_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
    )


@tasks_route.get("/", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
async def get_tasks(
    # Query parameters for filtering
    status_filter: Optional[TaskStatus] = Query(
        None, alias="status", description="Filter by task status"
    ),
    priority_filter: Optional[Priority] = Query(
        None, alias="priority", description="Filter by priority"
    ),
    due_date_from: Optional[str] = Query(
        None, description="Filter tasks due from this date (YYYY-MM-DD)"
    ),
    due_date_to: Optional[str] = Query(
        None, description="Filter tasks due until this date (YYYY-MM-DD)"
    ),
    parent_task_id: Optional[UUID] = Query(
        None, description="Filter by parent task ID"
    ),
    category_id: Optional[UUID] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    # Pagination parameters
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    # Sorting parameters
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    # Authentication
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all tasks for the authenticated user with optional filtering, pagination, and sorting.

    **Query Parameters:**
    - **status**: Filter by task status (pending, in_progress, completed, cancelled)
    - **priority**: Filter by priority (0=none, 1=low, 2=medium, 3=high, 4=urgent)
    - **due_date_from**: Filter tasks due from this date (YYYY-MM-DD format)
    - **due_date_to**: Filter tasks due until this date (YYYY-MM-DD format)
    - **parent_task_id**: Filter by parent task ID (for subtasks)
    - **category_id**: Filter by category ID
    - **search**: Search in title and description
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **sort_by**: Field to sort by (created_at, updated_at, title, due_date, priority, status, completion_percentage)
    - **sort_order**: Sort order (asc or desc, default: desc)
    """
    # Create query parameters object
    query_params = TaskListQueryParams(
        status=status_filter,
        priority=priority_filter,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        parent_task_id=parent_task_id,
        category_id=category_id,
        search=search,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    # Get tasks from service
    tasks, total_count = await TaskService.list_tasks(current_user, query_params)

    # Convert to response format
    task_responses = [_task_to_response(task) for task in tasks]

    # Calculate pagination info
    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1

    return TaskListResponse(
        tasks=task_responses,
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@tasks_route.get(
    "/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def get_task_by_id(task_id: UUID, current_user: User = Depends(get_current_user)):
    """
    Retrieve a specific task by ID.

    **Path Parameters:**
    - **task_id**: UUID of the task to retrieve

    **Returns:**
    - Task details if found and belongs to the authenticated user

    **Errors:**
    - 404: Task not found or doesn't belong to user
    - 401: Unauthorized (invalid or missing token)
    """
    task = await TaskService.get_task_by_id(current_user, task_id)
    return _task_to_response(task)


@tasks_route.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate, current_user: User = Depends(get_current_user)
):
    """
    Create a new task.

    **Request Body:**
    - Task data following the TaskCreate schema

    **Returns:**
    - Created task details

    **Errors:**
    - 422: Validation error (invalid data)
    - 401: Unauthorized (invalid or missing token)
    - 400: Bad request (e.g., parent task not found)
    """
    task = await TaskService.create_task(current_user, task_data)
    return _task_to_response(task)


@tasks_route.put(
    "/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: UUID, task_data: TaskUpdate, current_user: User = Depends(get_current_user)
):
    """
    Update an existing task completely (PUT).

    **Path Parameters:**
    - **task_id**: UUID of the task to update

    **Request Body:**
    - Task data following the TaskUpdate schema
    - At least one field must be provided

    **Returns:**
    - Updated task details

    **Errors:**
    - 404: Task not found or doesn't belong to user
    - 422: Validation error (invalid data)
    - 401: Unauthorized (invalid or missing token)
    - 400: Bad request (e.g., parent task not found)
    """
    task = await TaskService.update_task(current_user, task_id, task_data)
    return _task_to_response(task)


@tasks_route.patch(
    "/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def patch_task(
    task_id: UUID, task_data: TaskPatch, current_user: User = Depends(get_current_user)
):
    """
    Partially update an existing task (PATCH).

    **Path Parameters:**
    - **task_id**: UUID of the task to update

    **Request Body:**
    - Task data following the TaskPatch schema
    - Only provided fields will be updated

    **Returns:**
    - Updated task details

    **Errors:**
    - 404: Task not found or doesn't belong to user
    - 422: Validation error (invalid data)
    - 401: Unauthorized (invalid or missing token)
    - 400: Bad request (e.g., parent task not found)
    """
    task = await TaskService.patch_task(current_user, task_id, task_data)
    return _task_to_response(task)


@tasks_route.delete(
    "/{task_id}", response_model=TaskDeleteResponse, status_code=status.HTTP_200_OK
)
async def delete_task(task_id: UUID, current_user: User = Depends(get_current_user)):
    """
    Delete a task (soft delete).

    **Path Parameters:**
    - **task_id**: UUID of the task to delete

    **Returns:**
    - Confirmation message with deleted task ID

    **Errors:**
    - 404: Task not found or doesn't belong to user
    - 401: Unauthorized (invalid or missing token)

    **Note:**
    - This performs a soft delete (sets deleted_at timestamp)
    - The task will no longer appear in list/get operations
    - Related subtasks are not automatically deleted
    """
    task = await TaskService.delete_task(current_user, task_id)

    return TaskDeleteResponse(
        message="Task deleted successfully", deleted_task_id=task.id
    )
