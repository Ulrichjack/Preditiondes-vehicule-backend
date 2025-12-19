from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.alerte import Alerte
from app.schemas.alerte import AlerteResponse
from app.database import get_db
from app.services.alerte_service import generer_alertes_vehicule

router = APIRouter(prefix="/alertes", tags=["Alertes"])


@router.get("/", response_model=List[AlerteResponse])
def lister_alertes(db: Session = Depends(get_db)):
    """Liste toutes les alertes actives"""
    return db.query(Alerte).filter(Alerte.date_resolution.is_(None)).all()


@router.get("/vehicule/{vehicule_id}", response_model=List[AlerteResponse])
def alertes_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """Alertes d'un véhicule spécifique"""
    return db.query(Alerte).filter(
        Alerte.vehicule_id == vehicule_id,
        Alerte.date_resolution.is_(None)
    ).all()


@router.post("/generer/{vehicule_id}")
def generer(vehicule_id: int, db: Session = Depends(get_db)):
    """Forcer la génération d'alertes pour un véhicule"""
    generer_alertes_vehicule(vehicule_id, db)
    return {"message": "Alertes générées"}