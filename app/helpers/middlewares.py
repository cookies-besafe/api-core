from fastapi import Header, HTTPException
from app.models.user import User
from app.services.jwt_service import JWTService


async def jwt_auth_middleware(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No Authorization header is provided")
    payload = JWTService.get_payload_from_token(authorization)
    try:
        user = await User.objects.get_or_none(id=payload['sub'])
        if not user or user.email != payload['email']:
            raise HTTPException(status_code=401, detail="Incorrect token type!")
    except KeyError:
        raise HTTPException(status_code=401, detail="Incorrect token type!")
    