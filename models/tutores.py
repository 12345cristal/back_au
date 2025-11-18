from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database.base import Base

class Tutor(Base):
    __tablename__ = "tutores"

    id_tutor = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", onupdate="CASCADE", ondelete="CASCADE"), unique=True)

    ine = Column(String(25))
    curp = Column(String(25))
    parentesco = Column(String(50))
    calle = Column(String(100))
    numero_exterior = Column(String(10))
    colonia = Column(String(100))
    codigo_postal = Column(String(10))
    municipio = Column(String(100))
    estado = Column(String(100))
    comprobante_domicilio = Column(String(255))
    telefono_emergencia = Column(String(20))
    creado_en = Column(TIMESTAMP)

    # Relación con usuario
    usuario = relationship("Usuario", backref="tutor", uselist=False)

    # Relación con niños
    ninos = relationship("Nino", back_populates="tutor_rel")
