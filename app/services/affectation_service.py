# app/services/affectation_service.py
from sqlalchemy.orm import Session
from app.models.affectation import Affectation
from app.models.vehicule import Vehicule, StatutVehicule
from app.schemas.affectation import AffectationCreate, AffectationClose
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional


def affecter_vehicule(db: Session, data: AffectationCreate) -> Affectation:
    # Vérifier que le véhicule existe et est disponible
    vehicule = db.query(Vehicule).filter(Vehicule.id == data.vehicule_id).first()
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    if vehicule.statut != StatutVehicule.DISPONIBLE:
        raise HTTPException(status_code=400, detail="Véhicule non disponible")

    # Vérifier qu’il n’y a pas déjà une mission en cours
    mission_en_cours = db.query(Affectation).filter(
        Affectation.vehicule_id == data.vehicule_id,
        Affectation.date_fin.is_(None)
    ).first()
    if mission_en_cours:
        raise HTTPException(status_code=400, detail="Ce véhicule est déjà en mission")

    # Créer l’affectation
    affectation = Affectation(
        vehicule_id=data.vehicule_id,
        chauffeur_id=data.chauffeur_id,
        mission=data.mission,
        kilometrage_depart=data.kilometrage_depart,
        statut="EN_COURS"
    )
    db.add(affectation)

    # Mettre à jour le statut du véhicule
    vehicule.statut = StatutVehicule.EN_MISSION
    db.commit()
    db.refresh(affectation)
    return affectation


def cloturer_affectation(db: Session, affectation_id: int, data: AffectationClose) -> Affectation:
    affectation = db.query(Affectation).filter(Affectation.id == affectation_id).first()
    if not affectation:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    if affectation.date_fin:
        raise HTTPException(status_code=400, detail="Mission déjà clôturée")

    affectation.date_fin = data.date_fin
    affectation.kilometrage_retour = data.kilometrage_retour
    affectation.statut = "TERMINEE"

    # Remettre le véhicule disponible
    vehicule = db.query(Vehicule).filter(Vehicule.id == affectation.vehicule_id).first()
    if vehicule:
        vehicule.statut = StatutVehicule.DISPONIBLE

    db.commit()
    db.refresh(affectation)
    return affectation


def obtenir_affectation_active(db: Session, vehicule_id: int) -> Optional[Affectation]:
    return db.query(Affectation).filter(
        Affectation.vehicule_id == vehicule_id,
        Affectation.date_fin.is_(None)
    ).first()


def historique_affectations_vehicule(db: Session, vehicule_id: int) -> List[Affectation]:
    return db.query(Affectation).filter(Affectation.vehicule_id == vehicule_id).order_by(Affectation.date_debut.desc()).all()