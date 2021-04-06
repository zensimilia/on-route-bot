from peewee import AutoField, SqliteDatabase, TimestampField
from playhouse.signals import Model

from app.config import Config

db = SqliteDatabase(Config.DB_FILE)


class BaseModel(Model):
    """Custom base class for all models."""

    id = AutoField()
    timestamp = TimestampField()

    class Meta:
        database = db
