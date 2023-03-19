from pydantic import BaseModel
from datetime import datetime
from app.serializers.users.get_user_serializer import GetUserSerializer

class GetSosRequestSerializer(BaseModel):
    id: int
    is_active: bool
    user: GetUserSerializer
    created_at: datetime
