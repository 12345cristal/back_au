# models/citas.py
from sqlalchemy import Column, Integer, Date, Time, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)

    # Niño formal registrado
    id_nino = Column(Integer, ForeignKey("ninos.id_nino", onupdate="CASCADE", ondelete="SET NULL"))

    # Niño prospecto
    id_nino_prospecto = Column(
        Integer,
        ForeignKey("ninos_prospecto.id_nino_prospecto", onupdate="CASCADE", ondelete="SET NULL")
    )

    # Nombre libre (cuando no quieres ni nino formal ni prospecto)
    nombre_nino_libre = Column(String(150))

    # Terapeuta / personal
    id_personal = Column(Integer, ForeignKey("personal.id_personal", onupdate="CASCADE", ondelete="SET NULL"))

    # Terapia/área sugerida (puede estar vacía al inicio)
    id_terapia = Column(Integer, ForeignKey("terapias.id_terapia", onupdate="CASCADE", ondelete="SET NULL"))

    # Tipo de cita (valoración, observación, etc.)
    id_tipo = Column(Integer, ForeignKey("cita_tipos.id_tipo", onupdate="CASCADE", ondelete="SET NULL"))

    fecha = Column(Date)
    hora = Column(Time)
    tipo = Column(String(50))   # lo puedes dejar como texto libre si quieres, o luego eliminar si usas id_tipo
    notas = Column(Text)
    estado = Column(String(50), default="Programada")

    # Relaciones
    nino = relationship("Nino", backref="citas", foreign_keys=[id_nino])
    nino_prospecto = relationship("NinoProspecto", backref="citas", foreign_keys=[id_nino_prospecto])
    personal = relationship("Personal", backref="citas")
    terapia = relationship("Terapia", backref="citas")
    tipo_cita = relationship("CitaTipo", backref="citas")
