from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.chauffeur_service import (
    creer_chauffeur, lire_chauffeur, lister_chauffeurs,
    mettre_a_jour_chauffeur
)
from app.schemas.chauffeur import (
    ChauffeurCreate, ChauffeurUpdate, ChauffeurResponse
)
from app.database import get_db

router = APIRouter(prefix="/chauffeurs", tags=["Chauffeurs"])


@router.post("/", response_model=ChauffeurResponse, status_code=status.HTTP_201_CREATED)
def create(data: ChauffeurCreate, db: Session = Depends(get_db)):  # ✅ SANS ()
    return creer_chauffeur(db, data)


@router.get("/", response_model=List[ChauffeurResponse])  # ✅ "/" au lieu de ""
def lister(db: Session = Depends(get_db)):  # ✅ SANS ()
    return lister_chauffeurs(db)


@router.get("/{chauffeur_id}", response_model=ChauffeurResponse)
def obtenir(chauffeur_id: int, db: Session = Depends(get_db)):  # ✅ SANS ()
    return lire_chauffeur(db, chauffeur_id)


@router.put("/{chauffeur_id}", response_model=ChauffeurResponse)
def modifier(chauffeur_id: int, data: ChauffeurUpdate, db: Session = Depends(get_db)):  # ✅ SANS ()
    return mettre_a_jour_chauffeur(db, chauffeur_id, data)