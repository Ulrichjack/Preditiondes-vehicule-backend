from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

if TYPE_CHECKING:
    from .cours import Cours


class Question(Base):
    __tablename__ = "questions"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    reponse_attendue = Column(Text, nullable=True)
    
    # timestamps automatiques
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    
    # relation (many-to-one)
    # une question appartient à un cours
    cours: "Cours" = relationship("Cours", back_populates="questions")

    def __repr__(self) -> str:
        return f"<Question {self.id} - Cours {self.cours_id}>"
