from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AffectationCreate(BaseModel):
    vehicule_id: int = Field(..., example=1)
    chauffeur_id: int = Field(..., example=1)
    mission: str = Field(..., example="Livraison de marchandises")
    kilometrage_depart: int = Field(..., ge=0, example=50000)


class AffectationClose(BaseModel):
    date_fin: datetime = Field(..., example="2024-12-31T15:30:00Z")
    kilometrage_retour: int = Field(..., ge=0, example=50500)


class AffectationResponse(BaseModel):
    id: int
    vehicule_id: int
    chauffeur_id: int
    date_debut: datetime
    date_fin: Optional[datetime]
    mission: str | None
    kilometrage_depart: Optional[int]
    kilometrage_retour: Optional[int]
    statut: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}