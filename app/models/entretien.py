from datetime import datetime, timezone
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..database import Base

if TYPE_CHECKING:
    from .vehicule import Vehicule


class TypeEntretien(str, enum.Enum):
     VIDANGE = "VIDANGE"
     REVISION = "REVISION"
     FREINS = "FREINS"
     PNEUS = "PNEUS"
     CONTROLE_TECHNIQUE = "CONTROLE_TECHNIQUE"
     AUTRE = "AUTRE"

class Entretien(Base):
    __tablename__ = "entretiens"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    vehicule_id = Column(Integer, ForeignKey("vehicules.id"), nullable=False)
    date_entretien = Column(DateTime, nullable=False)
    type_entretien = Column(SQLEnum(TypeEntretien), nullable=False)
    kilometrage = Column(Integer, nullable=False)
    cout = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    prochain_entretien_prevu = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    vehicule: "Vehicule" = relationship("Vehicule", back_populates="entretiens")

    def __repr__(self) -> str:
        return f"<Entretien {self.type_entretien} - {self.vehicule_id}>"