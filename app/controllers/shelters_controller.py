from typing import List
from app.models.user import User
from app.models.shelter import Shelter
from fastapi import APIRouter, Depends
from app.helpers.middlewares import jwt_auth_middleware
from app.serializers.shelters.get_shelter_serializer import GetShelterSerializer


router = APIRouter(
    prefix="/api/shelters",
    tags=["shelters"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[GetShelterSerializer])
async def index(user: User=Depends(jwt_auth_middleware)):
    return await Shelter.objects.select_related('user').all()
