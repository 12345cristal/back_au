from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.ninos_prospecto import NinoProspecto
from schemas.ninos_prospecto import (
    ProspectoCreate,
    ProspectoUpdate,
    ProspectoResponse
)

router = APIRouter(prefix="/prospectos", tags=["Niños Prospecto"])


# ============================================================
# GET — Lista completa
# ============================================================
@router.get("/", response_model=list[ProspectoResponse])
def listar_prospectos(db: Session = Depends(get_db)):
    return db.query(NinoProspecto).all()


# ============================================================
# GET — Uno por ID
# ============================================================
@router.get("/", response_model=list[ProspectoResponse])
def listar_prospectos(db: Session = Depends(get_db)):
    return db.query(NinoProspecto).filter_by(activo=True).all()



# ============================================================
# POST — Crear
# ============================================================
@router.post("/", response_model=ProspectoResponse)
def crear_prospecto(data: ProspectoCreate, db: Session = Depends(get_db)):
    prospecto = NinoProspecto(**data.dict())
    db.add(prospecto)
    db.commit()
    db.refresh(prospecto)
    return prospecto


# ============================================================
# PUT — Actualizar
# ============================================================
@router.put("/{id_prospecto}", response_model=ProspectoResponse)
def actualizar_prospecto(id_prospecto: int, data: ProspectoUpdate, db: Session = Depends(get_db)):
    prospecto = db.query(NinoProspecto).filter_by(id_prospecto=id_prospecto).first()
    if not prospecto:
        raise HTTPException(status_code=404, detail="Prospecto no encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(prospecto, campo, valor)

    db.commit()
    db.refresh(prospecto)
    return prospecto


# ============================================================
# DELETE — Eliminar
# ============================================================
@router.delete("/{id_prospecto}")
def eliminar_prospecto(id_prospecto: int, db: Session = Depends(get_db)):
    prospecto = db.query(NinoProspecto).filter_by(id_prospecto=id_prospecto).first()
    if not prospecto:
        raise HTTPException(status_code=404, detail="Prospecto no encontrado")

    prospecto.activo = False   # 👈 NO se elimina
    db.commit()

    return {"mensaje": "Prospecto dado de baja correctamente"}
