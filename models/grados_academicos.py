from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class GradoAcademico(Base):
    __tablename__ = "grados_academicos"

    id_grado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, unique=True)

    personal = relationship("Personal", back_populates="grado")
