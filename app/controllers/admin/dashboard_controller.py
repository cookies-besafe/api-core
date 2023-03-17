from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.helpers.dependencies import get_token_header

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["index"])
def index():
    return {'need': 'template'}
