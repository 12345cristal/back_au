from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database.base import Base

class Personal(Base):
    __tablename__ = "personal"

    id_personal = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)

    fecha_nacimiento = Column(Date)
    fecha_ingreso = Column(Date)

    id_grado = Column(Integer, ForeignKey("grados_academicos.id_grado", ondelete="SET NULL"))

    especialidades = Column(Text)
    telefono_personal = Column(String(20))
    correo_personal = Column(String(100))

    rfc = Column(String(25))
    ine = Column(String(25))
    curp = Column(String(25))

    domicilio_calle = Column(String(100))
    domicilio_colonia = Column(String(100))
    domicilio_cp = Column(String(10))
    domicilio_municipio = Column(String(100))
    domicilio_estado = Column(String(100))

    cv_archivo = Column(String(255))
    comprobante_domicilio = Column(String(255))
    experiencia = Column(Text)

    usuario = relationship("Usuario", back_populates="personal")
    grado = relationship("GradoAcademico", back_populates="personal")
