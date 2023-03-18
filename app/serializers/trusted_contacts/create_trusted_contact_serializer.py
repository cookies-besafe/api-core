from pydantic import BaseModel
from app.models.user import User

class CreateTrustedContactSerializer(BaseModel):
    name: str
    phone: str
    email: str | None
    telegram_nickname: str | None
