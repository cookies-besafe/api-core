from app.models.user import User
from app.services.jwt_service import JWTService
from app.services.hasher_service import HasherService
from app.helpers.middlewares import jwt_auth_middleware
from app.serializers.authentication.login_serializer import LoginSerializer
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from app.serializers.authentication.registration_serializer import RegistrationSerializer

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", tags=["profile"])
async def me(user: User=Depends(jwt_auth_middleware)):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "email": user.email,
        "telegram_nickname": user.telegram_nickname,
        "home_address": user.home_address,
        "is_staff": user.is_staff,
        "email_veryfied": user.email_veryfied,
    }


@router.post("/login", tags=["login"])
async def login(body: LoginSerializer):
    user = await User.objects.get_or_none(email=body.email)
    if user is None:
        raise HTTPException(status_code=422, detail="Incorrect credentials, please try again!")
    if not HasherService.verify_password(body.password, user.password):
        raise HTTPException(status_code=422, detail="Incorrect password!")
    return {
        'token': f"Bearer {JWTService.create_token_by_user(user)}"
    }


@router.post("/register", tags=["register"])
async def register(body: RegistrationSerializer):
    user = await User.objects.create(
            first_name=body.first_name,
            last_name=body.last_name,
            phone=body.phone,
            email=body.email,
            telegram_nickname=body.telegram_nickname,
            home_address=body.home_address,
            password=HasherService.get_password_hash(body.password),
        )
    response = {
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'email': user.email,
            'telegram_nickname': user.telegram_nickname,
            'home_address': user.home_address,
        },
        'token': f"Bearer {JWTService.create_token_by_user(user)}"
    }
    return response
