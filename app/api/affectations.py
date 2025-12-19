# app/api/affectations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.affectation_service import (
    affecter_vehicule, cloturer_affectation, obtenir_affectation_active
)
from app.schemas.affectation import AffectationCreate, AffectationClose, AffectationResponse
from app.database import get_db

router = APIRouter(prefix="/affectations", tags=["Affectations"])


@router.post("/", response_model=AffectationResponse, status_code=201)
def creer(data: AffectationCreate, db: Session = Depends(get_db)):
    return affecter_vehicule(db, data)


@router.patch("/{affectation_id}/cloturer", response_model=AffectationResponse)
def cloturer(affectation_id: int, data: AffectationClose, db: Session = Depends(get_db)):
    return cloturer_affectation(db, affectation_id, data)


@router.get("/actives", response_model=List[AffectationResponse])
def actives(db: Session = Depends(get_db)):
    from app.models.affectation import Affectation
    return db.query(Affectation).filter(Affectation.date_fin.is_(None)).all()