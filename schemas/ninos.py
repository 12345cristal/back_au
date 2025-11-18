from pydantic import BaseModel
from typing import Optional

class NinoBase(BaseModel):
    id_tutor: int
    nombre: str
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    edad: Optional[int] = None  # ✔ AGREGADO
    sexo: Optional[str] = None
    diagnostico_principal: Optional[str] = None
    diagnostico_archivo: Optional[str] = None
    alergias: Optional[str] = None
    observaciones_generales: Optional[str] = None
    id_escuela: Optional[int] = None
    id_usuario_responsable: Optional[int] = None
    grado_escolar: Optional[str] = None
    fotografia: Optional[str] = None
    activo: Optional[int] = 1

class NinoCreate(NinoBase):
    pass

class NinoUpdate(BaseModel):
    id_tutor: Optional[int] = None
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    edad: Optional[int] = None  # ✔ AGREGADO
    sexo: Optional[str] = None
    diagnostico_principal: Optional[str] = None
    diagnostico_archivo: Optional[str] = None
    alergias: Optional[str] = None
    observaciones_generales: Optional[str] = None
    id_escuela: Optional[int] = None
    id_usuario_responsable: Optional[int] = None
    grado_escolar: Optional[str] = None
    fotografia: Optional[str] = None
    activo: Optional[int] = None

class NinoResponse(NinoBase):
    id_nino: int

    model_config = {
        "from_attributes": True
    }
