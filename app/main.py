from fastapi import FastAPI
from app.core.base_meta import database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.controllers import (
    authentication_controller,
    trusted_contacts_controller,
    shelters_controller,
    sos_request_controller,
    posts_controller
    )
from app.controllers.dashboard import authentication_controller as dash_auth_controller
from app.controllers.dashboard import users_controller as dash_user_controller
from app.controllers.dashboard import shelters_controller as dash_shelter_controller
from app.controllers.dashboard import dashboard_controller
from app.controllers.dashboard import posts_controller as dash_post_controller
from app.services.connection_service import ConnectionService
from app.services.smtp_service import SMTPService


app = FastAPI(title="Emergency Button Core API")


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

connection_service = ConnectionService()
# smtp_service = SMTPService()

app.include_router(authentication_controller.router)
app.include_router(trusted_contacts_controller.router)
app.include_router(sos_request_controller.router)
app.include_router(posts_controller.router)
app.include_router(shelters_controller.router)
app.include_router(dashboard_controller.router)
app.include_router(dash_user_controller.router)
app.include_router(dash_auth_controller.router)
app.include_router(dash_shelter_controller.router)
app.include_router(dash_post_controller.router)


@app.get("/")
async def root():
    # create a dummy entry
    try:
        from app.models.user import User
        from app.services.hasher_service import HasherService
        await User.objects.get_or_create(
            email="admin@gmail.com", 
            is_staff=True, 
            password=HasherService.get_password_hash('admin'),
            first_name="admin",
            last_name="maxima",
            phone="228",
            telegram_nickname="",
            home_address="",
            gender="non-binary"
            )
    except:
        pass
    return {'detail': 'Root'}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
