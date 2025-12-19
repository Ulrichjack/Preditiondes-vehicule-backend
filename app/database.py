from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import settings

#engine creaation du moteur
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,#voir toutes les requetes sql dans la console
    future=True
)

#explique le comportement futur de la session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency pour obtenir une session de base de donnees
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
