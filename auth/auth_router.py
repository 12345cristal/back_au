from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.security import verify_password, create_access_token
from database import get_db
from models.usuarios import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# 🧩 Modelo para el cuerpo del login
class LoginData(BaseModel):
    correo: str
    contrasena: str

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    print(f"🟢 Recibido login con correo: {data.correo}, contraseña: {data.contrasena}")

    user = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if not user:
        print("❌ Usuario no encontrado.")
        raise HTTPException(status_code=401, detail="Correo no encontrado")

    print(f"✅ Usuario encontrado: {user.correo}")
    print(f"Hash en BD: {user.contrasena_hash}")

    valido = verify_password(data.contrasena, user.contrasena_hash)
    print(f"¿Contraseña válida?: {valido}")

    if not valido:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({"sub": str(user.id_usuario)})
    print("🔑 Token generado correctamente")

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user.id_usuario,
            "nombre": user.nombre,
            "correo": user.correo,
            "rol": user.id_rol,
        },
    }
