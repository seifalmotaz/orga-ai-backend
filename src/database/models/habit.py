from tortoise import fields
from datetime import time
from .base import BaseModel
from .enums import Frequency, MessageType


class HabitTemplate(BaseModel):
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    category = fields.CharField(max_length=100, index=True)
    default_frequency = fields.CharEnumField(Frequency)
    default_target_days = fields.JSONField(null=True)
    default_target_count = fields.IntField(default=1)
    default_reminder_time = fields.TimeField(default=time(9, 0))
    icon_name = fields.CharField(max_length=50, null=True)
    color = fields.CharField(max_length=7, default="#4CAF50")
    difficulty_level = fields.IntField(default=1)
    estimated_time_minutes = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True, index=True)
    sort_order = fields.IntField(default=0)

    class Meta:
        table = "habit_templates"
        indexes = [
            ("category", "is_active"),
            ("sort_order",),
            ("name",),
        ]


class HabitTemplateMessage(BaseModel):
    habit_template = fields.ForeignKeyField(
        "models.HabitTemplate", related_name="messages", index=True
    )
    message_type = fields.CharEnumField(MessageType, index=True)
    message_text = fields.TextField()
    is_active = fields.BooleanField(default=True)
    usage_count = fields.IntField(default=0)

    class Meta:
        table = "habit_template_messages"
        indexes = [
            ("habit_template_id", "message_type", "is_active"),
        ]


class Habit(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="habits", index=True)
    template = fields.ForeignKeyField(
        "models.HabitTemplate", null=True, related_name="habits"
    )
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    frequency = fields.CharEnumField(Frequency)
    target_days = fields.JSONField(null=True)
    target_count = fields.IntField(default=1)
    reminder_time = fields.TimeField(null=True)
    is_active = fields.BooleanField(default=True, index=True)

    class Meta:
        table = "habits"
        indexes = [
            ("user_id", "is_active"),
            ("template_id",),
        ]


class HabitCompletion(BaseModel):
    habit = fields.ForeignKeyField(
        "models.Habit", related_name="completions", index=True
    )
    completion_date = fields.DateField(index=True)
    completed_count = fields.IntField(default=1)
    notes = fields.TextField(null=True)

    class Meta:
        table = "habit_completions"
        indexes = [
            ("habit_id", "completion_date"),
            ("completion_date",),
        ]


class HabitStreak(BaseModel):
    habit = fields.ForeignKeyField("models.Habit", related_name="streaks", index=True)
    start_date = fields.DateField()
    end_date = fields.DateField(null=True)
    streak_length = fields.IntField()
    is_current = fields.BooleanField(default=False, index=True)

    class Meta:
        table = "habit_streaks"
        indexes = [
            ("habit_id", "is_current"),
            ("habit_id", "start_date"),
        ]
