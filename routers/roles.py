from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from models.roles import Rol
from schemas.roles import RolOut
from core.security import require_role

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RolOut])
async def listar_roles(
    db: Session = Depends(get_db),
    current_user = require_role()
):
    return db.query(Rol).all()
