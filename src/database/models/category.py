from tortoise import fields
from .base import BaseModel


class Category(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="categories", index=True)
    name = fields.CharField(max_length=100)
    color = fields.CharField(max_length=7, default="#666666")

    class Meta:
        table = "categories"
        indexes = [("user_id",)]
