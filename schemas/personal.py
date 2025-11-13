from pydantic import BaseModel
from typing import Optional

class PersonalBase(BaseModel):
    id_usuario: int
    id_grado: Optional[int]
    especialidades: Optional[str]
    telefono_personal: Optional[str]
    correo_personal: Optional[str]
    rfc: Optional[str]
    ine: Optional[str]
    curp: Optional[str]
    domicilio_calle: Optional[str]
    domicilio_colonia: Optional[str]
    domicilio_cp: Optional[str]
    domicilio_municipio: Optional[str]
    domicilio_estado: Optional[str]
    experiencia: Optional[str]

class PersonalListItem(BaseModel):
    id_personal: int
    nombre: str
    email: str
    rol: str
    grado_academico: Optional[str]
    telefono: Optional[str]
    activo: bool
    foto: Optional[str]

    class Config:
        from_attributes = True

class PersonalDetalle(BaseModel):
    id_personal: int
    id_usuario: int
    nombre: str
    apellido_paterno: Optional[str]
    apellido_materno: Optional[str]
    correo: str
    telefono: Optional[str]
    rol: str
    foto_perfil: Optional[str]
    activo: bool
    fecha_nacimiento: Optional[str]
    fecha_ingreso: Optional[str]
    grado_academico: Optional[str]
    especialidades: Optional[str]
    telefono_personal: Optional[str]
    correo_personal: Optional[str]
    rfc: Optional[str]
    ine: Optional[str]
    curp: Optional[str]
    domicilio_calle: Optional[str]
    domicilio_colonia: Optional[str]
    domicilio_cp: Optional[str]
    domicilio_municipio: Optional[str]
    domicilio_estado: Optional[str]
    cv_archivo: Optional[str]
    comprobante_domicilio: Optional[str]
    experiencia: Optional[str]

    class Config:
        from_attributes = True
