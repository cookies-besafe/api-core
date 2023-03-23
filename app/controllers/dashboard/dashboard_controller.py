from fastapi import APIRouter, Depends, Request
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
def dashboard_index(request: Request, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    return main.templates.TemplateResponse("dashboard/index.html", {
        'request': request
    })
