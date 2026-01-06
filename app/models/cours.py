from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from .question import Question


class Cours(Base):
    __tablename__ = "cours"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    
    titre = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    professeur_nom = Column(String, nullable=False)
    
    # timestamps automatiques
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    
    # relation (one-to-many)
    # un cours peut avoir plusieurs questions
    questions: list["Question"] = relationship(
        "Question",
        back_populates="cours",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cours {self.titre} - {self.professeur_nom}>"
