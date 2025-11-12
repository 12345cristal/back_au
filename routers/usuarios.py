from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from models.usuarios import Usuario
from schemas.usuarios import UsuarioOut
from core.security import require_role

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioOut])
async def listar_usuarios(
    db: Session = Depends(get_db),
    current_user = require_role()
):
    return db.query(Usuario).all()
