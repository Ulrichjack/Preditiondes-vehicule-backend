from sqlalchemy.orm import Session
from app.models.cours import Cours
from app.schemas.cours import CoursCreate, CoursUpdate
from fastapi import HTTPException
from typing import List


def creer_cours(db: Session, data: CoursCreate) -> Cours:
    """Créer un nouveau cours"""
    nouveau_cours = Cours(
        titre=data.titre,
        description=data.description,
        professeur_nom=data.professeur_nom
    )
    
    db.add(nouveau_cours)
    db.commit()
    db.refresh(nouveau_cours)
    return nouveau_cours


def lire_cours(db: Session, cours_id: int) -> Cours:
    """Récupérer un cours par son ID"""
    cours = db.query(Cours).filter(Cours.id == cours_id).first()
    if not cours:
        raise HTTPException(status_code=404, detail="Cours non trouvé.")
    return cours


def lister_cours(db: Session) -> List[Cours]:
    """Lister tous les cours"""
    return db.query(Cours).all()


def mettre_a_jour_cours(db: Session, cours_id: int, data: CoursUpdate) -> Cours:
    """Mettre à jour un cours existant"""
    cours = lire_cours(db, cours_id)
    
    if data.titre is not None:
        cours.titre = data.titre
    if data.description is not None:
        cours.description = data.description
    if data.professeur_nom is not None:
        cours.professeur_nom = data.professeur_nom
    
    db.commit()
    db.refresh(cours)
    return cours


def supprimer_cours(db: Session, cours_id: int) -> None:
    """Supprimer un cours"""
    cours = lire_cours(db, cours_id)
    db.delete(cours)
    db.commit()
