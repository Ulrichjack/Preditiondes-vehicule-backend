from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):

    #base de donne
    DATABASE_URL: str = "sqlite:///./parc_automobile.db"

    #seuils et score
    SEUIL_KM_ENTRETIEN: int = 10000
    SEUIL_KM_ALERTE_AVANT: int = 1000
    SEUIL_MOIS_ENTRETIEN: int = 6
    SEUIL_MOIS_ALERTE_AVANT: int = 1

    # Score de sante
    SCRORE_CRITIQUE: int = 50
    SCRORE_ATTENTION: int = 70

    #ce qui indique au code python ou se trouve .env
    model_config = {
        "env_file": str(Path(__file__).parent.parent/".env"),
        "env_file_encoding": "utf-8",
        "case_sensitive":False,
        "extra": "ignore",

    }

# Instance globale qu'on va importer partout
settings = Settings()