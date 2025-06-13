from datetime import date, time, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from src.database.models.enums import TaskStatus, Priority


class TaskBase(BaseModel):
    """Base task schema with common fields."""

    title: str = Field(..., min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    due_date: Optional[date] = Field(None, description="Due date for the task")
    # due_time: Optional[time] = Field(None, description="Due time for the task")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Task status")
    priority: Priority = Field(Priority.LOW, description="Task priority")
    completion_percentage: int = Field(
        0, ge=0, le=100, description="Completion percentage"
    )
    estimated_duration: Optional[int] = Field(
        None, ge=0, description="Estimated duration in minutes"
    )
    actual_duration: Optional[int] = Field(
        None, ge=0, description="Actual duration in minutes"
    )
    parent_task_id: Optional[UUID] = Field(
        None, description="Parent task ID for subtasks"
    )
    category_id: Optional[UUID] = Field(None, description="Category ID")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (PUT - all fields optional but at least one required)."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)
    estimated_duration: Optional[int] = Field(None, ge=0)
    actual_duration: Optional[int] = Field(None, ge=0)
    parent_task_id: Optional[UUID] = None
    category_id: Optional[UUID] = None

    # Note: Validation for at least one field is handled at the service layer


class TaskPatch(BaseModel):
    """Schema for partial task updates (PATCH)."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)
    estimated_duration: Optional[int] = Field(None, ge=0)
    actual_duration: Optional[int] = Field(None, ge=0)
    parent_task_id: Optional[UUID] = None
    category_id: Optional[UUID] = None


class TaskResponse(TaskBase):
    """Schema for task responses."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskListQueryParams(BaseModel):
    """Query parameters for listing tasks."""

    status: Optional[TaskStatus] = Field(None, description="Filter by task status")
    priority: Optional[Priority] = Field(None, description="Filter by priority")
    due_date_from: Optional[date] = Field(
        None, description="Filter tasks due from this date"
    )
    due_date_to: Optional[date] = Field(
        None, description="Filter tasks due until this date"
    )
    parent_task_id: Optional[UUID] = Field(None, description="Filter by parent task ID")
    category_id: Optional[UUID] = Field(None, description="Filter by category ID")
    search: Optional[str] = Field(
        None, min_length=1, description="Search in title and description"
    )

    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")

    # Sorting
    sort_by: str = Field("created_at", description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")

    @field_validator("sort_by")
    @classmethod
    def validate_sort_field(cls, v):
        """Validate sort field."""
        allowed_fields = [
            "created_at",
            "updated_at",
            "title",
            "due_date",
            "priority",
            "status",
            "completion_percentage",
        ]
        if v not in allowed_fields:
            raise ValueError(f"sort_by must be one of: {', '.join(allowed_fields)}")
        return v


class TaskListResponse(BaseModel):
    """Response schema for task list with pagination."""

    tasks: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskDeleteResponse(BaseModel):
    """Response schema for task deletion."""

    message: str
    deleted_task_id: UUID
