import jwt
import datetime
from app.models.user import User
from app.configs.config import settings
from fastapi import HTTPException


class JWTService:
    @staticmethod
    def create_token_by_user(user, additional_payload: dict={})-> str:
        payload = {
            'sub': user.id,
            'email': user.email,
            'telegram_nickname': user.telegram_nickname,
            'phone': user.phone,
            'home_address': user.home_address,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=72)
        }
        payload.update(additional_payload)
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        return token

    @staticmethod
    def get_payload_from_token(token: str)-> dict:
        token = token.split(' ')[1]
        try:
            return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token is expired")
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Incorrect token type!")
            
