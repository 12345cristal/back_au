# ============================================================
# 🔵 Gestión de Personal – Router Final Profesional
# ============================================================

from fastapi import (
    APIRouter, Depends, Form, UploadFile, File, HTTPException
)
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import shutil

from database.session import get_db
from core.security import require_role, hash_password

from models.usuarios import Usuario
from models.personal import Personal
from models.roles import Rol
from models.grados_academicos import GradoAcademico

from schemas.personal import PersonalListItem, PersonalDetalle


# ============================================================
# 🗂 Configuración para guardar archivos (LOCAL, SIN utils)
# ============================================================

BASE_UPLOAD_DIR = Path("uploads")
FOTOS_DIR = BASE_UPLOAD_DIR / "personal_fotos"
CV_DIR = BASE_UPLOAD_DIR / "personal_cv"
COMP_DIR = BASE_UPLOAD_DIR / "personal_comprobantes"

for d in (FOTOS_DIR, CV_DIR, COMP_DIR):
    d.mkdir(parents=True, exist_ok=True)


def save_upload_file(file: UploadFile, folder: Path, prefix: str) -> str:
    """
    Guarda un archivo subido y regresa la ruta accesible por /static.
    NO usa 'utils', todo está en este archivo.
    """
    if not file:
        return ""

    ext = Path(file.filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    destination = folder / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Esto se sirve desde main.py: app.mount("/static", StaticFiles(directory="uploads"), name="static")
    return f"/static/{folder.name}/{filename}"


# ============================================================
# Inicializar router
# ============================================================

router = APIRouter(prefix="/personal", tags=["Personal"])


# ============================================================
# GET – LISTA DE PERSONAL
# ============================================================

@router.get("/", response_model=List[PersonalListItem])
def listar_personal(
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):
    query = (
        db.query(
            Personal.id_personal,
            Usuario.nombre,
            Usuario.apellido_paterno,
            Usuario.apellido_materno,
            Usuario.correo,
            Usuario.telefono,
            Usuario.activo,
            Usuario.foto_perfil,
            Rol.nombre_rol.label("rol"),
            GradoAcademico.nombre.label("grado_academico"),
        )
        .join(Usuario, Personal.id_usuario == Usuario.id_usuario)
        .join(Rol, Usuario.id_rol == Rol.id_rol)
        .outerjoin(GradoAcademico, Personal.id_grado == GradoAcademico.id_grado)
        .order_by(Usuario.nombre)
        .all()
    )

    salida: List[PersonalListItem] = []

    for r in query:
        nombre_completo = f"{r.nombre} {r.apellido_paterno or ''} {r.apellido_materno or ''}".strip()
        iniciales = ((r.nombre or "")[:1] + (r.apellido_paterno or "")[:1]).upper()

        salida.append(
            PersonalListItem(
                id_personal=r.id_personal,
                nombre=nombre_completo,
                email=r.correo,
                telefono=r.telefono or "",
                rol=r.rol,
                iniciales=iniciales,
                calificacion=0.0,  # si luego agregas rating real, se cambia aquí
                activo=bool(r.activo),
                foto=r.foto_perfil,
                grado_academico=r.grado_academico,
            )
        )

    return salida


# ============================================================
# GET – DETALLE DE PERSONAL
# ============================================================

@router.get("/{id_personal}", response_model=PersonalDetalle)
def obtener_personal(
    id_personal: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):

    result = (
        db.query(Personal, Usuario, Rol, GradoAcademico)
        .join(Usuario, Personal.id_usuario == Usuario.id_usuario)
        .join(Rol, Usuario.id_rol == Rol.id_rol)
        .outerjoin(GradoAcademico, Personal.id_grado == GradoAcademico.id_grado)
        .filter(Personal.id_personal == id_personal)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Personal no encontrado")

    p, u, rol, grado = result

    return PersonalDetalle(
        id_personal=p.id_personal,
        id_usuario=u.id_usuario,
        nombre=u.nombre,
        apellido_paterno=u.apellido_paterno,
        apellido_materno=u.apellido_materno,
        correo=u.correo,
        telefono=u.telefono,
        rol=rol.nombre_rol,
        activo=u.activo,
        foto_perfil=u.foto_perfil,

        # 👇 para poder editar desde Angular
        id_rol=u.id_rol,
        id_grado=p.id_grado,

        fecha_nacimiento=p.fecha_nacimiento.isoformat() if p.fecha_nacimiento else None,
        fecha_ingreso=p.fecha_ingreso.isoformat() if p.fecha_ingreso else None,
        grado_academico=grado.nombre if grado else None,

        especialidades=p.especialidades,
        telefono_personal=p.telefono_personal,
        correo_personal=p.correo_personal,

        rfc=p.rfc,
        ine=p.ine,
        curp=p.curp,

        domicilio_calle=p.domicilio_calle,
        domicilio_colonia=p.domicilio_colonia,
        domicilio_cp=p.domicilio_cp,
        domicilio_municipio=p.domicilio_municipio,
        domicilio_estado=p.domicilio_estado,

        cv_archivo=p.cv_archivo,
        comprobante_domicilio=p.comprobante_domicilio,
        experiencia=p.experiencia,
    )


# ============================================================
# POST – CREAR PERSONAL COMPLETO
# ============================================================

@router.post("/", status_code=201)
async def crear_personal(
    # Usuario
    nombre: str = Form(...),
    apellido_paterno: str = Form(""),
    apellido_materno: str = Form(""),
    correo: str = Form(...),
    telefono: str = Form(""),
    id_rol: int = Form(...),
    contrasena: str = Form(...),

    # Personal
    fecha_nacimiento: Optional[str] = Form(None),
    fecha_ingreso: Optional[str] = Form(None),
    id_grado: Optional[int] = Form(None),
    especialidades: str = Form(""),
    telefono_personal: str = Form(""),
    correo_personal: str = Form(""),
    rfc: str = Form(""),
    ine: str = Form(""),
    curp: str = Form(""),
    domicilio_calle: str = Form(""),
    domicilio_colonia: str = Form(""),
    domicilio_cp: str = Form(""),
    domicilio_municipio: str = Form(""),
    domicilio_estado: str = Form(""),
    experiencia: str = Form(""),

    # Archivos
    foto_perfil: UploadFile | None = File(None),
    cv_archivo: UploadFile | None = File(None),
    comprobante_domicilio: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):

    # Validar rol
    if not db.query(Rol).filter(Rol.id_rol == id_rol).first():
        raise HTTPException(400, "Rol inválido")

    # Validar grado
    if id_grado and not db.query(GradoAcademico).filter(GradoAcademico.id_grado == id_grado).first():
        raise HTTPException(400, "Grado académico inválido")

    # Validar correo duplicado
    if db.query(Usuario).filter(Usuario.correo == correo).first():
        raise HTTPException(400, "Ya existe un usuario con ese correo")

    # Guardar archivos
    foto_path = save_upload_file(foto_perfil, FOTOS_DIR, f"foto_{correo}") if foto_perfil else ""
    cv_path = save_upload_file(cv_archivo, CV_DIR, f"cv_{correo}") if cv_archivo else ""
    comp_path = save_upload_file(comprobante_domicilio, COMP_DIR, f"comp_{correo}") if comprobante_domicilio else ""

    # Crear usuario
    user = Usuario(
        nombre=nombre,
        apellido_paterno=apellido_paterno or None,
        apellido_materno=apellido_materno or None,
        correo=correo,
        telefono=telefono or None,
        id_rol=id_rol,
        contrasena_hash=hash_password(contrasena),
        activo=True,
        foto_perfil=foto_path or None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Parseo de fechas
    def parse_date(value: Optional[str]):
        try:
            return datetime.fromisoformat(value).date() if value else None
        except Exception:
            return None

    # Crear personal
    personal = Personal(
        id_usuario=user.id_usuario,
        fecha_nacimiento=parse_date(fecha_nacimiento),
        fecha_ingreso=parse_date(fecha_ingreso),
        id_grado=id_grado,
        especialidades=especialidades or None,
        telefono_personal=telefono_personal or None,
        correo_personal=correo_personal or None,
        rfc=rfc or None,
        ine=ine or None,
        curp=curp or None,
        domicilio_calle=domicilio_calle or None,
        domicilio_colonia=domicilio_colonia or None,
        domicilio_cp=domicilio_cp or None,
        domicilio_municipio=domicilio_municipio or None,
        domicilio_estado=domicilio_estado or None,
        cv_archivo=cv_path or None,
        comprobante_domicilio=comp_path or None,
        experiencia=experiencia or None,
    )

    db.add(personal)
    db.commit()
    db.refresh(personal)

    return {"mensaje": "Personal creado correctamente", "id_personal": personal.id_personal}


# ============================================================
# PATCH – Cambiar estado Activo
# ============================================================

class EstadoActivoIn(BaseModel):
    activo: bool


@router.patch("/{id_personal}/activo")
def cambiar_estado(
    id_personal: int,
    payload: EstadoActivoIn,
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):

    personal = db.query(Personal).filter(Personal.id_personal == id_personal).first()
    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    user = personal.usuario
    user.activo = payload.activo
    db.commit()

    return {"mensaje": "Estado actualizado", "activo": user.activo}


# ============================================================
# PUT – EDITAR PERSONAL COMPLETO
# ============================================================

@router.put("/{id_personal}", status_code=200)
async def editar_personal(
    id_personal: int,
    # Usuario
    nombre: str = Form(...),
    apellido_paterno: str = Form(""),
    apellido_materno: str = Form(""),
    correo: str = Form(...),
    telefono: str = Form(""),
    id_rol: int = Form(...),

    # Personal
    fecha_nacimiento: Optional[str] = Form(None),
    fecha_ingreso: Optional[str] = Form(None),
    id_grado: Optional[int] = Form(None),
    especialidades: str = Form(""),
    telefono_personal: str = Form(""),
    correo_personal: str = Form(""),
    rfc: str = Form(""),
    ine: str = Form(""),
    curp: str = Form(""),
    domicilio_calle: str = Form(""),
    domicilio_colonia: str = Form(""),
    domicilio_cp: str = Form(""),
    domicilio_municipio: str = Form(""),
    domicilio_estado: str = Form(""),
    experiencia: str = Form(""),

    # Archivos opcionales
    foto_perfil: UploadFile | None = File(None),
    cv_archivo: UploadFile | None = File(None),
    comprobante_domicilio: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):
    personal = db.query(Personal).filter(Personal.id_personal == id_personal).first()
    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    user = personal.usuario

    # validar correo único
    correo_existente = db.query(Usuario).filter(
        Usuario.correo == correo,
        Usuario.id_usuario != user.id_usuario
    ).first()
    if correo_existente:
        raise HTTPException(400, "Ya existe un usuario con ese correo")

    # validar rol
    if not db.query(Rol).filter(Rol.id_rol == id_rol).first():
        raise HTTPException(400, "Rol inválido")

    # validar grado
    if id_grado and not db.query(GradoAcademico).filter(GradoAcademico.id_grado == id_grado).first():
        raise HTTPException(400, "Grado académico inválido")

    # archivos
    if foto_perfil:
        user.foto_perfil = save_upload_file(foto_perfil, FOTOS_DIR, f"foto_{correo}")
    if cv_archivo:
        personal.cv_archivo = save_upload_file(cv_archivo, CV_DIR, f"cv_{correo}")
    if comprobante_domicilio:
        personal.comprobante_domicilio = save_upload_file(comprobante_domicilio, COMP_DIR, f"comp_{correo}")

    def parse_date(value: Optional[str]):
        try:
            return datetime.fromisoformat(value).date() if value else None
        except Exception:
            return None

    # actualizar usuario
    user.nombre = nombre
    user.apellido_paterno = apellido_paterno or None
    user.apellido_materno = apellido_materno or None
    user.correo = correo
    user.telefono = telefono or None
    user.id_rol = id_rol

    # actualizar personal
    personal.fecha_nacimiento = parse_date(fecha_nacimiento)
    personal.fecha_ingreso = parse_date(fecha_ingreso)
    personal.id_grado = id_grado
    personal.especialidades = especialidades or None
    personal.telefono_personal = telefono_personal or None
    personal.correo_personal = correo_personal or None
    personal.rfc = rfc or None
    personal.ine = ine or None
    personal.curp = curp or None
    personal.domicilio_calle = domicilio_calle or None
    personal.domicilio_colonia = domicilio_colonia or None
    personal.domicilio_cp = domicilio_cp or None
    personal.domicilio_municipio = domicilio_municipio or None
    personal.domicilio_estado = domicilio_estado or None
    personal.experiencia = experiencia or None

    db.commit()

    return {"mensaje": "Personal actualizado correctamente"}


# ============================================================
# DELETE – Eliminar registro de Personal
# ============================================================

@router.delete("/{id_personal}", status_code=204)
def eliminar_personal(
    id_personal: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_role(["Administrador", "Coordinador"]))
):

    personal = db.query(Personal).filter(Personal.id_personal == id_personal).first()

    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    db.delete(personal)
    db.commit()
    return {"status": "ok"}
