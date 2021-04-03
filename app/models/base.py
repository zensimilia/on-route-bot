from peewee import Model, AutoField, TimestampField, SqliteDatabase
from app.config import Config

db = SqliteDatabase(Config.DB_FILE)


class BaseModel(Model):
    """Custom base class for all models."""

    id = AutoField()
    timestamp = TimestampField()

    class Meta:
        database = db
