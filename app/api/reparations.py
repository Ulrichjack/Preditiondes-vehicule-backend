from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.services.reparation_service import enregistrer_reparation, historique_reparations
from app.schemas.reparation import ReparationCreate, ReparationResponse
from app.database import get_db

router = APIRouter(prefix="/reparations", tags=["Reparations"])


@router.post("/", response_model=ReparationResponse, status_code=201)
def creer(data: ReparationCreate, db: Session = Depends(get_db)):
    """Enregistrer une nouvelle réparation"""
    return enregistrer_reparation(db, data)


@router.get("/vehicule/{vehicule_id}", response_model=List[ReparationResponse])
def lister_par_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """Historique des réparations d'un véhicule"""
    return historique_reparations(db, vehicule_id)