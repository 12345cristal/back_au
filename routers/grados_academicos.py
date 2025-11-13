# routers/grados_academicos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from models.grados_academicos import GradoAcademico
from schemas.grados_academicos import GradoAcademicoOut
from core.security import require_role

router = APIRouter(
    prefix="/grados-academicos",
    tags=["Grados Académicos"]
)

@router.get("/", response_model=List[GradoAcademicoOut])
def listar_grados(
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):
    return db.query(GradoAcademico).order_by(GradoAcademico.nombre).all()
