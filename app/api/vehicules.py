from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.vehicule_service import (
    creer_vehicule, lire_vehicule, lister_vehicules,
    mettre_a_jour_vehicule, supprimer_vehicule
)
from app.services.prediction_service import calculer_score_sante
from app.schemas.vehicule import (
    VehiculeCreate, VehiculeUpdate, VehiculeResponse
)
from app.database import get_db
from app.services.prediction_service import predire_prochaine_panne, analyser_vehicule

router = APIRouter(prefix="/vehicules", tags=["Vehicules"])


@router.post("/", response_model=VehiculeResponse, status_code=status.HTTP_201_CREATED)
def create(data: VehiculeCreate, db: Session = Depends(get_db)):
    """Créer un nouveau véhicule"""
    return creer_vehicule(db, data)


@router.get("/", response_model=List[VehiculeResponse])
def lister(
        skip: int = 0,
        limit: int = 100,
        statut: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Lister tous les véhicules avec filtres optionnels"""
    return lister_vehicules(db, skip=skip, limit=limit, statut=statut)


@router.get("/{vehicule_id}", response_model=VehiculeResponse)
def obtenir(vehicule_id: int, db: Session = Depends(get_db)):
    """Obtenir un véhicule par son ID"""
    return lire_vehicule(db, vehicule_id)


@router.put("/{vehicule_id}", response_model=VehiculeResponse)
def modifier(vehicule_id: int, data: VehiculeUpdate, db: Session = Depends(get_db)):
    """Modifier un véhicule existant"""
    return mettre_a_jour_vehicule(db, vehicule_id, data)


@router.delete("/{vehicule_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer(vehicule_id: int, db: Session = Depends(get_db)):
    """Supprimer un véhicule"""
    supprimer_vehicule(db, vehicule_id)
    return None


@router.get("/{vehicule_id}/score")
def obtenir_score(vehicule_id: int, db: Session = Depends(get_db)):
    """Obtenir le score de santé d'un véhicule"""
    score = calculer_score_sante(vehicule_id, db)

    if score < 50:
        etat = "CRITIQUE"
        recommandation = "Immobiliser le véhicule et faire une inspection complète"
    elif score < 70:
        etat = "MOYEN"
        recommandation = "Surveiller de près et planifier un entretien"
    else:
        etat = "BON"
        recommandation = "Continuer l'entretien régulier"

    return {
        "score": round(score, 1),
        "etat": etat,
        "recommandation": recommandation
    }


@router.get("/{vehicule_id}/prediction")
def obtenir_prediction(vehicule_id: int, db: Session = Depends(get_db)):
    """Prédire la prochaine panne d'un véhicule"""
    return predire_prochaine_panne(vehicule_id, db)


@router.get("/{vehicule_id}/analyse")
def analyse_complete(vehicule_id: int, db: Session = Depends(get_db)):
    """Analyse complète d'un véhicule (score, prédiction, coûts)"""
    return analyser_vehicule(vehicule_id, db)