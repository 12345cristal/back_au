from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db

from models.ninos import Nino
from schemas.ninos import NinoCreate, NinoUpdate, NinoResponse

router = APIRouter(
    prefix="/ninos",
    tags=["Niños"]
)

@router.get("/", response_model=list[NinoResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Nino).all()

@router.get("/{id_nino}", response_model=NinoResponse)
def get(id_nino: int, db: Session = Depends(get_db)):
    nino = db.query(Nino).filter(Nino.id_nino == id_nino).first()
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    return nino

@router.post("/", response_model=NinoResponse, status_code=status.HTTP_201_CREATED)
def crear(data: NinoCreate, db: Session = Depends(get_db)):
    nuevo = Nino(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_nino}", response_model=NinoResponse)
def actualizar(id_nino: int, data: NinoUpdate, db: Session = Depends(get_db)):
    nino = db.query(Nino).filter(Nino.id_nino == id_nino).first()
    if not nino:
        raise HTTPException(404, "Niño no encontrado")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(nino, k, v)

    db.commit()
    db.refresh(nino)
    return nino

@router.delete("/{id_nino}", status_code=204)
def eliminar(id_nino: int, db: Session = Depends(get_db)):
    nino = db.query(Nino).filter(Nino.id_nino == id_nino).first()
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    db.delete(nino)
    db.commit()
