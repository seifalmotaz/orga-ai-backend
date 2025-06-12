from datetime import datetime
from tortoise.models import Model
from tortoise import fields
import uuid


class BaseModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True

    async def delete(self):
        self.deleted_at = datetime.now()
        await self.save()

    async def restore(self):
        self.deleted_at = None
        await self.save()
