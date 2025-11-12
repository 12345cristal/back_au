from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.permisos import Permiso
from schemas.permisos import PermisoBase
from core.deps import require_role

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)


# 📋 Listar todos los permisos
@router.get("/", response_model=List[PermisoBase])
def listar_permisos(
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador"]))
):
    permisos = db.query(Permiso).all()
    return permisos


# ➕ Crear nuevo permiso
@router.post("/", response_model=PermisoBase)
def crear_permiso(
    permiso_in: PermisoBase,
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador"]))
):
    existente = db.query(Permiso).filter(Permiso.nombre_permiso == permiso_in.nombre_permiso).first()
    if existente:
        raise HTTPException(status_code=400, detail="El permiso ya existe")

    nuevo_permiso = Permiso(**permiso_in.dict())
    db.add(nuevo_permiso)
    db.commit()
    db.refresh(nuevo_permiso)
    return nuevo_permiso
