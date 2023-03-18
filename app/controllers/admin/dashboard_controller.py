from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.helpers.middlewares import jwt_auth_middleware

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(jwt_auth_middleware)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["index"])
def index():
    return {'need': 'template'}
