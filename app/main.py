from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import vehicules, chauffeurs, affectations, entretiens, reparations, alertes, dashboard, cours, questions

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestion Parc Automobile",
    description="API pour gérer un parc de véhicules avec prédiction de pannes",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(vehicules.router)
app.include_router(chauffeurs.router)
app.include_router(affectations.router)
app.include_router(entretiens.router)
app.include_router(reparations.router)
app.include_router(alertes.router)
app.include_router(dashboard.router)
app.include_router(cours.router)
app.include_router(questions.router)


@app.get("/")
def root():
    return {
        "message": "API Gestion Parc Automobile",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}