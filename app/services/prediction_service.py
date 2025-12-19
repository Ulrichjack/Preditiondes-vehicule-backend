from sqlalchemy.orm import Session
from app.models.vehicule import Vehicule
from app.models.reparation import Reparation
from app.models.entretien import Entretien
from datetime import datetime, timedelta
from typing import Dict, List
from collections import Counter


def calculer_score_sante(vehicule_id: int, db: Session) -> float:
    """Calcule le score de santé d'un véhicule (0-100)"""
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    if not vehicule:
        return 0.0

    score = 100.0
    aujourd_hui = datetime.now()
    six_mois = aujourd_hui - timedelta(days=180)

    # 1. Réparations récentes (6 mois)
    reparations_recentes = db.query(Reparation).filter(
        Reparation.vehicule_id == vehicule_id,
        Reparation.date_reparation >= six_mois
    ).all()

    # Pénalité par réparation
    score -= len(reparations_recentes) * 5

    # 2. Coût des réparations
    cout_total = sum(r.cout for r in reparations_recentes if r.cout)
    score -= cout_total / 100000.0  # -1 point par 100,000 FCFA

    # 3. Entretien en retard ?
    if vehicule.date_dernier_entretien:
        jours_depuis = (aujourd_hui - vehicule.date_dernier_entretien).days
        if jours_depuis > 90:  # Plus de 3 mois
            score -= 10
        elif jours_depuis < 30:  # Entretien très récent
            score += 10

    # 4. Âge du véhicule
    age = aujourd_hui.year - vehicule.annee
    score -= age * 2

    # 5. Bonus si aucune panne en 6 mois
    if not reparations_recentes:
        score += 5

    # 6. Limiter entre 0 et 100
    score = max(0, min(100, round(score, 1)))

    # Sauvegarde
    vehicule.score_sante = score
    db.commit()

    return score


def detecter_pannes_recurrentes(vehicule_id: int, db: Session) -> Dict:
    """Détecte les pannes récurrentes (même type >= 2 fois en 6 mois)"""
    aujourd_hui = datetime.now()
    six_mois = aujourd_hui - timedelta(days=180)

    reparations = db.query(Reparation).filter(
        Reparation.vehicule_id == vehicule_id,
        Reparation.date_reparation >= six_mois
    ).all()

    # Compter par type de panne
    types_pannes = [r.type_panne for r in reparations]
    compteur = Counter(types_pannes)

    # Identifier les récurrences (>= 2)
    recurrences = {type_panne: count for type_panne, count in compteur.items() if count >= 2}

    if recurrences:
        type_plus_frequent = max(recurrences, key=recurrences.get)
        return {
            "a_recurrence": True,
            "type_principal": type_plus_frequent,
            "nombre_occurrences": recurrences[type_plus_frequent],
            "toutes_recurrences": recurrences
        }

    return {"a_recurrence": False}


def predire_prochaine_panne(vehicule_id: int, db: Session) -> Dict:
    """Prédit la prochaine panne probable"""
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    if not vehicule:
        return {"erreur": "Véhicule non trouvé"}

    aujourd_hui = datetime.now()
    six_mois = aujourd_hui - timedelta(days=180)

    # Récupérer les réparations
    reparations = db.query(Reparation).filter(
        Reparation.vehicule_id == vehicule_id,
        Reparation.date_reparation >= six_mois
    ).order_by(Reparation.date_reparation.asc()).all()

    if len(reparations) < 2:
        return {
            "risque_panne": 10,
            "jours_estimes": None,
            "probleme_probable": "INDÉTERMINÉ",
            "confiance": 0.2,
            "message": "Pas assez de données historiques (moins de 2 pannes)",
            "recommandation": "Continuer la surveillance normale"
        }

    # Calculer intervalle moyen entre pannes
    intervalles = []
    for i in range(len(reparations) - 1):
        jours = (reparations[i + 1].date_reparation - reparations[i].date_reparation).days
        if jours > 0:  # ✅ Ignorer les intervalles nuls
            intervalles.append(jours)

    # ✅ Gérer le cas où toutes les pannes sont le même jour
    if not intervalles or sum(intervalles) == 0:
        return {
            "risque_panne": 90,
            "jours_estimes": 0,
            "probleme_probable": "MULTIPLE",
            "confiance": 0.8,
            "message": f"{len(reparations)} pannes en très peu de temps",
            "recommandation": "🚨 CRITIQUE : Immobiliser immédiatement - problème grave"
        }

    intervalle_moyen = sum(intervalles) / len(intervalles)

    # Dernière panne
    derniere_panne = reparations[-1].date_reparation
    jours_depuis_derniere = (aujourd_hui - derniere_panne).days

    # Calculer le risque
    if jours_depuis_derniere > intervalle_moyen:
        risque = min(95, 50 + (jours_depuis_derniere - intervalle_moyen) * 2)
    else:
        # ✅ Protection contre division par zéro
        if intervalle_moyen > 0:
            risque = max(5, (jours_depuis_derniere / intervalle_moyen) * 50)
        else:
            risque = 90  # Risque élevé si intervalle moyen = 0

    # Détecter les pannes récurrentes
    recurrences = detecter_pannes_recurrentes(vehicule_id, db)

    # Ajuster le risque si panne récurrente
    if recurrences["a_recurrence"]:
        risque = min(95, risque * 1.5)

    # Jours estimés avant prochaine panne
    jours_estimes = max(0, int(intervalle_moyen - jours_depuis_derniere))

    # Problème probable
    probleme_probable = recurrences.get("type_principal", "INDÉTERMINÉ")

    # Message contextuel
    if len(reparations) >= 5 and recurrences["a_recurrence"]:
        message = f"{len(reparations)} pannes dont {recurrences['nombre_occurrences']} fois {probleme_probable}"
    elif recurrences["a_recurrence"]:
        message = f"Problème récurrent : {probleme_probable}"
    else:
        message = f"{len(reparations)} pannes en 6 mois"

    # Recommandation
    if risque > 75:
        recommandation = "🚨 URGENT : Inspection immédiate recommandée"
    elif risque > 50:
        recommandation = "⚠️ Planifier une inspection préventive rapidement"
    else:
        recommandation = "✅ Surveillance normale, entretien régulier"

    return {
        "risque_panne": round(risque, 1),
        "jours_estimes": jours_estimes if jours_estimes > 0 else 0,
        "probleme_probable": probleme_probable,
        "confiance": min(0.9, len(reparations) / 10),
        "message": message,
        "recommandation": recommandation,
        "pannes_recurrentes": recurrences,
        "statistiques": {
            "nombre_pannes_6_mois": len(reparations),
            "intervalle_moyen_jours": round(intervalle_moyen, 1) if intervalle_moyen > 0 else 0,
            "jours_depuis_derniere_panne": jours_depuis_derniere
        }
    }

def analyser_vehicule(vehicule_id: int, db: Session) -> Dict:
    """Analyse complète d'un véhicule"""
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    if not vehicule:
        return {"erreur": "Véhicule non trouvé"}

    score = calculer_score_sante(vehicule_id, db)
    prediction = predire_prochaine_panne(vehicule_id, db)
    recurrences = detecter_pannes_recurrentes(vehicule_id, db)

    # Historique des coûts
    six_mois = datetime.now() - timedelta(days=180)
    reparations = db.query(Reparation).filter(
        Reparation.vehicule_id == vehicule_id,
        Reparation.date_reparation >= six_mois
    ).all()

    cout_total = sum(r.cout for r in reparations if r.cout)

    return {
        "vehicule": {
            "id": vehicule.id,
            "immatriculation": vehicule.immatriculation,
            "marque": vehicule.marque,
            "modele": vehicule.modele,
            "kilometrage": vehicule.kilometrage
        },
        "score_sante": score,
        "etat": "CRITIQUE" if score < 50 else "MOYEN" if score < 70 else "BON",
        "prediction": prediction,
        "pannes_recurrentes": recurrences,
        "couts_6_mois": {
            "total": cout_total,
            "nombre_reparations": len(reparations),
            "cout_moyen": round(cout_total / len(reparations), 2) if reparations else 0
        }
    }