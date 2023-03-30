import ormar
from datetime import datetime
from app.models.user import User
from typing import Optional, Union
from app.core.base_meta import BaseMeta

class Post(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'posts'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=255, nullable=False)
    content: str = ormar.Text(nullable=False)
    created_at: datetime = ormar.DateTime(timezone=True, default=datetime.now)
    user: Optional[Union[User, dict]] = ormar.ForeignKey(User, related_name="posts", ondelete="RESTRICT")
