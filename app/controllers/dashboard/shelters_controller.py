from fastapi import APIRouter, Depends, Request, Response, Form
from app.models.shelter import Shelter
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/dashboard/shelters",
    tags=["dashboard_shelters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/page={page}", response_class=HTMLResponse)
async def dashboard_shelters_index(request: Request, page: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    shelters = await Shelter.objects.paginate(page).all()
    shelters_count = shelters.count(True)
    return main.templates.TemplateResponse("dashboard/shelters/index.html", {
        'request': request,
        'current_user': user,
        'shelters': shelters,
        'shelters_count': shelters_count,
        'page': page
    })


@router.post('/store', response_class=RedirectResponse)
async def dashboard_shelters_store(
    request: Request, 
    title: str = Form(...), 
    address: str = Form(...), 
    phone: str = Form(...), 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    await Shelter.objects.create(
        title=title,
        phone=phone,
        address=address
    )
    return RedirectResponse(request.url_for('dashboard_shelters_index', page=1), status_code=303)  


@router.get("/page={page}/{id}/edit", response_class=HTMLResponse)
async def dashboard_shelters_edit(request: Request, page: int, id: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    shelter = await Shelter.objects.get_or_none(pk=id)
    if shelter is None:
        return RedirectResponse(request.url_for('dashboard_shelters_index', page=1), status_code=303)  
    return main.templates.TemplateResponse("dashboard/shelters/edit.html", {
        'request': request,
        'current_user': user,
        'shelter': shelter,
        'page': page
    })


@router.post("/page={page}/{id}", response_class=RedirectResponse)
async def dashboard_shelters_update(
    request: Request, 
    page: int,
    id: int, 
    title: str = Form(...), 
    address: str = Form(...), 
    phone: str = Form(...), 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    shelter = await Shelter.objects.get_or_none(pk=id)
    if shelter is not None:
        shelter.title = title
        shelter.address = address
        shelter.phone = phone
        await shelter.update()
    return RedirectResponse(request.url_for('dashboard_shelters_index', page=page), status_code=303)  


@router.post("/page={page}/{id}/delete")
async def dashboard_shelters_destroy(
    request: Request, 
    page: int,
    id: int, 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    shelter = await Shelter.objects.get_or_none(pk=id)
    if shelter is not None:
        await shelter.delete()
    return RedirectResponse(request.url_for('dashboard_shelters_index', page=page), status_code=303)  
