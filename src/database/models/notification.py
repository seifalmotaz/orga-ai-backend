from tortoise import fields
from .base import BaseModel
from .enums import NotificationType, NotificationStatus, MessageType


class NotificationQueue(BaseModel):
    user = fields.ForeignKeyField(
        "models.User", related_name="notifications", db_index=True
    )
    task = fields.ForeignKeyField("models.Task", null=True, db_index=True)
    habit = fields.ForeignKeyField("models.Habit", null=True, db_index=True)
    task_reminder = fields.ForeignKeyField("models.TaskReminder", null=True)
    scheduled_time = fields.DatetimeField(db_index=True)
    notification_type = fields.CharEnumField(NotificationType)
    status = fields.CharEnumField(
        NotificationStatus, default=NotificationStatus.PENDING, db_index=True
    )
    custom_message = fields.TextField(null=True)
    message_type = fields.CharEnumField(MessageType, null=True)
    retry_count = fields.IntField(default=0)
    error_message = fields.TextField(null=True)
    sent_at = fields.DatetimeField(null=True)

    class Meta:
        table = "notification_queue"
        indexes = [
            ("scheduled_time", "status"),
            ("user_id", "status"),
            ("status", "retry_count"),
            ("task_id",),
            ("habit_id",),
        ]
