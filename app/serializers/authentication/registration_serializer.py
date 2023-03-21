from datetime import datetime
from pydantic import BaseModel

class RegistrationSerializer(BaseModel):
    phone: str
    email: str
    first_name: str
    last_name: str
    telegram_nickname: str
    home_address: str
    password: str
    birth_date: datetime
    gender: str
