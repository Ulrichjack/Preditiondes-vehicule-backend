from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class CoursBase(BaseModel):
    titre: str = Field(..., example="Mécanique automobile de base")
    description: Optional[str] = Field(None, example="Cours sur les principes de base de la mécanique automobile")
    professeur_nom: str = Field(..., example="Prof. Dupont")


class CoursCreate(CoursBase):
    pass


class CoursUpdate(BaseModel):
    titre: Optional[str] = Field(None, example="Mécanique automobile de base")
    description: Optional[str] = Field(None, example="Cours sur les principes de base de la mécanique automobile")
    professeur_nom: Optional[str] = Field(None, example="Prof. Dupont")


class CoursResponse(CoursBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}
