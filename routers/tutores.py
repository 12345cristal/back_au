from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db

from models.tutores import Tutor
from schemas.tutores import TutorCreate, TutorUpdate, TutorResponse

router = APIRouter(
    prefix="/tutores",
    tags=["Tutores"]
)

@router.get("/", response_model=list[TutorResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Tutor).all()

@router.get("/{id_tutor}", response_model=TutorResponse)
def obtener(id_tutor: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id_tutor == id_tutor).first()
    if not tutor:
        raise HTTPException(404, "Tutor no encontrado")
    return tutor

@router.post("/", response_model=TutorResponse, status_code=status.HTTP_201_CREATED)
def crear(data: TutorCreate, db: Session = Depends(get_db)):
    nuevo = Tutor(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_tutor}", response_model=TutorResponse)
def actualizar(id_tutor: int, data: TutorUpdate, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id_tutor == id_tutor).first()
    if not tutor:
        raise HTTPException(404, "Tutor no encontrado")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(tutor, k, v)

    db.commit()
    db.refresh(tutor)
    return tutor

@router.delete("/{id_tutor}", status_code=204)
def eliminar(id_tutor: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id_tutor == id_tutor).first()
    if not tutor:
        raise HTTPException(404, "Tutor no encontrado")
    db.delete(tutor)
    db.commit()
