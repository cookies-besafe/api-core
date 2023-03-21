from datetime import datetime
from pydantic import BaseModel

class UpdateProfileSerializer(BaseModel):
    phone: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    telegram_nickname: str | None
    home_address: str | None
    password: str | None
    birth_date: datetime | None
    gender: str | None
