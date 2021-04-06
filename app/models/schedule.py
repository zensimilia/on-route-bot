from peewee import BlobField, BooleanField, ForeignKeyField

from .base import BaseModel
from .route import Route


class Schedule(BaseModel):
    """Schedule model class."""

    route = ForeignKeyField(Route, backref='schedules')
    schedule = BlobField(null=False)
    is_active = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'schedules'
