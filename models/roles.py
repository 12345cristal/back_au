from sqlalchemy import Column, Integer, String, Text
from database.base import Base

class Rol(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
