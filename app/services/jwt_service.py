import jwt
from app.models.user import User
from app.configs.config import settings


class JWTService:
    def __init__(self, user: User):
        self.user = user

    def create_token_by_user(self, additional_payload: dict={})-> str:
        payload = {
            'sub': self.user.id,
            'email': self.user.email,
            'telegram_nickname': self.user.telegram_nickname,
            'phone': self.user.phone,
            'home_address': self.user.home_address,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_staff': self.user.is_staff,
        }
        payload += additional_payload
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        return token

    @staticmethod
    def get_payload_from_token(token: str)-> dict:
        token = token.split(' ')[1]
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
