from pydantic import BaseModel
from typing import Optional


class PermisoBase(BaseModel):
    nombre_permiso: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
