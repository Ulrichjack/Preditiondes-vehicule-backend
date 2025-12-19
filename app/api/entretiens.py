from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.entretien_service import enregistrer_entretien, historique_entretiens
from app.schemas.entretien import EntretienCreate, EntretienResponse
from app.database import get_db

router = APIRouter(prefix="/entretiens", tags=["Entretiens"])


@router.post("/", response_model=EntretienResponse, status_code=201)
def creer(data: EntretienCreate, db: Session = Depends(get_db)):
    """Enregistrer un nouvel entretien"""
    return enregistrer_entretien(db, data)


@router.get("/vehicule/{vehicule_id}", response_model=List[EntretienResponse])
def lister_par_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """Historique des entretiens d'un véhicule"""
    return historique_entretiens(db, vehicule_id)