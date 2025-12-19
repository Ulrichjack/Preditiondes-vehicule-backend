from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EntretienCreate(BaseModel):
    vehicule_id: int = Field(..., example=1)
    type_entretien: str = Field(..., example="VIDANGE")
    kilometrage: int = Field(..., ge=0)
    cout: Optional[int] = Field(0.0, ge=0)
    notes: Optional[str] = None


class EntretienResponse(BaseModel):
    id: int
    vehicule_id: int
    type_entretien: str
    date_entretien: datetime
    kilometrage: int
    cout: int
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}