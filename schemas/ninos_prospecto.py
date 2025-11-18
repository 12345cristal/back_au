from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProspectoBase(BaseModel):
    nombre: str
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    edad_aproximada: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    telefono_contacto: Optional[str] = None
    nombre_tutor: Optional[str] = None
    notas: Optional[str] = None


class ProspectoCreate(ProspectoBase):
    pass


class ProspectoUpdate(ProspectoBase):
    pass


class ProspectoResponse(ProspectoBase):
    id_prospecto: int

    model_config = {
        "from_attributes": True
    }
