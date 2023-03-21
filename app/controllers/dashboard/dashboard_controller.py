from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware, jwt_auth_middleware
from app.serializers.authentication.login_serializer import LoginSerializer
from app.services.cookie_service import CookieService
from app.services.hasher_service import HasherService
from app.services.jwt_service import JWTService
from app import main
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return main.templates.TemplateResponse("dashboard/authentication/login.html", {
        'request': request
    })


@router.post('/login', response_class=HTMLResponse)
async def login(request: Request, response: Response, body: LoginSerializer):
    user = await User.objects.get_or_none(email=body.email)
    if user is None:
        raise HTTPException(status_code=422, detail="Incorrect credentials, please try again!")
    if not HasherService.verify_password(body.password, user.password):
        raise HTTPException(status_code=422, detail="Incorrect password!")
    response = main.templates.TemplateResponse("dashboard/authentication/login.html", {
        'request': request
    })
    CookieService.set_cookie(response=response, access_token=JWTService.create_token_by_user(user))
    return response


@router.get("/", response_class=HTMLResponse)
def index(request: Request, user: User=Depends(dashboard_middleware)):
    return main.templates.TemplateResponse("dashboard/authentication/login.html", {
        'request': request
    })
