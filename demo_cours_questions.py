#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité Cours et Questions
Ce script démontre comment un professeur peut créer des cours et poser des questions
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def create_course():
    """Créer un cours sur la maintenance automobile"""
    print("1. Création d'un cours sur la maintenance automobile...")
    response = requests.post(
        f"{BASE_URL}/cours/",
        json={
            "titre": "Maintenance préventive des véhicules",
            "description": "Cours pratique sur l'entretien et la maintenance des véhicules du parc automobile",
            "professeur_nom": "Prof. Jean-Claude Martin"
        }
    )
    course = response.json()
    print(f"   ✓ Cours créé: ID={course['id']}, Titre={course['titre']}")
    return course['id']

def add_questions(course_id):
    """Ajouter des questions au cours"""
    print(f"\n2. Ajout de questions au cours {course_id}...")
    
    questions = [
        {
            "question_text": "Quelle est la fréquence recommandée pour la vidange d'huile moteur?",
            "reponse_attendue": "Tous les 10 000 km ou tous les 6 mois, selon le premier atteint"
        },
        {
            "question_text": "Quels sont les signes d'usure des freins?",
            "reponse_attendue": "Bruits de grincement, pédale molle, vibrations au freinage, témoin lumineux allumé"
        },
        {
            "question_text": "Comment vérifier le niveau de liquide de refroidissement?",
            "reponse_attendue": "Vérifier à froid, niveau entre MIN et MAX sur le vase d'expansion"
        }
    ]
    
    for q in questions:
        response = requests.post(
            f"{BASE_URL}/cours/{course_id}/questions",
            json=q
        )
        question = response.json()
        print(f"   ✓ Question ajoutée: ID={question['id']}")

def list_course_questions(course_id):
    """Lister toutes les questions d'un cours"""
    print(f"\n3. Liste des questions du cours {course_id}:")
    response = requests.get(f"{BASE_URL}/cours/{course_id}/questions")
    questions = response.json()
    
    for i, q in enumerate(questions, 1):
        print(f"\n   Question {i}:")
        print(f"   Q: {q['question_text']}")
        print(f"   R: {q['reponse_attendue']}")

def list_all_courses():
    """Lister tous les cours disponibles"""
    print("\n4. Liste de tous les cours:")
    response = requests.get(f"{BASE_URL}/cours/")
    courses = response.json()
    
    for course in courses:
        print(f"\n   - {course['titre']}")
        print(f"     Professeur: {course['professeur_nom']}")
        print(f"     Description: {course['description']}")

if __name__ == "__main__":
    print("=" * 70)
    print("DÉMONSTRATION: Fonctionnalité Cours et Questions pour Professeurs")
    print("=" * 70)
    
    try:
        course_id = create_course()
        add_questions(course_id)
        list_course_questions(course_id)
        list_all_courses()
        
        print("\n" + "=" * 70)
        print("✓ DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        print("Assurez-vous que le serveur est démarré: uvicorn app.main:app")
