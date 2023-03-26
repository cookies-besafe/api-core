import json
from datetime import datetime
from typing import List
from app.models.user import User
from app.models.sos_request import SosRequest
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from app.helpers.middlewares import jwt_auth_middleware
from app.models.translocation_history import TranslocationHistory
from app.serializers.sos_requests.get_sos_request_serializer import GetSosRequestSerializer


router = APIRouter(
    prefix="/api/sos-request",
    tags=["sos_request"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[GetSosRequestSerializer])
async def index(user: User=Depends(jwt_auth_middleware)):
    return await user.sos_requests.all()


@router.post("/", response_model=GetSosRequestSerializer)
async def store(user: User=Depends(jwt_auth_middleware)):
    active_sos_requests_count = await user.sos_requests.filter(is_active=True).count()
    if active_sos_requests_count > 0:
        return await SosRequest.objects.filter(is_active=True).select_related('user').first() 
    return await SosRequest.objects.create(user=user)


@router.patch("/{id}", response_model=GetSosRequestSerializer)
async def switch_status(id: int, user: User=Depends(jwt_auth_middleware)):
    sos_request = await user.sos_requests.get_or_none(pk=id)
    if sos_request is None:
        raise HTTPException(status_code=404, detail='Sos request is not found, try another id')
    if sos_request.is_active:
        sos_request.is_active = False
    else:
        sos_request.is_active = True
    return await sos_request.update()


customers = []
# TODO: not updating dashboard
@router.websocket("/{id}/location-live-update")
async def location_live_update(id: int, websocket: WebSocket):
    customers.append(websocket)
    await websocket.accept()
    connection = False
    sos_request = await SosRequest.objects.get_or_none(pk=id)
    if sos_request is not None:
        connection = True
    while connection:
        data = await websocket.receive_text()
        if data:
            data = json.loads(data)
            await TranslocationHistory.objects.create(
                        lat=data.get('lat'),
                        long=data.get('long'),
                        sos_request=sos_request
                    )
            response = json.dumps({
                "status": f"Location updated and saved to DB. Latitude: {data.get('lat')}, longitude: {data.get('long')}"
            })
            for customer in customers:
                await customer.send_text(response)
