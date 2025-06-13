from typing import List, Tuple
from uuid import UUID
from datetime import datetime
from tortoise.expressions import Q
from src.database.models import Task, User
from src.server.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskPatch,
    TaskListQueryParams,
)
from src.server.utils.responses import TaskNotFoundError, ValidationError


class TaskService:
    """Service layer for task operations."""

    @staticmethod
    async def create_task(user: User, task_data: TaskCreate) -> Task:
        """Create a new task for the user."""
        # Validate parent task exists and belongs to user if specified
        if task_data.parent_task_id:
            parent_task = await Task.filter(
                id=task_data.parent_task_id, user=user, deleted_at__isnull=True
            ).first()
            if not parent_task:
                raise ValidationError(
                    "Parent task not found or does not belong to user",
                    {"parent_task_id": str(task_data.parent_task_id)},
                )

        # Create task
        task = await Task.create(user=user, **task_data.model_dump(exclude_unset=True))

        # Load related fields for response
        await task.fetch_related("user", "parent_task", "category")
        return task

    @staticmethod
    async def get_task_by_id(user: User, task_id: UUID) -> Task:
        """Get a specific task by ID for the user."""
        task = (
            await Task.filter(id=task_id, user=user, deleted_at__isnull=True)
            .prefetch_related("user", "parent_task", "category")
            .first()
        )

        if not task:
            raise TaskNotFoundError(str(task_id))

        return task

    @staticmethod
    async def update_task(user: User, task_id: UUID, task_data: TaskUpdate) -> Task:
        """Update a task completely."""
        task = await TaskService.get_task_by_id(user, task_id)

        # Validate parent task if being updated
        if task_data.parent_task_id is not None:
            if task_data.parent_task_id == task_id:
                raise ValidationError("Task cannot be its own parent")

            if task_data.parent_task_id:
                parent_task = await Task.filter(
                    id=task_data.parent_task_id, user=user, deleted_at__isnull=True
                ).first()
                if not parent_task:
                    raise ValidationError(
                        "Parent task not found or does not belong to user",
                        {"parent_task_id": str(task_data.parent_task_id)},
                    )

        # Update task fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Set completion timestamp if status changed to completed
        if (
            task_data.status
            and task_data.status.value == "completed"
            and not task.completed_at
        ):
            task.completed_at = datetime.now()
        elif task_data.status and task_data.status.value != "completed":
            task.completed_at = None

        await task.save()
        await task.fetch_related("user", "parent_task", "category")
        return task

    @staticmethod
    async def patch_task(user: User, task_id: UUID, task_data: TaskPatch) -> Task:
        """Partially update a task."""
        task = await TaskService.get_task_by_id(user, task_id)

        # Validate parent task if being updated
        if task_data.parent_task_id is not None:
            if task_data.parent_task_id == task_id:
                raise ValidationError("Task cannot be its own parent")

            if task_data.parent_task_id:
                parent_task = await Task.filter(
                    id=task_data.parent_task_id, user=user, deleted_at__isnull=True
                ).first()
                if not parent_task:
                    raise ValidationError(
                        "Parent task not found or does not belong to user",
                        {"parent_task_id": str(task_data.parent_task_id)},
                    )

        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True, exclude_none=False)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Handle completion timestamp
        if (
            task_data.status
            and task_data.status.value == "completed"
            and not task.completed_at
        ):
            task.completed_at = datetime.now()
        elif task_data.status and task_data.status.value != "completed":
            task.completed_at = None

        await task.save()
        await task.fetch_related("user", "parent_task", "category")
        return task

    @staticmethod
    async def delete_task(user: User, task_id: UUID) -> Task:
        """Soft delete a task."""
        task = await TaskService.get_task_by_id(user, task_id)
        await task.delete()  # This uses the soft delete from BaseModel
        return task

    @staticmethod
    async def list_tasks(
        user: User, query_params: TaskListQueryParams
    ) -> Tuple[List[Task], int]:
        """List tasks for the user with filtering, pagination, and sorting."""
        # Build base query
        query = Task.filter(user=user, deleted_at__isnull=True)

        # Apply filters
        if query_params.status:
            query = query.filter(status=query_params.status)

        if query_params.priority:
            query = query.filter(priority=query_params.priority)

        if query_params.due_date_from:
            query = query.filter(due_date__gte=query_params.due_date_from)

        if query_params.due_date_to:
            query = query.filter(due_date__lte=query_params.due_date_to)

        if query_params.parent_task_id:
            query = query.filter(parent_task_id=query_params.parent_task_id)

        if query_params.category_id:
            query = query.filter(category_id=query_params.category_id)

        if query_params.search:
            search_term = query_params.search.strip()
            query = query.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term)
            )

        # Get total count before pagination
        total_count = await query.count()

        # Apply sorting
        sort_field = query_params.sort_by
        if query_params.sort_order == "desc":
            sort_field = f"-{sort_field}"

        query = query.order_by(sort_field)

        # Apply pagination
        offset = (query_params.page - 1) * query_params.page_size
        query = query.offset(offset).limit(query_params.page_size)

        # Execute query with related fields
        tasks = await query.prefetch_related("user", "parent_task", "category")

        return tasks, total_count
