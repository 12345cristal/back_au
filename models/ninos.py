from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Nino(Base):
    __tablename__ = "ninos"

    id_nino = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50))
    apellido_materno = Column(String(50))
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)  # ✔ AGREGADO
    sexo = Column(String(20))
    id_tutor = Column(Integer, ForeignKey("tutores.id_tutor", onupdate="CASCADE", ondelete="CASCADE"))
    id_usuario_responsable = Column(Integer, ForeignKey("usuarios.id_usuario", onupdate="CASCADE", ondelete="SET NULL"))
    id_escuela = Column(Integer, ForeignKey("escuelas.id_escuela", onupdate="CASCADE", ondelete="SET NULL"))
    grado_escolar = Column(String(50))
    diagnostico_principal = Column(String(255))
    diagnostico_archivo = Column(String(255))
    alergias = Column(Text)
    observaciones_generales = Column(Text)
    fotografia = Column(String(255))
    activo = Column(Integer, default=1)

    tutor = relationship("Tutor", backref="ninos")
    usuario_responsable = relationship("Usuario", backref="ninos_responsables", foreign_keys=[id_usuario_responsable])
    escuela = relationship("Escuela", backref="ninos")
