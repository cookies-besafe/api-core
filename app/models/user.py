import ormar
from app.core.base_meta import BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    phone: str = ormar.String(max_length=20, unique=True, nullable=False)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    telegram_nickname: str = ormar.String(max_length=255, nullable=True)
    home_address: str = ormar.String(max_length=500, nullable=True)
