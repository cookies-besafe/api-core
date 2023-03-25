from datetime import datetime
from pydantic import BaseModel
from app.serializers.users.get_user_serializer import GetUserSerializer

class GetPostSerializer(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user: GetUserSerializer
