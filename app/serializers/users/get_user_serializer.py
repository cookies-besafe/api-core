from pydantic import BaseModel
from app.models.user import User

class GetUserSerializer(BaseModel):
    id: int
    phone: str
    email: str
    first_name: str
    last_name: str
    telegram_nickname: str
    home_address: str
