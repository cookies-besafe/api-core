import asyncpg
from fastapi import FastAPI
from app.core.base_meta import database
from app.models.user import User


app = FastAPI(title="Emergency Button Core API")


@app.get("/")
async def read_root():
    # create a dummy entry
    try:
        await User.objects.get_or_create(email="test@test.com")
    except asyncpg.exceptions.UndefinedTableError:
        print('Please, migrate tables by "make migrate"')
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
