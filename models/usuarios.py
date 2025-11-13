from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    # ================================
    # 📌 Columnas principales
    # ================================
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=True)
    apellido_materno = Column(String(50), nullable=True)

    correo = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)

    telefono = Column(String(20), nullable=True)
    foto_perfil = Column(String(255), nullable=True)

    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    activo = Column(Boolean, default=True)
    ultimo_login = Column(DateTime, nullable=True)

    creado_en = Column(DateTime, nullable=True)
    actualizado_en = Column(DateTime, nullable=True)

    # ================================
    # 🔗 Relaciones
    # ================================

    # Un usuario pertenece a un rol
    rol = relationship("Rol", back_populates="usuarios")

    # Un usuario puede tener un registro en personal (1 a 1)
    personal = relationship("Personal", back_populates="usuario", uselist=False)

    # Si tienes tutores o coordinadores en otras tablas, aquí irían igual:
    # tutor = relationship("Tutor", back_populates="usuario", uselist=False)
    # coordinador = relationship("Coordinador", back_populates="usuario", uselist=False)

    # ================================
    # 🔎 Debug
    # ================================
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre='{self.nombre}', correo='{self.correo}')>"
