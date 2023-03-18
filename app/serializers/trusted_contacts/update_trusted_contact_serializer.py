from pydantic import BaseModel

class UpdateTrustedContactSerializer(BaseModel):
    name: str | None
    phone: str | None
    email: str | None
    telegram_nickname: str | None
