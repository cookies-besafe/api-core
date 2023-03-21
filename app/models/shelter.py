import ormar
from datetime import datetime
from app.models.user import User
from typing import Optional, Union
from app.core.base_meta import BaseMeta

class Shelter(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'shelters'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=255, nullable=False)
    address: str = ormar.String(max_length=500, nullable=False)
    phone: str = ormar.String(max_length=50, nullable=False)
    