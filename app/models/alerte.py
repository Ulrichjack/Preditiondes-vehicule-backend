from datetime import datetime, timezone
import enum

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, Text, String, DateTime
from sqlalchemy.orm import relationship

from ..database import Base

if TYPE_CHECKING:
    from .vehicule import Vehicule



class TypeAlerte(str, enum.Enum):
    ENTRETIEN_DU = "ENTRETIEN_DU"
    KM_TROP_ELEVE = "KM_TROP_ELEVE"
    PANNE_REPETEE = "PANNE_REPETEE"
    SCORE_CRITIQUE = "SCORE_CRITIQUE"
    PERMIS_EXPIRE = "PERMIS_EXPIRE"

class PrioriteAlerte(str, enum.Enum):
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    URGENTE = "URGENTE"


class Alerte(Base):
    __tablename__ = "alertes"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)

    vehicule_id = Column(Integer, ForeignKey("vehicules.id"), nullable=False)
    type_alerte = Column(SQLEnum(TypeAlerte), nullable=False)
    priorite = Column(SQLEnum(PrioriteAlerte), nullable=False)
    message = Column(Text, nullable=False)

    est_lue = Column(String(1),default="0")
    date_creation = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    date_resolution = Column(DateTime, nullable=True)

    vehicule: "Vehicule" = relationship("Vehicule", back_populates="alertes")

    def __repr__(self) -> str:
        return f"<Alete [{self.priorite.value}] {self.type_alerte.value}>"