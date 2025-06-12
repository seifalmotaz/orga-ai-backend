from tortoise import fields
from .base import BaseModel
from .enums import NotificationType, DeviceType


class User(BaseModel):
    clerk_id = fields.CharField(max_length=255, unique=True, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    username = fields.CharField(max_length=100, null=True)
    timezone = fields.CharField(max_length=50, default="UTC")
    default_reminder_minutes = fields.IntField(default=15)
    preferred_notification_type = fields.CharEnumField(
        NotificationType, default=NotificationType.PUSH
    )
    # calendars: fields.ReverseRelation["Calendar"]
    # tasks: fields.ReverseRelation["Task"]
    # habits: fields.ReverseRelation["Habit"]
    # devices: fields.ReverseRelation["UserDevice"]

    class Meta:
        table = "users"
        indexes = [("email"), ("clerk_id")]


class UserDevice(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="devices", index=True)
    device_type = fields.CharEnumField(DeviceType)
    push_token = fields.TextField(null=True)
    endpoint_url = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "user_devices"
        indexes = [("user_id", "is_active"), ("device_type",)]
