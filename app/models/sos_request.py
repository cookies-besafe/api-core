import ormar
from datetime import datetime
from app.models.user import User
from typing import Optional, Union
from app.core.base_meta import BaseMeta

class SosRequest(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'sos_requests'

    id: int = ormar.Integer(primary_key=True)
    is_active: bool = ormar.Boolean(default=True)
    user: Optional[Union[User, dict]] = ormar.ForeignKey(User, related_name="sos_requests", ondelete="RESTRICT")
    created_at: datetime = ormar.DateTime(timezone=True, default=datetime.now())
