# app/services/reparation_service.py
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Vehicule
from app.models.reparation import Reparation
from app.schemas.reparation import ReparationCreate
from fastapi import HTTPException
from app.services.prediction_service import calculer_score_sante
from app.services.alerte_service import generer_alertes_vehicule


def enregistrer_reparation(db: Session, data: ReparationCreate) -> Reparation:
    vehicule = db.query(Vehicule).filter(Vehicule.id == data.vehicule_id).first()
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")

    reparation = Reparation(
        vehicule_id=data.vehicule_id,
        type_panne=data.type_panne,
        gravite=data.gravite,
        kilometrage=data.kilometrage,
        cout=data.cout,
        description=data.description,
        pieces_remplacees=data.pieces_remplacees,
        date_reparation=datetime.now()
    )
    db.add(reparation)
    db.commit()
    db.refresh(reparation)

    # MAJ du kilométrage
    vehicule.kilometrage = data.kilometrage

    # CRUCIAL : recalculer score + alertes
    calculer_score_sante(data.vehicule_id, db)
    generer_alertes_vehicule(data.vehicule_id, db)

    return reparation


def historique_reparations(db: Session, vehicule_id: int):
    return db.query(Reparation).filter(Reparation.vehicule_id == vehicule_id).order_by(Reparation.date_reparation.desc()).all()