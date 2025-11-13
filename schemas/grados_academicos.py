from pydantic import BaseModel

class GradoAcademicoOut(BaseModel):
    id_grado: int
    nombre: str

    class Config:
        from_attributes = True
