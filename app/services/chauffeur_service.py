from sqlalchemy.orm import Session
from app.models.chauffeur import Chauffeur
from app.schemas.chauffeur import ChauffeurCreate, ChauffeurUpdate
from fastapi import HTTPException, status
from typing import List


def creer_chauffeur(db:Session, data: ChauffeurCreate) -> Chauffeur:

    #verifier telephone unique
    existe = db.query(Chauffeur).filter(Chauffeur.telephone == data.telephone).first()
    if existe:
        raise HTTPException(status_code =400, detail="Le chauffeur avec ce numéro de téléphone existe déjà.")

    existe = db.query(Chauffeur).filter(Chauffeur.numero_permis == data.numero_permis).first()
    if existe:
        raise HTTPException(status_code =400, detail="Le chauffeur avec ce numéro de permis existe déjà.")

    nouveau = Chauffeur(
        nom = data.nom,
        prenom = data.prenom,
        telephone = data.telephone,
        numero_permis = data.numero_permis,
        email  = data.email,
        date_expiration_permis = data.date_expiration_permis,
        statut = "ACTIF"
    )

    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

def lire_chauffeur(db:Session, chauffeur_id: int) -> Chauffeur:
    chauffeur = db.query(Chauffeur).filter(Chauffeur.id == chauffeur_id).first()
    if not chauffeur:
        raise HTTPException(status_code=404, detail="Chauffeur non trouvé.")
    return chauffeur

def lister_chauffeurs(db: Session, statut: str = None) -> List[Chauffeur]:
    query = db.query(Chauffeur)
    if statut:
        query = query.filter(Chauffeur.statut == status.upper())
    return query.all()

def mettre_a_jour_chauffeur(db: Session, chauffeur_id: int, data: ChauffeurUpdate) -> Chauffeur:
    chauffeur = lire_chauffeur(db, chauffeur_id)

    if data.telephone is not None:
        autre = (db.query(Chauffeur).filter(
            Chauffeur.telephone == data.telephone,
            Chauffeur.id != chauffeur_id
        ).first())
        if autre:
            raise HTTPException(status_code=400, detail="Le numéro de téléphone est déjà utilisé par un autre chauffeur.")
        chauffeur.telephone = data.telephone

    if data.email is not None:
        chauffeur.email = data.email
    if data.statut is not None:
        chauffeur.statut = data.statut.upper()
    if data.date_expiration_permis is not None:
        chauffeur.date_expiration_permis = data.date_expiration_permis

    db.commit()
    db.refresh(chauffeur)
    return chauffeur
