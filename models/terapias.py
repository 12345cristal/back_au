from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP
from database.base import Base

class Terapia(Base):
    __tablename__ = "terapias"

    id_terapia = Column(Integer, primary_key=True, index=True)
    nombre_terapia = Column(String(150), nullable=False)
    descripcion = Column(Text)
    duracion_minutos = Column(Integer)
    costo = Column(DECIMAL(10, 2))
    creado_en = Column(TIMESTAMP)
