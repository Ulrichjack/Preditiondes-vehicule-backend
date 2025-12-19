from datetime import datetime, timezone
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, DateTime, String, Float, Enum as SQLEnum, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base

if TYPE_CHECKING:
    from .vehicule import Vehicule


class GraviteReparation(str, enum.Enum):
    FAIBLE = "FAIBLE"
    MOYENNE = "MOYENNE"
    ELEVEE = "ELEVEE"
    CRITIQUE = "CRITIQUE"


class TypePanne(str, enum.Enum):
    MOTEUR = "MOTEUR"
    FREINS = "FREINS"
    ELECTRICITE = "ELECTRICITE"
    SUSPENSION = "SUSPENSION"
    CARROSSERIE = "CARROSSERIE"
    AUTRE = "AUTRE"


class Reparation(Base):
    __tablename__ = "reparations"
    __allow_unmapped__ = True   # Ligne magique

    id = Column(Integer, primary_key=True, index=True)

    # Lien avec le véhicule
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"), nullable=False)

    date_reparation = Column(DateTime, nullable=False)
    type_panne = Column(SQLEnum(TypePanne), nullable=False)
    gravite = Column(SQLEnum(GraviteReparation), nullable=False)
    kilometrage = Column(Integer, nullable=False)
    cout = Column(Float, default=0.0)
    description = Column(Text, nullable=False)
    pieces_remplacees = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Relation inverse
    vehicule: "Vehicule" = relationship("Vehicule", back_populates="reparations")

    def __repr__(self) -> str:
        return f"<Reparation {self.type_panne.value} [{self.gravite.value}] - {self.cout} FCFA>"