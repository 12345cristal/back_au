from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel   # ✅ Faltaba este import
from core.security import hash_password
from database.session import get_db
from models.usuarios import Usuario
from core.security import require_role

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

class PasswordUpdate(BaseModel):
    nueva_contrasena: str

@router.patch("/{id_usuario}/password")
async def actualizar_password(
    id_usuario: int,
    payload: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["Administrador", "Coordinador"]))
):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    user.contrasena_hash = hash_password(payload.nueva_contrasena)
    db.commit()

    return {"mensaje": "Contraseña actualizada"}
