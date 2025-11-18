from pydantic import BaseModel

class CitaTipoBase(BaseModel):
    nombre_tipo: str
    descripcion: str | None = None

class CitaTipoCreate(CitaTipoBase):
    pass

class CitaTipoUpdate(BaseModel):
    nombre_tipo: str | None = None
    descripcion: str | None = None

class CitaTipoResponse(CitaTipoBase):
    id_tipo: int

    model_config = {"from_attributes": True}
