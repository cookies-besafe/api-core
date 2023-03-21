from fastapi import APIRouter, Depends, HTTPException, Response
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware, jwt_auth_middleware
from app.serializers.authentication.login_serializer import LoginSerializer
from app.services.cookie_service import CookieService
from app.services.hasher_service import HasherService
from app.services.jwt_service import JWTService
from app.main import templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(jwt_auth_middleware)],
    responses={404: {"description": "Not found"}},
)


@router.get('/login', response_class=HTMLResponse)
async def login():
    return templates.TemplateResponse("dashboard/authentication/login.html", {
        'status': 'undefined'
    })


@router.post('/login', response_class=HTMLResponse)
async def login(response: Response, body: LoginSerializer):
    user = await User.objects.get_or_none(email=body.email)
    if user is None:
        raise HTTPException(status_code=422, detail="Incorrect credentials, please try again!")
    if not HasherService.verify_password(body.password, user.password):
        raise HTTPException(status_code=422, detail="Incorrect password!")
    response = templates.TemplateResponse("dashboard/authentication/login.html", {
        'status': 'success'
    })
    CookieService.set_cookie(response=response, access_token=JWTService.create_token_by_user(user))
    return response


@router.get("/", response_class=HTMLResponse)
def index(user: User=Depends(dashboard_middleware)):
    return {'need': 'template'}
