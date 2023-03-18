from typing import List

from ormar.exceptions import NoMatch
from app.models.user import User
from app.models.trusted_contact import TrustedContact
from app.serializers.trusted_contacts.get_trusted_contact_serializer import GetTrustedContactSerializer
from app.serializers.trusted_contacts.create_trusted_contact_serializer import CreateTrustedContactSerializer
from app.serializers.trusted_contacts.update_trusted_contact_serializer import UpdateTrustedContactSerializer
from app.serializers.trusted_contacts.bulk_update_trusted_contact_serializer import BulkUpdateTrustedContactSerializer
from app.helpers.middlewares import jwt_auth_middleware
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/api/trusted-contacts",
    tags=["trusted_contacts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=['index'], response_model=List[GetTrustedContactSerializer])
async def index(user: User=Depends(jwt_auth_middleware)):
    return await user.trusted_contacts.all()


@router.post('/bulk-store', tags=['bulk_store'], response_model=List[GetTrustedContactSerializer])
async def bulk_store(body: List[CreateTrustedContactSerializer], user: User=Depends(jwt_auth_middleware)):
    for contact in body:
        await TrustedContact.objects.create(
            name=contact.name,
            phone=contact.phone,    
            email=contact.email,
            telegram_nickname=contact.telegram_nickname,
            user=user
        )
    return await user.trusted_contacts.all()


@router.patch('/bulk-update', tags=['bulk_update'], response_model=List[GetTrustedContactSerializer])
async def bulk_update(body: List[BulkUpdateTrustedContactSerializer], user: User=Depends(jwt_auth_middleware)):
    for contact in body:
        trusted_contact = await user.trusted_contacts.get_or_none(pk=contact.id)
        if trusted_contact is None:
            continue
        if contact.name is not None:
            trusted_contact.name = contact.name
        if contact.phone is not None:
            trusted_contact.phone = contact.phone
        if contact.email is not None:
            trusted_contact.email = contact.email
        if contact.telegram_nickname is not None:
            trusted_contact.telegram_nickname = contact.telegram_nickname
        await trusted_contact.update()
    return await user.trusted_contacts.all()


@router.post('/', tags=['store'], response_model=GetTrustedContactSerializer)
async def store(body: CreateTrustedContactSerializer, user: User=Depends(jwt_auth_middleware)):
    return await TrustedContact.objects.create(
        name=body.name,
        phone=body.phone,
        email=body.email,
        telegram_nickname=body.telegram_nickname,
        user=user
    )


@router.patch("/{id}", tags=['update'], response_model=GetTrustedContactSerializer)
async def update(id: int, body: UpdateTrustedContactSerializer, user: User=Depends(jwt_auth_middleware)):
    trusted_contact = await user.trusted_contacts.get_or_none(pk=id)
    if trusted_contact is None:
        raise HTTPException(status_code=404, detail='Contact is not found, try another id')
    if body.name is not None:
        trusted_contact.name = body.name
    if body.phone is not None:
        trusted_contact.phone = body.phone
    if body.email is not None:
        trusted_contact.email = body.email
    if body.telegram_nickname is not None:
        trusted_contact.telegram_nickname = body.telegram_nickname
    return await trusted_contact.update()


@router.delete("/{id}", tags=['destroy'])
async def destroy(id: int, user: User=Depends(jwt_auth_middleware)):
    try:
        trusted_contact = await TrustedContact.objects.get(pk=id)
        await trusted_contact.delete()
        return {
            'status': 'success',
            'detail': 'Contact deleted successfully!'
        }
    except NoMatch:
        raise HTTPException(status_code=404, detail='Contact is not found, try another id')
