from pydantic import BaseModel
from app.serializers.users.get_user_serializer import GetUserSerializer

class GetTrustedContactSerializer(BaseModel):
    id: int
    name: str
    phone: str
    email: str | None
    telegram_nickname: str | None
    user: GetUserSerializer
