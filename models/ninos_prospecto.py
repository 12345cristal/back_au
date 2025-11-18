from sqlalchemy import Column, Integer, String, Text, Date, Boolean
from database.base import Base

class NinoProspecto(Base):
    __tablename__ = "ninos_prospecto"

    id_prospecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100))
    apellido_materno = Column(String(100))
    edad_aproximada = Column(Integer)
    fecha_nacimiento = Column(Date)
    sexo = Column(String(20))
    telefono_contacto = Column(String(20))
    nombre_tutor = Column(String(150))
    notas = Column(Text)
    activo = Column(Boolean, default=True)   # 👈 agregado
