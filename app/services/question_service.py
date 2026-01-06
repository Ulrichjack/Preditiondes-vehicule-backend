from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.services.cours_service import lire_cours
from fastapi import HTTPException
from typing import List


def creer_question(db: Session, cours_id: int, data: QuestionCreate) -> Question:
    """Créer une nouvelle question pour un cours"""
    # Vérifier que le cours existe
    lire_cours(db, cours_id)
    
    nouvelle_question = Question(
        cours_id=cours_id,
        question_text=data.question_text,
        reponse_attendue=data.reponse_attendue
    )
    
    db.add(nouvelle_question)
    db.commit()
    db.refresh(nouvelle_question)
    return nouvelle_question


def lire_question(db: Session, question_id: int) -> Question:
    """Récupérer une question par son ID"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée.")
    return question


def lister_questions_cours(db: Session, cours_id: int) -> List[Question]:
    """Lister toutes les questions d'un cours"""
    # Vérifier que le cours existe
    lire_cours(db, cours_id)
    
    return db.query(Question).filter(Question.cours_id == cours_id).all()


def mettre_a_jour_question(db: Session, question_id: int, data: QuestionUpdate) -> Question:
    """Mettre à jour une question existante"""
    question = lire_question(db, question_id)
    
    if data.question_text is not None:
        question.question_text = data.question_text
    if data.reponse_attendue is not None:
        question.reponse_attendue = data.reponse_attendue
    
    db.commit()
    db.refresh(question)
    return question


def supprimer_question(db: Session, question_id: int) -> None:
    """Supprimer une question"""
    question = lire_question(db, question_id)
    db.delete(question)
    db.commit()
