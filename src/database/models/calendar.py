from tortoise import fields
from .base import BaseModel
from .enums import Frequency


class RecurrencePattern(BaseModel):
    frequency = fields.CharEnumField(Frequency)
    interval_value = fields.IntField(default=1)
    days_of_week = fields.JSONField(null=True)
    day_of_month = fields.IntField(null=True)
    month_of_year = fields.IntField(null=True)
    end_type = fields.CharField(max_length=20, default="never")
    end_count = fields.IntField(null=True)
    end_date = fields.DateField(null=True)

    class Meta:
        table = "recurrence_patterns"
