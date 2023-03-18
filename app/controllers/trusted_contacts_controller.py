from app.models.user import User
from app.models.trusted_contact import TrustedContact
from app.helpers.middlewares import jwt_auth_middleware
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/api/trusted-contacts",
    tags=["trusted_contacts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", tags=['index'])
async def index(user: User=Depends(jwt_auth_middleware)):
    return
