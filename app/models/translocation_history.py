import ormar
from datetime import datetime
from app.models.sos_request import SosRequest
from typing import Optional, Union
from app.core.base_meta import BaseMeta

class TranslocationHistory(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'translocation_histories'

    id: int = ormar.Integer(primary_key=True)
    lat: float = ormar.Float(nullable=False)
    long: float = ormar.Float(nullable=False)
    sos_request: Optional[Union[SosRequest, dict]] = ormar.ForeignKey(SosRequest, related_name="translocation_histories", ondelete="RESTRICT")
    created_at: datetime = ormar.DateTime(timezone=True, default=datetime.now())
