from datetime import datetime
from pydantic import BaseModel

class GetUserSerializer(BaseModel):
    id: int
    phone: str
    email: str
    first_name: str
    last_name: str
    telegram_nickname: str
    home_address: str
    birth_date: datetime
    gender: str
