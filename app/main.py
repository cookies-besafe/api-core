from fastapi import FastAPI
from app.core.base_meta import database
from app.controllers import (
    authentication_controller,
    trusted_contacts_controller,
    shelters_controller,
    sos_request_controller
    )
from app.controllers.admin import dashboard_controller


app = FastAPI(title="Emergency Button Core API")


app.include_router(authentication_controller.router)
app.include_router(trusted_contacts_controller.router)
app.include_router(sos_request_controller.router)
app.include_router(shelters_controller.router)
app.include_router(dashboard_controller.router)


@app.get("/")
async def root():
    # create a dummy entry
    # try:
    #     await User.objects.get_or_create(email="test@test.com")
    # except asyncpg.exceptions.UndefinedTableError:
    #     print('Please, migrate tables by "make migrate"')
    return {'detail': 'Root'}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
