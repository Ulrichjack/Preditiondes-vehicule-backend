# test_en_vrai.py
"""
TEST COMPLET EN VRAI – Scénario réaliste
Lance avec : python test_en_vrai.py
"""

from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.database import engine
from app.models.vehicule import Vehicule, StatutVehicule
from app.models.chauffeur import Chauffeur, StatutChauffeur
from app.models.affectation import Affectation
from app.models.entretien import Entretien, TypeEntretien
from app.models.reparation import Reparation, TypePanne, GraviteReparation
from app.models.alerte import Alerte, TypeAlerte, PrioriteAlerte

# Ouvre une session (comme un panier pour ajouter des objets)
db = Session(engine)

print("DÉBUT DU TEST EN VRAI")
print("=" * 60)

# 1. Créer un chauffeur
print("1. Création du chauffeur Koffi Jean...")
koffi = Chauffeur(
    nom="Koffi",
    prenom="Jean",
    telephone="+2250712345678",
    email="koffi@example.com",
    numero_permis="CIV-123456789",
    date_expiration_permis=datetime(2027, 12, 31).date(),
    statut=StatutChauffeur.ACTIF
)
db.add(koffi)
db.commit()
db.refresh(koffi)
print(f"   → {koffi}")

# 2. Créer un véhicule
print("\n2. Création de la Toyota Corolla...")
toyota = Vehicule(
    immatriculation="AB-123-CD",
    marque="Toyota",
    modele="Corolla",
    annee=2021,
    kilometrage=85000,
    statut=StatutVehicule.DISPONIBLE,
    score_sante=68.5
)
db.add(toyota)
db.commit()
db.refresh(toyota)
print(f"   → {toyota}")

# 3. Affecter le véhicule au chauffeur
print("\n3. Koffi prend la voiture en mission...")
mission = Affectation(
    chauffeur_id=koffi.id,
    vehicule_id=toyota.id,
    mission="Livraison urgente à Yamoussoukro",
    kilometrage_depart=85000
)
db.add(mission)
db.commit()
print(f"   → Mission créée !")

# Mettre à jour le statut du véhicule
toyota.statut = StatutVehicule.EN_MISSION
db.commit()

# 4. Ajouter un entretien récent
print("\n4. Entretien fait il y a 2 mois...")
entretien = Entretien(
    vehicule_id=toyota.id,
    date_entretien=datetime.now(timezone.utc) - timedelta(days=60),
    type_entretien=TypeEntretien.VIDANGE,
    kilometrage=84000,
    cout=45000,
    notes="Vidange + filtre à huile"
)
db.add(entretien)
db.commit()

# 5. Ajouter une réparation grave (va déclencher une alerte !)
print("\n5. Réparation critique : freins HS !")
reparation = Reparation(
    vehicule_id=toyota.id,
    date_reparation=datetime.now(timezone.utc) - timedelta(days=10),
    type_panne=TypePanne.FREINS,
    gravite=GraviteReparation.CRITIQUE,
    kilometrage=84900,
    cout=380000,
    description="Plaquettes et disques avant complètement usés",
    pieces_remplacees="Kit freinage complet"
)
db.add(reparation)
db.commit()

# 6. Créer une alerte automatique
print("\n6. Alerte automatique générée !")
alerte = Alerte(
    vehicule_id=toyota.id,
    type_alerte=TypeAlerte.SCORE_CRITIQUE,
    priorite=PrioriteAlerte.URGENTE,
    message="Réparation critique des freins + score santé bas (68.5%) → Véhicule à immobiliser !"
)
db.add(alerte)
db.commit()

print("\n" + "=" * 60)
print("TOUT EST CRÉÉ ! Voici le résumé :")
print("=" * 60)

# AFFICHAGE FINAL – LA MAGIE
print(f"Chauffeur      : {koffi.nom} {koffi.prenom}")
print(f"Véhicule       : {toyota.immatriculation} – {toyota.marque} {toyota.modele}")
print(f"Statut         : {toyota.statut.value}")
print(f"Kilométrage    : {toyota.kilometrage} km")
print(f"Score santé    : {toyota.score_sante}/100")
print(f"Mission        : {mission.mission}")
print(f"ALERTE         : {alerte.priorite.value} → {alerte.message}")

print("\nOuvre ta base pour voir tout ça en vrai :")
print("sqlite3 parc_automobile.db")
print("→ puis tape : SELECT * FROM alertes;")

db.close()
print("\nFIN DU TEST – TU AS UNE VRAIE BASE QUI VIT !")