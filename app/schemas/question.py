from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class QuestionBase(BaseModel):
    question_text: str = Field(..., example="Quelle est la fréquence recommandée pour une vidange ?")
    reponse_attendue: Optional[str] = Field(None, example="Tous les 10 000 km ou tous les 6 mois")


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, example="Quelle est la fréquence recommandée pour une vidange ?")
    reponse_attendue: Optional[str] = Field(None, example="Tous les 10 000 km ou tous les 6 mois")


class QuestionResponse(QuestionBase):
    id: int
    cours_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}
