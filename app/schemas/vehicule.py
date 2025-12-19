from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, validator, field_validator


class VehiculeBase(BaseModel):
    immatriculation: str = Field(..., example="AB-123-CD")
    marque: str = Field(..., example="Toyota")
    modele: str = Field(..., example="Corolla")
    annee: int = Field(...,
                       ge=1886,
                       le=2026,
                       example=2020,
                       description="Annee de mise en circulation du vehicule")


class VehiculeCreate(VehiculeBase):
    kilometrage: Optional[int] = Field(
        0,
        ge=0,
        example=85000,
        description="Kilometrage initial du vehicule"
    )
    date_dernier_entretien: Optional[date] = Field(
        None,
        example="2023-01-15",
        description="Date du dernier entretien du vehicule"
    )

    @field_validator("immatriculation")
    @classmethod
    def valider_immatriculation(cls, v):
        pattern = r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"
        if not re.match(pattern, v.upper()):
            raise ValueError("L'immatriculation invalide (ex: AB-123-CD)")
        return v.upper()


class VehiculeUpdate(BaseModel):
    kilometrage: Optional[int] = Field(None, ge=0,description="Mise a jour du kilometrage du vehicule")
    statut: Optional[str] = None
    date_dernier_entretien: Optional[date] = None

class VehiculeInDB(VehiculeBase):
    id: int
    kilometrage: int
    date_dernier_entretien: Optional[date]
    statut: str
    score_sante: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VehiculeResponse(VehiculeBase):
    id: int
    kilometrage: int
    statut: str
    score_sante: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}