# Guide SQLite - Parc Automobile

## 1. Ouvrir la base de données

```bash
sqlite3 parc_automobile.db
```

## 2. Configuration initiale (à taper une seule fois par session)

```sql
.headers on      -- affiche les noms des colonnes
.mode column     -- met en colonnes (super lisible)
.width auto      -- ajuste la largeur automatiquement
```

## 3. Commandes de navigation (à retenir par cœur)

```sql
.tables                  -- liste toutes les tables
.schema                  -- montre la structure de toutes les tables
.schema vehicules        -- montre seulement la table vehicules
.schema chauffeurs       -- montre seulement la table chauffeurs
```

## 4. Consulter le contenu des tables

```sql
SELECT * FROM vehicules;
SELECT * FROM chauffeurs;
SELECT * FROM affectations;
SELECT * FROM entretiens;
SELECT * FROM reparations;
```

## 5. Filtrer les données (exemples utiles)

```sql
-- Colonnes spécifiques
SELECT immatriculation, marque, statut FROM vehicules;

-- Filtrer par statut
SELECT * FROM vehicules WHERE statut = 'EN_MISSION';

-- Missions en cours
SELECT * FROM affectations WHERE date_fin IS NULL;

-- Entretiens par type
SELECT * FROM entretiens WHERE type_entretien = 'VIDANGE';

-- Réparations critiques
SELECT * FROM reparations WHERE gravite = 'CRITIQUE';
```

## 6. Compter les enregistrements

```sql
-- Nombre total de véhicules
SELECT COUNT(*) FROM vehicules;

-- Chauffeurs actifs
SELECT COUNT(*) FROM chauffeurs WHERE statut = 'ACTIF';
```

## 7. Trier les résultats

```sql
-- Réparations les plus récentes d'abord
SELECT * FROM reparations ORDER BY date_reparation DESC;

-- Véhicules par kilométrage décroissant
SELECT * FROM vehicules ORDER BY kilometrage DESC;
```

## 8. Rechercher avec LIKE (contient)

```sql
-- Rechercher un chauffeur
SELECT * FROM chauffeurs WHERE nom LIKE '%Koffi%';

-- Rechercher une marque
SELECT * FROM vehicules WHERE marque LIKE 'Toyota%';
```

## 9. Joindre plusieurs tables

```sql
-- Voir qui conduit quoi en ce moment
SELECT 
    v.immatriculation, 
    c.nom, 
    c.prenom, 
    a.date_debut
FROM affectations a
JOIN vehicules v ON a.vehicule_id = v.id
JOIN chauffeurs c ON a.chauffeur_id = c.id
WHERE a.date_fin IS NULL;  -- missions en cours
```

## 10. Quitter SQLite

```sql
.quit
```

Ou appuyez sur `Ctrl + D`

---

## LA COMMANDE ULTIME

Copier-coller cette commande pour voir toutes les données importantes :

```bash
sqlite3 parc_automobile.db <<EOF
.headers on
.mode column
.width auto

-- Véhicules
SELECT '=== VÉHICULES ===' AS info;
SELECT id, immatriculation, marque, modele, statut, kilometrage 
FROM vehicules;

-- Chauffeurs
SELECT '', '=== CHAUFFEURS ===';
SELECT id, nom, prenom, telephone, statut 
FROM chauffeurs;

-- Missions en cours
SELECT '', '=== MISSIONS EN COURS ===';
SELECT 
    a.id, 
    v.immatriculation, 
    c.nom || ' ' || c.prenom AS chauffeur, 
    a.date_debut
FROM affectations a
JOIN vehicules v ON a.vehicule_id = v.id
JOIN chauffeurs c ON a.chauffeur_id = c.id
WHERE a.date_fin IS NULL;

-- Derniers entretiens
SELECT '', '=== DERNIERS ENTRETIENS ===';
SELECT 
    e.type_entretien, 
    v.immatriculation, 
    e.date_entretien
FROM entretiens e
JOIN vehicules v ON e.vehicule_id = v.id
ORDER BY e.date_entretien DESC 
LIMIT 5;
EOF
```

---

## Mini-fiche de référence rapide

```sql
-- Configuration
.headers on
.mode column
.width auto

-- Navigation
.tables
.schema vehicules

-- Requêtes courantes
SELECT * FROM vehicules;
SELECT * FROM affectations WHERE date_fin IS NULL;

-- Jointures
SELECT v.immatriculation, c.nom 
FROM affectations a 
JOIN vehicules v 
JOIN chauffeurs c;

-- Quitter
.quit
```

---

## Bonus : Alias pour le terminal

À ajouter dans votre `~/.bashrc` ou `~/.zshrc` :

```bash
# Ouvrir la base avec configuration
alias db='sqlite3 parc_automobile.db ".headers on" ".mode column"'

# Lister les tables
alias tables='sqlite3 parc_automobile.db ".tables"'

# Voir tout en un coup d'œil
alias tout='sqlite3 parc_automobile.db <<EOF
.headers on
.mode column
SELECT "=== VOITURES ===";
SELECT immatriculation, marque, statut FROM vehicules;
SELECT "", "=== MISSIONS EN COURS ===";
SELECT a.id, v.immatriculation, c.nom 
FROM affectations a 
JOIN vehicules v 
JOIN chauffeurs c 
WHERE a.date_fin IS NULL;
EOF'

# Créer les tables (Python/FastAPI)
alias db-create='python -c "
from app.database import Base, engine
from app.models import *
Base.metadata.create_all(bind=engine)
print(\"Toutes les tables sont créées !\")
"'

# Ouvrir la base
alias db-open='sqlite3 parc_automobile.db ".headers on" ".mode column"'

# Lister les tables
alias db-tables='sqlite3 parc_automobile.db ".tables"'
```

Après avoir ajouté ces alias, rechargez votre configuration :

```bash
source ~/.bashrc
# ou
source ~/.zshrc
```