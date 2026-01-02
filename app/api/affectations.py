# app/api/affectations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.affectation_service import (
    affecter_vehicule, cloturer_affectation, obtenir_affectation_active
)
from app.schemas.affectation import AffectationCreate, AffectationClose, AffectationResponse
from app.database import get_db
from app.models.affectation import Affectation  # ✅ Ajouté

router = APIRouter(prefix="/affectations", tags=["Affectations"])


@router.post("/", response_model=AffectationResponse, status_code=201)
def creer(data: AffectationCreate, db: Session = Depends(get_db)):
    return affecter_vehicule(db, data)


# ✅ AJOUT : Route pour lister TOUTES les affectations
@router.get("/", response_model=List[AffectationResponse])
def lister_toutes(db: Session = Depends(get_db)):
    """Liste toutes les affectations (en cours, terminées, annulées)"""
    return db.query(Affectation).order_by(Affectation.date_debut.desc()).all()


@router.get("/actives", response_model=List[AffectationResponse])
def actives(db: Session = Depends(get_db)):
    """Liste uniquement les affectations en cours"""
    return db.query(Affectation).filter(Affectation.date_fin.is_(None)).all()


@router.patch("/{affectation_id}/cloturer", response_model=AffectationResponse)
def cloturer(affectation_id: int, data: AffectationClose, db: Session = Depends(get_db)):
    return cloturer_affectation(db, affectation_id, data)

@router.get("/", response_model=List[AffectationResponse])
def lister_toutes(db: Session = Depends(get_db)):
    """Liste toutes les affectations"""
    return db.query(Affectation).order_by(Affectation.date_debut.desc()).all()

@router.get("/vehicule/{vehicule_id}", response_model=List[AffectationResponse])
def par_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """Affectations d'un véhicule"""
    return db.query(Affectation).filter(
        Affectation.vehicule_id == vehicule_id
    ).order_by(Affectation.date_debut.desc()).all()

@router.get("/chauffeur/{chauffeur_id}", response_model=List[AffectationResponse])
def par_chauffeur(chauffeur_id: int, db: Session = Depends(get_db)):
    """Affectations d'un chauffeur"""
    return db.query(Affectation).filter(
        Affectation.chauffeur_id == chauffeur_id
    ).order_by(Affectation.date_debut.desc()).all()

@router.get("/active/{vehicule_id}", response_model=Optional[AffectationResponse])
def affectation_active(vehicule_id: int, db: Session = Depends(get_db)):
    """Affectation active d'un véhicule"""
    return db.query(Affectation).filter(
        Affectation.vehicule_id == vehicule_id,
        Affectation.date_fin.is_(None)
    ).first()