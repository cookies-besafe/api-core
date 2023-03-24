from fastapi import APIRouter, Depends, Request
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/dashboard/users",
    tags=["dashboard_users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/page={page}", response_class=HTMLResponse)
async def dashboard_users_index(request: Request, page: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    users = await User.objects.paginate(page).all()
    users_count = users.count(True)
    return main.templates.TemplateResponse("dashboard/users/index.html", {
        'request': request,
        'current_user': user,
        'users': users,
        'users_count': users_count,
        'page': page
    })


@router.post("/{id}/change-staff-status/page={page}", response_class=RedirectResponse)
async def dashboard_users_change_staff_status(request: Request, id: int, page: int, current_user: User=Depends(dashboard_middleware)):
    if not current_user:
        return RedirectResponse(request.url_for('dashboard_users_index', page=page), status_code=303)
    user = await User.objects.get_or_none(pk=id)
    if not user:
        return RedirectResponse(request.url_for('dashboard_users_index', page=page), status_code=303)
    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True
    await user.update()
    return RedirectResponse(request.url_for('dashboard_users_index', page=page), status_code=303)

