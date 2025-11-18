from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from database.base import Base
from sqlalchemy.sql import func

class CitaTipo(Base):
    __tablename__ = "cita_tipos"

    id_tipo = Column(Integer, primary_key=True, index=True)
    nombre_tipo = Column(String(150), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    creado_en = Column(TIMESTAMP, server_default=func.current_timestamp())
