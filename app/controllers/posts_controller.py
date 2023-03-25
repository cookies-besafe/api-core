from typing import List
from app.models.user import User
from app.models.post import Post
from fastapi import APIRouter, Depends
from app.helpers.middlewares import jwt_auth_middleware
from app.serializers.posts.get_post_serializer import GetPostSerializer


router = APIRouter(
    prefix="/api/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[GetPostSerializer])
async def index(page: int = 1, user: User=Depends(jwt_auth_middleware)):
    return await Post.objects.select_related('user').paginate(page).all()
