from tortoise import fields
from .base import BaseModel
from .enums import EventStatus, Priority, NotificationType


class Event(BaseModel):
    calendar = fields.ForeignKeyField(
        "models.Calendar", related_name="events", index=True
    )
    title = fields.CharField(max_length=500, index=True)
    description = fields.TextField(null=True)
    location = fields.CharField(max_length=500, null=True)
    start_datetime = fields.DatetimeField(index=True)
    end_datetime = fields.DatetimeField(index=True)
    is_all_day = fields.BooleanField(default=False)
    recurrence_pattern = fields.ForeignKeyField(
        "models.RecurrencePattern", null=True, related_name="events"
    )
    parent_event = fields.ForeignKeyField(
        "models.Event", null=True, related_name="instances"
    )
    is_recurring_master = fields.BooleanField(default=False, index=True)
    status = fields.CharEnumField(
        EventStatus, default=EventStatus.CONFIRMED, index=True
    )
    priority = fields.IntEnumField(Priority, default=Priority.NONE)

    class Meta:
        table = "events"
        indexes = [
            ("calendar_id",),
            ("start_datetime", "end_datetime"),
            ("status", "start_datetime"),
            ("is_recurring_master",),
            ("title",),
        ]


class EventInstance(BaseModel):
    master_event = fields.ForeignKeyField(
        "models.Event", related_name="computed_instances", index=True
    )
    instance_date = fields.DateField(index=True)
    start_datetime = fields.DatetimeField(index=True)
    end_datetime = fields.DatetimeField(index=True)
    is_exception = fields.BooleanField(default=False)

    class Meta:
        table = "event_instances"
        indexes = [
            ("master_event_id", "instance_date"),
            ("start_datetime", "end_datetime"),
            ("instance_date",),
        ]


class EventException(BaseModel):
    master_event = fields.ForeignKeyField("models.Event", related_name="exceptions")
    exception_date = fields.DateField()
    exception_type = fields.CharField(max_length=20)
    modified_event = fields.ForeignKeyField("models.Event", null=True)

    class Meta:
        table = "event_exceptions"
        indexes = [("master_event_id", "exception_date")]


class EventReminder(BaseModel):
    event = fields.ForeignKeyField("models.Event", related_name="reminders", index=True)
    reminder_minutes = fields.IntField()
    notification_type = fields.CharEnumField(NotificationType)
    is_enabled = fields.BooleanField(default=True)

    class Meta:
        table = "event_reminders"
        indexes = [("event_id",)]


class EventCategoryMapping(BaseModel):
    event = fields.ForeignKeyField("models.Event", related_name="category_mappings")
    category = fields.ForeignKeyField("models.Category", related_name="events")

    class Meta:
        table = "event_category_mappings"
        indexes = [("event_id",), ("category_id",)]
