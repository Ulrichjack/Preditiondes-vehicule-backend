# app/services/alerte_service.py
from sqlalchemy.orm import Session
from app.models.alerte import Alerte, TypeAlerte, PrioriteAlerte
from app.models.vehicule import Vehicule
from datetime import datetime, timedelta


def generer_alertes_vehicule(vehicule_id: int, db: Session):
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    if not vehicule:
        return

    # Supprimer les anciennes alertes non résolues de ce véhicule
    db.query(Alerte).filter(
        Alerte.vehicule_id == vehicule_id,
        Alerte.date_resolution.is_(None)
    ).delete()

    alertes = []

    # 1. Score critique
    if vehicule.score_sante < 50:
        alertes.append(Alerte(
            vehicule_id=vehicule_id,
            type_alerte=TypeAlerte.SCORE_CRITIQUE,
            priorite=PrioriteAlerte.URGENTE,
            message=f"Score santé critique : {vehicule.score_sante}/100 – Véhicule à immobiliser"
        ))

    # 2. Entretien en retard (> 3 mois ou > 5000 km)
    if vehicule.date_dernier_entretien:
        jours = (datetime.now() - vehicule.date_dernier_entretien).days
        km_depuis = vehicule.kilometrage - vehicule.kilometrage  # à améliorer avec historique
        if jours > 90:
            alertes.append(Alerte(
                vehicule_id=vehicule_id,
                type_alerte=TypeAlerte.ENTRETIEN_DU,
                priorite=PrioriteAlerte.HAUTE,
                message=f"Entretien en retard de {jours} jours"
            ))

    # Sauvegarder les alertes
    for alerte in alertes:
        db.add(alerte)
    db.commit()