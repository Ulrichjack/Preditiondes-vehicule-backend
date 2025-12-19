from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReparationCreate(BaseModel):
    vehicule_id: int = Field(..., example=1)
    type_panne: str = Field(..., example="FREINS")
    gravite: str = Field(..., example="CRITIQUE")
    kilometrage: int = Field(..., ge=0)
    cout: float = Field(..., ge=0)
    description: str = Field(..., example="Disques avant HS")
    pieces_remplacees: Optional[str] = None


class ReparationResponse(BaseModel):
    id: int
    vehicule_id: int
    type_panne: str
    gravite: str
    date_reparation: datetime
    kilometrage: int
    cout: float
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}