import ormar
from app.models.user import User
from typing import Optional, Union
from app.core.base_meta import BaseMeta

class TrustedContact(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'trusted_contacts'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255, nullable=False)
    phone: str = ormar.String(max_length=20, nullable=False)
    email: str = ormar.String(max_length=20, nullable=True)
    telegram_nickname: str = ormar.String(max_length=20, nullable=True)
    user: Optional[Union[User, dict]] = ormar.ForeignKey(User, related_name="trusted_contacts", ondelete="RESTRICT")
