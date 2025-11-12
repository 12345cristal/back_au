from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import usuarios, roles
from schemas import usuarios as usuarios_schema
from core.deps import get_current_user, require_role

router = APIRouter(
    prefix="/coordinadores",
    tags=["Coordinadores"]
)

@router.get("/", response_model=List[usuarios_schema.UsuarioOut])
def listar_coordinadores(
    db: Session = Depends(get_db),
    _: usuarios.Usuario = Depends(require_role(["Administrador"]))
):
    """
    Devuelve la lista de usuarios con rol 'Coordinador'.
    Solo accesible para usuarios con rol 'Administrador'.
    """
    coordinador_rol = db.query(roles.Rol).filter(roles.Rol.nombre_rol == "Coordinador").first()
    if not coordinador_rol:
        raise HTTPException(status_code=404, detail="No existe el rol 'Coordinador'")

    coordinadores = db.query(usuarios.Usuario).filter(usuarios.Usuario.id_rol == coordinador_rol.id_rol).all()
    return coordinadores


@router.get("/{id_coordinador}", response_model=usuarios_schema.UsuarioOut)
def obtener_coordinador(
    id_coordinador: int,
    db: Session = Depends(get_db),
    _: usuarios.Usuario = Depends(require_role(["Administrador", "Coordinador"]))
):
    """
    Obtiene un coordinador por su ID.
    """
    coordinador = db.query(usuarios.Usuario).filter(usuarios.Usuario.id_usuario == id_coordinador).first()
    if not coordinador:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    return coordinador


@router.put("/{id_coordinador}", response_model=usuarios_schema.UsuarioOut)
def actualizar_coordinador(
    id_coordinador: int,
    datos_actualizados: usuarios_schema.UsuarioUpdate,
    db: Session = Depends(get_db),
    _: usuarios.Usuario = Depends(require_role(["Administrador"]))
):
    """
    Actualiza los datos de un coordinador.
    Solo accesible para el rol 'Administrador'.
    """
    coordinador = db.query(usuarios.Usuario).filter(usuarios.Usuario.id_usuario == id_coordinador).first()
    if not coordinador:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")

    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(coordinador, key, value)

    db.commit()
    db.refresh(coordinador)
    return coordinador


@router.delete("/{id_coordinador}")
def eliminar_coordinador(
    id_coordinador: int,
    db: Session = Depends(get_db),
    _: usuarios.Usuario = Depends(require_role(["Administrador"]))
):
    """
    Elimina un coordinador por su ID.
    Solo accesible para el rol 'Administrador'.
    """
    coordinador = db.query(usuarios.Usuario).filter(usuarios.Usuario.id_usuario == id_coordinador).first()
    if not coordinador:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")

    db.delete(coordinador)
    db.commit()
    return {"mensaje": f"Coordinador con ID {id_coordinador} eliminado correctamente"}
