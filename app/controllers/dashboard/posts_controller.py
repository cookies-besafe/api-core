from fastapi import APIRouter, Depends, Request, Response, Form
from app.models.post import Post
from app.models.user import User
from app.helpers.middlewares import dashboard_middleware
from app import main
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/dashboard/posts",
    tags=["dashboard_posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/page={page}", response_class=HTMLResponse)
async def dashboard_posts_index(request: Request, page: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    posts = await Post.objects.paginate(page).all()
    posts_count = posts.count(True)
    return main.templates.TemplateResponse("dashboard/posts/index.html", {
        'request': request,
        'current_user': user,
        'posts': posts,
        'posts_count': posts_count,
        'page': page
    })


@router.post('/store', response_class=RedirectResponse)
async def dashboard_posts_store(
    request: Request, 
    title: str = Form(...), 
    content: str = Form(...), 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    await Post.objects.create(
        title=title,
        content=content,
        user=user
    )
    return RedirectResponse(request.url_for('dashboard_posts_index', page=1), status_code=303)  


@router.get("/page={page}/{id}/edit", response_class=HTMLResponse)
async def dashboard_posts_edit(request: Request, page: int, id: int, user: User=Depends(dashboard_middleware)):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    post = await Post.objects.get_or_none(pk=id)
    if post is None:
        return RedirectResponse(request.url_for('dashboard_posts_index', page=1), status_code=303)  
    return main.templates.TemplateResponse("dashboard/posts/edit.html", {
        'request': request,
        'current_user': user,
        'post': post,
        'page': page
    })


@router.post("/page={page}/{id}", response_class=RedirectResponse)
async def dashboard_posts_update(
    request: Request, 
    page: int,
    id: int, 
    title: str = Form(...), 
    content: str = Form(...), 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    post = await Post.objects.get_or_none(pk=id)
    if post is not None:
        post.title = title
        post.content = content
        await post.update()
    return RedirectResponse(request.url_for('dashboard_posts_index', page=page), status_code=303)  


@router.post("/page={page}/{id}/delete")
async def dashboard_posts_destroy(
    request: Request, 
    page: int,
    id: int, 
    user: User=Depends(dashboard_middleware)
    ):
    if not user:
        return RedirectResponse(request.url_for('dashboard_login'))
    post = await Post.objects.get_or_none(pk=id)
    if post is not None:
        await post.delete()
    return RedirectResponse(request.url_for('dashboard_posts_index', page=page), status_code=303)  
