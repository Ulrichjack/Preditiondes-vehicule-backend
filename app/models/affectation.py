import enum
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..database import Base

if TYPE_CHECKING:
    from .chauffeur import Chauffeur
    from .vehicule import Vehicule


class StatutAffectation(str,enum.Enum):
       EN_COURS = "EN_COURS"
       TERMINEE = "TERMINEE"
       ANNULEE = "ANNULEE"





class Affectation(Base):

    __tablename__ = "affectations"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)

    chauffeur_id = Column(Integer, ForeignKey("chauffeurs.id"), nullable=False)
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"), nullable=False)

    date_debut = Column(DateTime, default=lambda:datetime.now(timezone.utc),nullable=False)
    date_fin = Column(DateTime, nullable=True)

    mission = Column(String, nullable=True)
    kilometrage_depart = Column(Integer, nullable=True)
    kilometrage_retour = Column(Integer, nullable=True)


    statut = Column(SQLEnum(StatutAffectation), default=StatutAffectation.EN_COURS.value)

    #timestamps automatiques
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    #relation (many-to-one)
    chauffeur: "Chauffeur" = relationship("Chauffeur", back_populates="affectations")
    vehicule: "Vehicule" = relationship("Vehicule", back_populates="affectations")

    def __repr__(self) -> str:
        return f"<Affectation {self.chauffeur_id} → {self.vehicule_id}>"