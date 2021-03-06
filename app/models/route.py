from peewee import CharField, ForeignKeyField, BooleanField
from .base import BaseModel
from .user import User


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
