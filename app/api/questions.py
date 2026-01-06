from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.services.question_service import (
    creer_question, lire_question, lister_questions_cours,
    mettre_a_jour_question, supprimer_question
)
from app.schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse
)
from app.database import get_db

router = APIRouter(prefix="/cours", tags=["Questions"])


@router.post("/{cours_id}/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(cours_id: int, data: QuestionCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle question pour un cours"""
    return creer_question(db, cours_id, data)


@router.get("/{cours_id}/questions", response_model=List[QuestionResponse])
def lister_questions(cours_id: int, db: Session = Depends(get_db)):
    """Lister toutes les questions d'un cours"""
    return lister_questions_cours(db, cours_id)


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def obtenir_question(question_id: int, db: Session = Depends(get_db)):
    """Obtenir une question par son ID"""
    return lire_question(db, question_id)


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def modifier_question(question_id: int, data: QuestionUpdate, db: Session = Depends(get_db)):
    """Modifier une question existante"""
    return mettre_a_jour_question(db, question_id, data)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_question_route(question_id: int, db: Session = Depends(get_db)):
    """Supprimer une question"""
    supprimer_question(db, question_id)
    return None
