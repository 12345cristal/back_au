from pydantic import BaseModel, EmailStr
from typing import Optional


# 🧱 Base compartida por todos los esquemas
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    id_rol: int


# 🟢 Para crear nuevos usuarios
class UsuarioCreate(UsuarioBase):
    contrasena: str


# 🟡 Para actualizar usuarios existentes
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    id_rol: Optional[int] = None
    activo: Optional[bool] = None


# 🔵 Para devolver usuarios (respuesta de la API)
class UsuarioOut(UsuarioBase):
    id_usuario: int
    activo: bool

    class Config:
        from_attributes = True  # o orm_mode = True si usas FastAPI < 0.110
