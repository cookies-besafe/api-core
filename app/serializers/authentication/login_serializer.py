from pydantic import BaseModel

class LoginSerializer(BaseModel):
    email: str
    password: str
