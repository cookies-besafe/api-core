from pydantic import BaseModel

class BulkUpdateTrustedContactSerializer(BaseModel):
    id: int
    name: str | None
    phone: str | None
    email: str | None
    telegram_nickname: str | None
