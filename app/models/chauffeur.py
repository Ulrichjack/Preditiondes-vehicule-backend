from datetime import datetime, timezone
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from .affectation import Affectation




class StatutChauffeur(str,enum.Enum):
    ACTIF = "ACTIF"
    INACTIF = "INACTIF"
    EN_CONGE = "EN_CONGE"
    SUSPENDU = "SUSPENDU"


class Chauffeur(Base):
    __tablename__ = "chauffeurs"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    email=Column(String, unique=True, nullable=True)
    numero_permis = Column(String, unique=True, nullable=False)
    date_expiration_permis = Column(Date, nullable=False)

    statut = Column(SQLEnum(StatutChauffeur), default=StatutChauffeur.ACTIF)

    #timestamps automatiques
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    #relation (one-to-many)
    #un chauffeur peut avoir plusieurs affectation
    affectations: list["Affectation"] = relationship(
        "Affectation",
        back_populates="chauffeur",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Chauffeur {self.nom} - {self.telephone}>"
