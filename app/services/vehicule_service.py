from sqlalchemy.orm import Session
from app.models.vehicule import Vehicule
from app.schemas.vehicule import VehiculeCreate, VehiculeUpdate
from fastapi import HTTPException, status
from typing import List, Optional


def creer_vehicule(db: Session, data: VehiculeCreate) -> Vehicule:
    existe = db.query(Vehicule).filter(
        Vehicule.immatriculation == data.immatriculation
    ).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un véhicule avec cette immatriculation existe déjà."
        )
    nouveau_vehicule = Vehicule(
        immatriculation=data.immatriculation,
        marque=data.marque,
        modele=data.modele,
        annee=data.annee,
        kilometrage=data.kilometrage or 0,
        date_dernier_entretien=data.date_dernier_entretien,
        statut="DISPONIBLE",
        score_sante=100
    )
    db.add(nouveau_vehicule)
    db.commit()
    db.refresh(nouveau_vehicule)
    return nouveau_vehicule


def lire_vehicule(db: Session, vehicule_id: int) -> Vehicule:
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    if not vehicule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule non trouvé."
        )
    return vehicule


def lister_vehicules(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        statut: Optional[str] = None
) -> List[Vehicule]:
    """Liste les véhicules avec pagination et filtre optionnel"""
    query = db.query(Vehicule)

    # Filtre par statut si fourni
    if statut:
        query = query.filter(Vehicule.statut == statut.upper())

    # Pagination
    return query.offset(skip).limit(limit).all()


def mettre_a_jour_vehicule(db: Session, vehicule_id: int, data: VehiculeUpdate) -> Vehicule:
    vehicule = lire_vehicule(db, vehicule_id)

    if data.kilometrage is not None:
        vehicule.kilometrage = data.kilometrage
    if data.date_dernier_entretien is not None:
        vehicule.date_dernier_entretien = data.date_dernier_entretien
    if data.statut is not None:
        vehicule.statut = data.statut.upper()

    db.commit()
    db.refresh(vehicule)
    return vehicule


def supprimer_vehicule(db: Session, vehicule_id: int):
    vehicule = lire_vehicule(db, vehicule_id)
    db.delete(vehicule)
    db.commit()
    return {"detail": "Véhicule supprimé avec succès."}