from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware, guest_middleware
from app.serializers.authentication.login_serializer import LoginSerializer
from app.services.cookie_service import CookieService
from app.services.hasher_service import HasherService
from app.services.jwt_service import JWTService
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/dashboard/auth",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get('/login', response_class=HTMLResponse)
async def dashborad_login_page(request: Request, is_guest: bool=Depends(guest_middleware), error: str | None = None):
    if not is_guest:
        return RedirectResponse(request.url_for('dashboard_index'))  
    return main.templates.TemplateResponse("dashboard/authentication/login.html", {
        'request': request,
        'error': error
    })



@router.get('/logout', response_class=HTMLResponse)
async def dashboard_logout(request: Request, response: Response, is_guest: bool=Depends(dashboard_middleware)):
    response = RedirectResponse(request.url_for('dashboard_login'))
    CookieService.delete_cookie(response=response)
    return response


@router.post('/login', response_class=HTMLResponse)
async def dashboard_login(request: Request, response: Response, email: str = Form(...), password: str = Form(...), is_guest: bool=Depends(guest_middleware)):
    if not is_guest:
        return RedirectResponse(request.url_for('dashboard_index'))  
    user = await User.objects.get_or_none(email=email)
    if user is None:
        return main.templates.TemplateResponse("dashboard/authentication/login.html", {
            'request': request,
            'error': 'incorrect_credentials'
        })
    if not HasherService.verify_password(password, user.password):
        return main.templates.TemplateResponse("dashboard/authentication/login.html", {
            'request': request,
            'error': 'incorrect_password'
        })
    if not user.is_staff:
        return main.templates.TemplateResponse("dashboard/authentication/login.html", {
            'request': request,
            'error': 'incorrect_permissions'
        })
    response = RedirectResponse(request.url_for('dashboard_index'), status_code=303)  
    CookieService.set_cookie(response=response, access_token=JWTService.create_token_by_user(user))
    return response

