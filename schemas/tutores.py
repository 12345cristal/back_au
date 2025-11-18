from pydantic import BaseModel
from typing import Optional


# =============================
# 📌 Base (campos editables)
# =============================
class TutorBase(BaseModel):
    id_usuario: int
    ine: Optional[str] = None
    curp: Optional[str] = None
    parentesco: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    comprobante_domicilio: Optional[str] = None
    telefono_emergencia: Optional[str] = None


# =============================
# 📌 Crear tutor
# =============================
class TutorCreate(TutorBase):
    pass


# =============================
# 📌 Actualizar tutor
# =============================
class TutorUpdate(BaseModel):
    ine: Optional[str] = None
    curp: Optional[str] = None
    parentesco: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    comprobante_domicilio: Optional[str] = None
    telefono_emergencia: Optional[str] = None

    id_usuario: Optional[int] = None


# =============================
# 📌 Respuesta
# =============================
class TutorResponse(TutorBase):
    id_tutor: int

    model_config = {
        "from_attributes": True
    }
