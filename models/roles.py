from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.base import Base
class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    usuarios = relationship("Usuario", back_populates="rol")
