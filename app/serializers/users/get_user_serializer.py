from datetime import datetime
from pydantic import BaseModel

class GetUserSerializer(BaseModel):
    id: int
    phone: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    telegram_nickname: str | None
    home_address: str | None
    birth_date: datetime | None
    gender: str | None
