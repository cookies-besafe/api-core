from ormar.exceptions import NoMatch
from typing import List
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from app.models.user import User
from app.models.sos_request import SosRequest
from app.helpers.middlewares import dashboard_middleware
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse
from app.serializers.sos_requests.get_sos_request_serializer import GetSosRequestSerializer
from app.services.cookie_service import CookieService

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/page={page}", response_class=HTMLResponse)
async def dashboard_index(request: Request, page: int = 1, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    sos_requests = await SosRequest.objects.select_related('user').filter(is_active=True).order_by('-created_at').paginate(page).all()
    sos_requests_count = sos_requests.count(True)
    return main.templates.TemplateResponse("dashboard/index.html", {
        'request': request,
        'current_user': user,
        'sos_requests': sos_requests,
        'sos_requests_count': sos_requests_count,
        'page': page
    })


@router.get("/page={page}/sos-requests/history", response_class=HTMLResponse)
async def dashboard_sos_requests_history(request: Request, page: int = 1, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    sos_requests = await SosRequest.objects.select_related('user').filter(is_active=False).order_by('-created_at').paginate(page).all()
    sos_requests_count = sos_requests.count(True)
    return main.templates.TemplateResponse("dashboard/sos_requests/history.html", {
        'request': request,
        'current_user': user,
        'sos_requests': sos_requests,
        'sos_requests_count': sos_requests_count,
        'page': page
    })


@router.get("/async-sos-requests", response_model=List[GetSosRequestSerializer])
async def dashboard_sos_requests(request: Request, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    return await SosRequest.objects.select_related('user').filter(is_active=True).order_by('-created_at').paginate(1).all()
# Send here short polling request to update sos-requests list
# after it just connect to socket event on update location (the same func)


@router.get('/sos-requests/{id}', response_class=HTMLResponse)
async def dashboard_sos_requests_show(request: Request, id: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    sos_request = await SosRequest.objects.select_related('user').get_or_none(pk=id)
    if sos_request is None:
        return RedirectResponse(request.url_for('dashboard_index', page=1))
    try:
        current_location = await sos_request.translocation_histories.order_by('-created_at').first()
    except NoMatch:
        current_location = {
            "lat": 0,
            "long": 0
        }
    return main.templates.TemplateResponse("dashboard/sos_requests/show.html", {
        'request': request,
        'current_user': user,
        'sos_request': sos_request,
        'current_location': current_location,
    })
