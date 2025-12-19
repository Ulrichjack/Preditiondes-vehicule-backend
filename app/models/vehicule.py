from datetime import datetime, timezone
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..database import Base

if TYPE_CHECKING:
    from .entretien import Entretien
    from .reparation import Reparation
    from .affectation import Affectation


class StatutVehicule(str, enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    EN_MISSION = "EN_MISSION"
    EN_REPARATION = "EN_REPARATION"
    HORS_SERVICE = "HORS_SERVICE"


class Vehicule(Base):
    __tablename__ = "vehicules"
    __allow_unmapped__ = True   # LIGNE MAGIQUE QUI RÉSOUT TOUT

    id = Column(Integer, primary_key=True, index=True)
    immatriculation = Column(String, unique=True, index=True, nullable=False)
    marque = Column(String, nullable=False)
    modele = Column(String, nullable=False)
    annee = Column(Integer, nullable=False)
    kilometrage = Column(Integer, default=0, nullable=False)
    date_dernier_entretien = Column(DateTime, nullable=True)

    statut = Column(SQLEnum(StatutVehicule), default=StatutVehicule.DISPONIBLE)
    score_sante = Column(Float, default=100.0, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    entretiens: list["Entretien"] = relationship("Entretien", back_populates="vehicule", cascade="all, delete-orphan")
    reparations: list["Reparation"] = relationship("Reparation", back_populates="vehicule", cascade="all, delete-orphan")
    affectations: list["Affectation"] = relationship("Affectation", back_populates="vehicule", cascade="all, delete-orphan")
    alertes: list["Alerte"] = relationship("Alerte", back_populates="vehicule", cascade="all, delete-orphan")