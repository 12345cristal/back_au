# routers/citas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from database.session import get_db
from models.citas import Cita
from models.ninos_prospecto import NinoProspecto
from schemas.citas import CitaCreate, CitaUpdate, CitaResponse

from utils.email_notificaciones import (
    enviar_notificacion_cita_creada,
    enviar_notificacion_cita_cancelada,
)

router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)

# ===========================================================
# 🔹 Helper: validar que haya algún tipo de niño ligado
# ===========================================================
def _validar_nino_fuente(data: CitaCreate | CitaUpdate):
    if not data.id_nino and not data.id_nino_prospecto and not data.nombre_nino_libre:
        raise HTTPException(
            status_code=400,
            detail="Debes proporcionar al menos uno: id_nino, id_nino_prospecto o nombre_nino_libre."
        )


# ===========================================================
# 🟢 Obtener todas las citas
# ===========================================================
@router.get("/", response_model=list[CitaResponse])
def get_citas(db: Session = Depends(get_db)):
    return db.query(Cita).order_by(Cita.fecha.desc(), Cita.hora).all()


# ===========================================================
# 🟢 Obtener cita por ID
# ===========================================================
@router.get("/{id_cita}", response_model=CitaResponse)
def get_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(404, "Cita no encontrada")
    return cita


# ===========================================================
# 🟢 Citas de hoy
# ===========================================================
@router.get("/hoy", response_model=list[CitaResponse])
def citas_de_hoy(db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.fecha == date.today()).all()


# ===========================================================
# 🟢 Citas sin niño formal (prospectos o solo nombre)
# ===========================================================
@router.get("/prospectos", response_model=list[CitaResponse])
def citas_prospectos(db: Session = Depends(get_db)):
    return (
        db.query(Cita)
        .filter(Cita.id_nino.is_(None))
        .filter((Cita.id_nino_prospecto.is_not(None)) | (Cita.nombre_nino_libre.is_not(None)))
        .order_by(Cita.fecha.desc(), Cita.hora)
        .all()
    )


# ===========================================================
# 🟢 Crear nueva cita (niño formal, prospecto o solo nombre)
# ===========================================================
@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(data: CitaCreate, db: Session = Depends(get_db)):

    _validar_nino_fuente(data)

    nueva = Cita(**data.dict(exclude_unset=True))
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # Notificación por correo (solo si hay niño formal o prospecto con correo)
    try:
        enviar_notificacion_cita_creada(nueva, db)
    except Exception:
        # no rompemos la API por falla de correo
        pass

    return nueva


# ===========================================================
# 🟢 Actualizar cita
# ===========================================================
@router.put("/{id_cita}", response_model=CitaResponse)
def actualizar_cita(id_cita: int, data: CitaUpdate, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()

    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    # Si el payload incluye cambios de niño, valida regla de al menos uno
    if any([
        "id_nino" in data.dict(exclude_unset=True),
        "id_nino_prospecto" in data.dict(exclude_unset=True),
        "nombre_nino_libre" in data.dict(exclude_unset=True),
    ]):
        _validar_nino_fuente(data)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(cita, key, value)

    db.commit()
    db.refresh(cita)

    return cita


# ===========================================================
# 🟢 Cancelar cita (solo cambia estado)
# ===========================================================
@router.put("/cancelar/{id_cita}", response_model=CitaResponse)
def cancelar_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()

    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    cita.estado = "Cancelada"
    db.commit()
    db.refresh(cita)

    try:
        enviar_notificacion_cita_cancelada(cita, db)
    except Exception:
        pass

    return cita


# ===========================================================
# 🟢 Eliminar cita
# ===========================================================
@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()

    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    db.delete(cita)
    db.commit()

    return {"mensaje": "Cita eliminada correctamente"}


# ===========================================================
# 🟢 Asociar cita a un niño ya registrado (registro posterior)
# ===========================================================
@router.put("/{id_cita}/asociar-nino/{id_nino}", response_model=CitaResponse)
def asociar_nino_definitivo(id_cita: int, id_nino: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(404, "Cita no encontrada")

    # Asigna niño formal y limpia prospecto (opcional)
    cita.id_nino = id_nino
    cita.id_nino_prospecto = None
    # puedes decidir si limpiar o no el nombre libre
    # cita.nombre_nino_libre = None

    db.commit()
    db.refresh(cita)

    return cita


# ===========================================================
# 🟢 Citas por terapeuta
# ===========================================================
@router.get("/terapeuta/{id_personal}", response_model=list[CitaResponse])
def citas_por_terapeuta(id_personal: int, db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.id_personal == id_personal).all()


# ===========================================================
# 🟢 Citas por niño formal
# ===========================================================
@router.get("/nino/{id_nino}", response_model=list[CitaResponse])
def citas_por_nino(id_nino: int, db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.id_nino == id_nino).all()
