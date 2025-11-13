# core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.session import get_db
from models.usuarios import Usuario
from models.roles import Rol
from config.settings import settings

# ============================
# 🔐 CONFIGURACIÓN
# ============================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ============================
# 🔑 HASH CONTRASEÑA
# ============================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ============================
# 🔑 CREAR TOKEN
# ============================
def create_access_token(data: dict, expires: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

# ============================
# 👤 USUARIO ACTUAL
# ============================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    cred_exc = HTTPException(
        status_code=401,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not user:
        raise cred_exc

    return user

# ============================
# 🔒 VALIDACIÓN DE ROLES
# ============================
def require_role(roles: list[str] | None = None):
    def checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        rol = db.query(Rol).filter(Rol.id_rol == current_user.id_rol).first()

        if not rol:
            raise HTTPException(403, "El usuario no tiene rol asignado")

        if roles and rol.nombre_rol not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado. Rol requerido: {roles}"
            )

        return current_user

    return checker
