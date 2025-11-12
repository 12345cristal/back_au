from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models.usuarios import Usuario
from models.roles import Rol
from config.settings import settings

# ================================================================
# 🔐 Configuración general
# ================================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ================================================================
# 1️⃣ Funciones de contraseña
# ================================================================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print("❌ Error al verificar contraseña:", e)
        return False

# ================================================================
# 2️⃣ Creación de tokens JWT
# ================================================================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print("❌ Error al crear token:", e)
        raise HTTPException(status_code=500, detail="Error al crear token")

# ================================================================
# 3️⃣ Obtener usuario actual desde el token JWT
# ================================================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not user:
        raise credentials_exception
    return user

# ================================================================
# 4️⃣ Validación dinámica de roles
# ================================================================
def require_role(nombres_roles_permitidos: list[str] | None = None):
    """
    ✅ Permite:
    - Cualquier usuario autenticado si no se pasan roles.
    - Solo los roles indicados si se especifican.
    """
    def role_checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        rol_usuario = db.query(Rol).filter(Rol.id_rol == current_user.id_rol).first()
        if not rol_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no tiene un rol asignado."
            )

        # Si no se pasan roles, cualquier usuario autenticado puede entrar
        if not nombres_roles_permitidos:
            return current_user

        if rol_usuario.nombre_rol not in nombres_roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos para acceder. Tu rol: {rol_usuario.nombre_rol}"
            )

        return current_user

    return role_checker
