from peewee import CharField, BitField
from .base import BaseModel


class User(BaseModel):
    """
    User model class.
    """
    username = CharField(null=False)
    uid = BitField(unique=True, null=False, index=True)
    timezone = CharField(null=True)

    class Meta:
        table_name = 'users'
