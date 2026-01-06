from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.services.cours_service import (
    creer_cours, lire_cours, lister_cours,
    mettre_a_jour_cours, supprimer_cours
)
from app.schemas.cours import (
    CoursCreate, CoursUpdate, CoursResponse
)
from app.database import get_db

router = APIRouter(prefix="/cours", tags=["Cours"])


@router.post("/", response_model=CoursResponse, status_code=status.HTTP_201_CREATED)
def create(data: CoursCreate, db: Session = Depends(get_db)):
    """Créer un nouveau cours"""
    return creer_cours(db, data)


@router.get("/", response_model=List[CoursResponse])
def lister(db: Session = Depends(get_db)):
    """Lister tous les cours"""
    return lister_cours(db)


@router.get("/{cours_id}", response_model=CoursResponse)
def obtenir(cours_id: int, db: Session = Depends(get_db)):
    """Obtenir un cours par son ID"""
    return lire_cours(db, cours_id)


@router.put("/{cours_id}", response_model=CoursResponse)
def modifier(cours_id: int, data: CoursUpdate, db: Session = Depends(get_db)):
    """Modifier un cours existant"""
    return mettre_a_jour_cours(db, cours_id, data)


@router.delete("/{cours_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer(cours_id: int, db: Session = Depends(get_db)):
    """Supprimer un cours"""
    supprimer_cours(db, cours_id)
    return None
