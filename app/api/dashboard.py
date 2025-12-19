from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.vehicule import Vehicule
from app.models.alerte import Alerte
from app.models.reparation import Reparation
from app.database import get_db
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def obtenir_dashboard(db: Session = Depends(get_db)):
    """Statistiques complètes du parc automobile"""

    # Total véhicules par statut
    total = db.query(Vehicule).count()
    disponibles = db.query(Vehicule).filter(Vehicule.statut == "DISPONIBLE").count()
    en_mission = db.query(Vehicule).filter(Vehicule.statut == "EN_MISSION").count()
    en_reparation = db.query(Vehicule).filter(Vehicule.statut == "EN_REPARATION").count()

    # Alertes actives
    alertes_actives = db.query(Alerte).filter(Alerte.date_resolution.is_(None)).count()
    alertes_urgentes = db.query(Alerte).filter(
        Alerte.date_resolution.is_(None),
        Alerte.priorite == "URGENTE"
    ).count()

    # Score moyen du parc
    vehicules = db.query(Vehicule).all()
    score_moyen = sum(v.score_sante for v in vehicules) / len(vehicules) if vehicules else 0

    # Véhicules par état
    vehicules_critiques = db.query(Vehicule).filter(Vehicule.score_sante < 50).all()
    vehicules_attention = db.query(Vehicule).filter(
        Vehicule.score_sante >= 50,
        Vehicule.score_sante < 70
    ).all()
    vehicules_bons = db.query(Vehicule).filter(Vehicule.score_sante >= 70).all()

    # Coûts du mois
    debut_mois = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    reparations_mois = db.query(Reparation).filter(
        Reparation.date_reparation >= debut_mois
    ).all()

    cout_total_mois = sum(r.cout for r in reparations_mois if r.cout)

    # Top 3 véhicules les plus coûteux (6 derniers mois)
    six_mois = datetime.now() - timedelta(days=180)
    top_couts = db.query(
        Vehicule.id,
        Vehicule.immatriculation,
        Vehicule.marque,
        Vehicule.modele,
        func.sum(Reparation.cout).label('cout_total')
    ).join(Reparation).filter(
        Reparation.date_reparation >= six_mois
    ).group_by(Vehicule.id).order_by(func.sum(Reparation.cout).desc()).limit(3).all()

    return {
        "statistiques": {
            "total_vehicules": total,
            "disponibles": disponibles,
            "en_mission": en_mission,
            "en_reparation": en_reparation
        },
        "alertes": {
            "total_actives": alertes_actives,
            "urgentes": alertes_urgentes
        },
        "sante_parc": {
            "score_moyen": round(score_moyen, 1),
            "critiques": len(vehicules_critiques),
            "attention": len(vehicules_attention),
            "bons": len(vehicules_bons)
        },
        "couts_mois": {
            "total": cout_total_mois,
            "nombre_reparations": len(reparations_mois)
        },
        "top_vehicules_couteux": [
            {
                "immatriculation": v.immatriculation,
                "marque": v.marque,
                "modele": v.modele,
                "cout_total_6_mois": float(v.cout_total)
            } for v in top_couts
        ],
        "vehicules_a_surveiller": [
            {
                "id": v.id,
                "immatriculation": v.immatriculation,
                "score": v.score_sante,
                "statut": v.statut
            } for v in vehicules_critiques + vehicules_attention
        ]
    }


