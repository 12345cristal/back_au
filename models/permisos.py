from sqlalchemy import Column, Integer, String, Text
from database.base import Base


class Permiso(Base):
    __tablename__ = "permisos"

    id_permiso = Column(Integer, primary_key=True, index=True)
    nombre_permiso = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
