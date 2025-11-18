from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db

from models.terapias import Terapia
from schemas.terapias import TerapiaCreate, TerapiaUpdate, TerapiaResponse

router = APIRouter(
    prefix="/terapias",
    tags=["Terapias"]
)

# ============================
# ✔ Obtener todas
# ============================
@router.get("/", response_model=list[TerapiaResponse])
def get_terapias(db: Session = Depends(get_db)):
    return db.query(Terapia).all()


# ============================
# ✔ Obtener por ID
# ============================
@router.get("/{id_terapia}", response_model=TerapiaResponse)
def get_terapia(id_terapia: int, db: Session = Depends(get_db)):
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id_terapia).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")
    return terapia


# ============================
# ✔ Crear
# ============================
@router.post("/", response_model=TerapiaResponse, status_code=status.HTTP_201_CREATED)
def crear_terapia(data: TerapiaCreate, db: Session = Depends(get_db)):
    nueva = Terapia(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# ============================
# ✔ Modificar
# ============================
@router.put("/{id_terapia}", response_model=TerapiaResponse)
def actualizar_terapia(id_terapia: int, data: TerapiaUpdate, db: Session = Depends(get_db)):
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id_terapia).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(terapia, k, v)

    db.commit()
    db.refresh(terapia)
    return terapia


# ============================
# ✔ Eliminar
# ============================
@router.delete("/{id_terapia}", status_code=204)
def eliminar_terapia(id_terapia: int, db: Session = Depends(get_db)):
    terapia = db.query(Terapia).filter(Terapia.id_terapia == id_terapia).first()
    if not terapia:
        raise HTTPException(404, "Terapia no encontrada")
