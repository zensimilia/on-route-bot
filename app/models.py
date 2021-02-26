from peewee import *
from app.config import Config

db = SqliteDatabase(Config.DB_FILE)


class BaseModel(Model):
    """
    Custom base class for all models.
    """
    id = AutoField()
    timestamp = TimestampField()

    class Meta:
        database = db


class User(BaseModel):
    """
    User model class.
    """
    username = CharField(null=False)
    uid = BitField(unique=True, null=False, index=True)
    timezone = CharField(null=True)

    class Meta:
        table_name = 'users'


class Route(BaseModel):
    """
    Route model class.
    """
    name = CharField(null=False)
    url = CharField(null=False)
    user = ForeignKeyField(User, backref='routes')
    is_active = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'routes'
