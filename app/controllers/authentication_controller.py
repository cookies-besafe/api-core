from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.user import User
from app.helpers.dependencies import get_token_header
from app.services.hasher_service import HasherService
from app.services.jwt_service import JWTService
from app.serializers.registration_serializer import RegistrationSerializer
from app.serializers.login_serializer import LoginSerializer

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", tags=["profile"], dependencies=[Depends(get_token_header)])
async def me(authorization: str = Header()):
    service = JWTService()
    payload = service.get_payload_from_token(authorization)
    return payload


@router.post("/login", tags=["login"])
async def login(body: LoginSerializer):
    user = await User.objects.get_or_none(email=body.email)
    if user is None:
        raise HTTPException(status_code=422, detail="Incorrect credentials, please try again!")
    if not HasherService.verify_password(body.password, user.password):
        raise HTTPException(status_code=422, detail="Incorrect password!")
    service = JWTService()
    return {
        'token': f"Bearer {service.create_token_by_user(user)}"
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
            password=body.password,
        )
    service = JWTService()
    response = {
        'user': user,
        'token': f"Bearer {service.create_token_by_user(user)}"
    }
    return response
