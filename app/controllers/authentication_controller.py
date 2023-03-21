from app.models.user import User
from app.services.jwt_service import JWTService
from app.services.hasher_service import HasherService
from app.helpers.middlewares import jwt_auth_middleware
from app.serializers.authentication.login_serializer import LoginSerializer
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from app.serializers.authentication.registration_serializer import RegistrationSerializer
from app.serializers.authentication.update_profile_serialozer import UpdateProfileSerializer

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


@router.patch("/me", tags=["profile.update"])
async def update_profile(body: UpdateProfileSerializer, user: User=Depends(jwt_auth_middleware)):
    if user.first_name is not None:
        user.first_name = body.first_name
    if user.last_name is not None:
        user.last_name = body.last_name
    if user.phone is not None:
        user.phone = body.phone
    if user.password is not None:
        user.password = HasherService.get_password_hash(body.password)
    if user.email is not None:
        user.email = body.email
    if user.home_address is not None:
        user.home_address = body.home_address
    if user.telegram_nickname is not None:
        user.telegram_nickname = body.telegram_nickname
    if user.gender is not None:
        user.gender = body.gender
    if user.birth_date is not None:
        user.birth_date = body.birth_date
    return await user.update()


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
            birth_date=body.birth_date,
            gender=body.gender,
            password=HasherService.get_password_hash(body.password),
        )
    response = {
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'email': user.email,
            'birth_date': user.birth_date,
            'gender': user.gender,
            'telegram_nickname': user.telegram_nickname,
            'home_address': user.home_address,
        },
        'token': f"Bearer {JWTService.create_token_by_user(user)}"
    }
    return response
