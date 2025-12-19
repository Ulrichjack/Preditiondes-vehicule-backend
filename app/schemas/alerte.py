from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AlerteResponse(BaseModel):
    id: int
    vehicule_id: int
    type_alerte: str
    priorite: str
    message: str
    est_lue: str
    date_creation: datetime
    date_resolution: Optional[datetime] = None

    model_config = {"from_attributes": True}