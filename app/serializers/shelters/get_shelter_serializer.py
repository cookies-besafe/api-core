from pydantic import BaseModel

class GetShelterSerializer(BaseModel):
    id: int
    address: str
    phone: str
    title: str
