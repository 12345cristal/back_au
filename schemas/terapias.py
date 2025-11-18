from pydantic import BaseModel
from typing import Optional


# =================================
# 📌 Base (campos comunes)
# =================================
class TerapiaBase(BaseModel):
    nombre_terapia: str
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    costo: Optional[float] = None


# =================================
# 📌 Crear Terapia
# =================================
class TerapiaCreate(TerapiaBase):
    pass


# =================================
# 📌 Actualizar Terapia
# =================================
class TerapiaUpdate(BaseModel):
    nombre_terapia: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    costo: Optional[float] = None


# =================================
# 📌 Respuesta
# =================================
class TerapiaResponse(TerapiaBase):
    id_terapia: int

    model_config = {
        "from_attributes": True
    }
