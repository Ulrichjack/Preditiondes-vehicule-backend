from datetime import datetime,date
from typing import Optional

from pydantic import Field, EmailStr, BaseModel, validator, field_validator
import re

class ChauffeurBase(BaseModel):
    nom: str = Field(..., example="karlos")
    prenom: str = Field(..., example="santana")
    telephone: str = Field(..., example="+33123456789")
    email: Optional[EmailStr] = Field(None, example="karlos@example.com")

class ChauffeurCreate(ChauffeurBase):
    numero_permis: str = Field(..., example="AB1234567")
    date_expiration_permis: date = Field(..., example="2025-12-31")

    @field_validator("telephone")
    def valider_telephone(cls, v):
        pattern = r"^\+?(237|33|225|229|241|242)\d{8,10}$"  # Cameroun, France, CI, etc.        if not re.match(pattern, v):
        if not re.match(pattern, v):
            raise ValueError("Numéro de téléphone invalide (ex: +237691234567)")
        return v

    @field_validator("date_expiration_permis")
    def valider_date_expiration_permis(cls, v):
        if v <= date.today():
            raise ValueError("La date d'expiration du permis doit être une date future.")
        return v

class ChauffeurUpdate(BaseModel):
    telephone: Optional[str] = Field(None, example="+33123456789")
    email: Optional[EmailStr] = None
    statut: Optional[str] = Field(None, example="ACTIF")
    date_expiration_permis: Optional[date] = None

class ChauffeurResponse(ChauffeurBase):
    id: int
    numero_permis: str
    statut: str
    date_expiration_permis: date
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}