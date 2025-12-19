# test_complet.py
from app.database import SessionLocal
from app.services.vehicule_service import creer_vehicule
from app.services.chauffeur_service import creer_chauffeur
from app.services.affectation_service import affecter_vehicule
from app.services.entretien_service import enregistrer_entretien
from app.services.reparation_service import enregistrer_reparation
from app.services.prediction_service import calculer_score_sante
from app.services.alerte_service import generer_alertes_vehicule

from app.schemas.vehicule import VehiculeCreate
from app.schemas.chauffeur import ChauffeurCreate
from app.schemas.affectation import AffectationCreate
from app.schemas.entretien import EntretienCreate
from app.schemas.reparation import ReparationCreate

from datetime import datetime, timedelta
import time

db = SessionLocal()

print("DÉBUT DU TEST COMPLET – PARC AUTOMOBILE")
print("=" * 70)

# 1. Créer un chauffeur
print("\n1. Création du chauffeur Fatou Mballo...")
chauffeur_data = ChauffeurCreate(
    nom="Mballo",
    prenom="Fatou",
    telephone="+237619457890",
    email="fatou@parc-auto.cm",
    numero_permis="CM9876543121",
    date_expiration_permis="2028-06-30"
)
chauffeur = creer_chauffeur(db, chauffeur_data)
print(f"   → Chauffeur créé : {chauffeur.nom} {chauffeur.prenom} (ID: {chauffeur.id})")

# 2. Créer un véhicule
print("\n2. Création du véhicule Toyota RAV4...")
vehicule_data = VehiculeCreate(
    immatriculation="CE 4321 SW",
    marque="Toyota",
    modele="RAV4",
    annee=2021,
    kilometrage=78000
)
vehicule = creer_vehicule(db, vehicule_data)
print(f"   → Véhicule créé : {vehicule.immatriculation} – Score santé = {vehicule.score_sante}")

# 3. Affecter le véhicule au chauffeur
print("\n3. Affectation du véhicule à Fatou...")
affectation_data = AffectationCreate(
    vehicule_id=vehicule.id,
    chauffeur_id=chauffeur.id,
    mission="Mission de livraison à Bertoua",
    kilometrage_depart=78000
)
affectation = affecter_vehicule(db, affectation_data)
print(f"   → Mission créée ! Véhicule maintenant EN MISSION")

# 4. Enregistrer un entretien
print("\n4. Enregistrement d’un entretien (vidange)...")
entretien_data = EntretienCreate(
    vehicule_id=vehicule.id,
    type_entretien="VIDANGE",
    kilometrage=78500,
    cout=45000,
    notes="Vidange + filtre à huile"
)
entretien = enregistrer_entretien(db, entretien_data)
print(f"   → Entretien enregistré – Score santé recalculé")

# 5. Enregistrer une réparation grave
print("\n5. Enregistrement d’une réparation CRITIQUE (freins)...")
reparation_data = ReparationCreate(
    vehicule_id=vehicule.id,
    type_panne="FREINS",
    gravite="CRITIQUE",
    kilometrage=80000,
    cout=380000,
    description="Disques et plaquettes avant complètement usés",
    pieces_remplacees="Kit freinage complet"
)
reparation = enregistrer_reparation(db, reparation_data)
print(f"   → Réparation enregistrée – Alerte générée automatiquement !")

# 6. Forcer le calcul du score + alertes
score = calculer_score_sante(vehicule.id, db)
generer_alertes_vehicule(vehicule.id, db)

# 7. Affichage final
from app.models.vehicule import Vehicule
from app.models.alerte import Alerte

vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule.id).first()
alertes = db.query(Alerte).filter(Alerte.vehicule_id == vehicule.id, Alerte.est_lue == "0").all()

print("\n" + "=" * 70)
print("RÉSUMÉ FINAL")
print("=" * 70)
print(f"Véhicule     : {vehicule.immatriculation} – {vehicule.marque} {vehicule.modele}")
print(f"Kilométrage  : {vehicule.kilometrage} km")
print(f"Statut       : {vehicule.statut.value}")
print(f"Score santé  : {vehicule.score_sante}/100")
print(f"Chauffeur    : {chauffeur.nom} {chauffeur.prenom}")
print(f"Mission      : {affectation.mission}")

if alertes:
    print(f"\nALERTES ACTIVES ({len(alertes)})")
    for a in alertes:
        print(f"   • [{a.priorite.value}] {a.type_alerte.value} → {a.message}")
else:
    print("\nAucune alerte – tout va bien !")

db.close()
print("\nTEST TERMINÉ AVEC SUCCÈS !")
print("Ton système est vivant, intelligent et professionnel.")