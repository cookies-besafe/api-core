import jwt
from app.models.user import User


class JWTService:
    def __init__(self, user: User):
        self.user = user

    def create_token_by_user(self, additional_payload={}):
        payload = {
            'sub': self.user.id,
            'email': self.user.email,
            'telegram_nickname': self.user.telegram_nickname,
            'phone': self.user.phone,
            'home_address': self.user.home_address,
        }
        payload += additional_payload
