# Fonctionnalité Cours et Questions

Cette fonctionnalité permet aux professeurs de créer des cours sur des projets et de poser des questions aux étudiants.

## Description

Le système permet aux enseignants de:
- Créer des cours avec un titre, une description et le nom du professeur
- Ajouter des questions à chaque cours avec les réponses attendues
- Gérer (créer, lire, mettre à jour, supprimer) les cours et les questions

## Modèles de données

### Cours (Course)
- `id`: Identifiant unique
- `titre`: Titre du cours
- `description`: Description détaillée (optionnelle)
- `professeur_nom`: Nom du professeur
- `created_at`: Date de création
- `updated_at`: Date de dernière mise à jour

### Question
- `id`: Identifiant unique
- `cours_id`: Référence au cours (clé étrangère)
- `question_text`: Texte de la question
- `reponse_attendue`: Réponse attendue (optionnelle)
- `created_at`: Date de création
- `updated_at`: Date de dernière mise à jour

## Endpoints API

### Gestion des Cours

#### Créer un cours
```http
POST /cours/
Content-Type: application/json

{
  "titre": "Mécanique automobile de base",
  "description": "Cours sur les principes de base de la mécanique",
  "professeur_nom": "Prof. Dupont"
}
```

#### Lister tous les cours
```http
GET /cours/
```

#### Obtenir un cours spécifique
```http
GET /cours/{cours_id}
```

#### Mettre à jour un cours
```http
PUT /cours/{cours_id}
Content-Type: application/json

{
  "titre": "Nouveau titre",
  "description": "Nouvelle description",
  "professeur_nom": "Prof. Martin"
}
```

#### Supprimer un cours
```http
DELETE /cours/{cours_id}
```

### Gestion des Questions

#### Ajouter une question à un cours
```http
POST /cours/{cours_id}/questions
Content-Type: application/json

{
  "question_text": "Quelle est la fréquence recommandée pour une vidange ?",
  "reponse_attendue": "Tous les 10 000 km ou tous les 6 mois"
}
```

#### Lister les questions d'un cours
```http
GET /cours/{cours_id}/questions
```

#### Obtenir une question spécifique
```http
GET /cours/questions/{question_id}
```

#### Mettre à jour une question
```http
PUT /cours/questions/{question_id}
Content-Type: application/json

{
  "question_text": "Nouvelle question ?",
  "reponse_attendue": "Nouvelle réponse"
}
```

#### Supprimer une question
```http
DELETE /cours/questions/{question_id}
```

## Démonstration

Un script de démonstration est disponible dans `demo_cours_questions.py`. Pour l'exécuter:

1. Démarrer le serveur:
```bash
uvicorn app.main:app --reload
```

2. Dans un autre terminal, exécuter le script de démonstration:
```bash
python demo_cours_questions.py
```

Le script va:
1. Créer un cours sur la maintenance automobile
2. Ajouter 3 questions au cours
3. Afficher toutes les questions du cours
4. Lister tous les cours disponibles

## Documentation Interactive

La documentation interactive Swagger est disponible à l'adresse:
```
http://localhost:8000/docs
```

Vous pouvez y tester tous les endpoints directement depuis votre navigateur.

## Exemples d'utilisation

### Avec curl

```bash
# Créer un cours
curl -X POST "http://localhost:8000/cours/" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Conduite défensive",
    "description": "Techniques de conduite sécuritaire",
    "professeur_nom": "Prof. Martin"
  }'

# Ajouter une question
curl -X POST "http://localhost:8000/cours/1/questions" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Quelle est la distance de sécurité recommandée ?",
    "reponse_attendue": "Au moins 2 secondes derrière le véhicule précédent"
  }'

# Lister les questions d'un cours
curl -X GET "http://localhost:8000/cours/1/questions"
```

### Avec Python

```python
import requests

# Créer un cours
response = requests.post(
    "http://localhost:8000/cours/",
    json={
        "titre": "Maintenance préventive",
        "description": "Cours sur l'entretien des véhicules",
        "professeur_nom": "Prof. Durand"
    }
)
cours = response.json()
print(f"Cours créé avec l'ID: {cours['id']}")

# Ajouter une question
response = requests.post(
    f"http://localhost:8000/cours/{cours['id']}/questions",
    json={
        "question_text": "Quand faire la révision ?",
        "reponse_attendue": "Selon le carnet d'entretien du constructeur"
    }
)
question = response.json()
print(f"Question ajoutée avec l'ID: {question['id']}")
```

## Structure du code

```
app/
├── models/
│   ├── cours.py         # Modèle SQLAlchemy pour les cours
│   └── question.py      # Modèle SQLAlchemy pour les questions
├── schemas/
│   ├── cours.py         # Schémas Pydantic pour validation
│   └── question.py      # Schémas Pydantic pour validation
├── services/
│   ├── cours_service.py     # Logique métier pour les cours
│   └── question_service.py  # Logique métier pour les questions
└── api/
    ├── cours.py         # Endpoints REST pour les cours
    └── questions.py     # Endpoints REST pour les questions
```

## Notes

- Toutes les dates sont stockées en UTC
- La suppression d'un cours supprime automatiquement toutes ses questions (cascade)
- Les champs `description` et `reponse_attendue` sont optionnels
- Les validations sont gérées par Pydantic au niveau des schémas
