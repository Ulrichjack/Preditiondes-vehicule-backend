# app/services/entretien_service.py
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Vehicule
from app.models.entretien import Entretien
from app.schemas.entretien import EntretienCreate
from fastapi import HTTPException
from app.services.prediction_service import calculer_score_sante
from app.services.alerte_service import generer_alertes_vehicule  # on le créera juste après


def enregistrer_entretien(db: Session, data: EntretienCreate) -> Entretien:
    vehicule = db.query(Vehicule).filter(Vehicule.id == data.vehicule_id).first()
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")

    entretien = Entretien(
        vehicule_id=data.vehicule_id,
        type_entretien=data.type_entretien,
        kilometrage=data.kilometrage,
        cout=data.cout or 0.0,
        notes=data.notes,
        date_entretien=datetime.now()
    )
    db.add(entretien)

    # Mettre à jour la date du dernier entretien
    vehicule.date_dernier_entretien = entretien.date_entretien
    vehicule.kilometrage = data.kilometrage

    db.commit()
    db.refresh(entretien)

    # Recalculer score + alertes
    calculer_score_sante(data.vehicule_id, db)
    generer_alertes_vehicule(data.vehicule_id, db)

    return entretien


def historique_entretiens(db: Session, vehicule_id: int):
    return db.query(Entretien).filter(Entretien.vehicule_id == vehicule_id).order_by(Entretien.date_entretien.desc()).all()