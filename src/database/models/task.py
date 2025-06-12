from tortoise import fields
from .base import BaseModel
from .enums import TaskStatus, Priority, NotificationType


class Task(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="tasks", index=True)
    title = fields.CharField(max_length=500, index=True)
    description = fields.TextField(null=True)
    due_date = fields.DateField(null=True, index=True)
    due_time = fields.TimeField(null=True)
    status = fields.CharEnumField(TaskStatus, default=TaskStatus.PENDING, index=True)
    priority = fields.IntEnumField(Priority, default=Priority.LOW, index=True)
    completion_percentage = fields.IntField(default=0)
    estimated_duration = fields.IntField(null=True)
    actual_duration = fields.IntField(null=True)
    parent_task = fields.ForeignKeyField(
        "models.Task", null=True, related_name="subtasks"
    )
    category = fields.ForeignKeyField(
        "models.Category", null=True, related_name="tasks"
    )
    recurrence_pattern = fields.ForeignKeyField("models.RecurrencePattern", null=True)
    completed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "tasks"
        indexes = [
            ("user_id", "status"),
            ("due_date", "priority"),
            ("status", "due_date"),
            ("parent_task_id",),
            ("title",),
        ]


class TaskDependency(BaseModel):
    prerequisite_task = fields.ForeignKeyField(
        "models.Task", related_name="dependents", index=True
    )
    dependent_task = fields.ForeignKeyField(
        "models.Task", related_name="prerequisites", index=True
    )

    class Meta:
        table = "task_dependencies"
        indexes = [
            ("prerequisite_task_id",),
            ("dependent_task_id",),
        ]


class TaskTimeLog(BaseModel):
    task = fields.ForeignKeyField("models.Task", related_name="time_logs", index=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)
    duration_minutes = fields.IntField(null=True)
    notes = fields.TextField(null=True)

    class Meta:
        table = "task_time_logs"
        indexes = [("task_id", "start_time")]


class TaskReminder(BaseModel):
    task = fields.ForeignKeyField("models.Task", related_name="reminders", index=True)
    reminder_minutes = fields.IntField()
    notification_type = fields.CharEnumField(NotificationType)
    is_enabled = fields.BooleanField(default=True)

    class Meta:
        table = "task_reminders"
        indexes = [("task_id",)]
