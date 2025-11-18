from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from core.security import require_role
from models.roles import Rol
from schemas.roles import RolOut

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RolOut])
def listar_roles(
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):
    return db.query(Rol).order_by(Rol.nombre_rol).all()
