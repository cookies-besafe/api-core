from fastapi import Header, HTTPException, Request
from app.models.user import User
from app.services.cookie_service import CookieService
from app.services.jwt_service import JWTService


async def jwt_auth_middleware(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No Authorization header is provided")
    payload = JWTService.get_payload_from_token(authorization)
    user = await User.objects.get_or_none(id=payload.get('sub'))
    if not user or user.email != payload.get('email'):
        raise HTTPException(status_code=401, detail="Incorrect token type!")
    return user


async def dashboard_middleware(request: Request):
    authorization = CookieService.get_cookie(request=request)
    if authorization is None:
        raise HTTPException(status_code=401, detail="No Authorization header is provided")
    payload = JWTService.get_payload_from_token(authorization)
    user = await User.objects.get_or_none(id=payload.get('sub'))
    if not user or user.email != payload.get('email'):
        raise HTTPException(status_code=401, detail="Incorrect token type!")
    if not user.is_staff:
        raise HTTPException(status_code=403, detail="Forbidden, you are not a stuff")
    return user
