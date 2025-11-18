from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.cita_tipos import CitaTipo
from schemas.cita_tipos import CitaTipoCreate, CitaTipoUpdate, CitaTipoResponse

router = APIRouter(prefix="/cita-tipos", tags=["Cita Tipos"])

# Obtener todos
@router.get("/", response_model=list[CitaTipoResponse])
def listar_tipos(db: Session = Depends(get_db)):
    return db.query(CitaTipo).all()

# Crear
@router.post("/", response_model=CitaTipoResponse)
def crear_tipo(data: CitaTipoCreate, db: Session = Depends(get_db)):

    existe = db.query(CitaTipo).filter(CitaTipo.nombre_tipo == data.nombre_tipo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este tipo ya existe.")

    nuevo = CitaTipo(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Actualizar
@router.put("/{id_tipo}", response_model=CitaTipoResponse)
def actualizar_tipo(id_tipo: int, data: CitaTipoUpdate, db: Session = Depends(get_db)):
    tipo = db.query(CitaTipo).filter(CitaTipo.id_tipo == id_tipo).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="No encontrado")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(tipo, field, value)

    db.commit()
    db.refresh(tipo)
    return tipo

# Eliminar (no borramos, solo modo seguro)
@router.delete("/{id_tipo}")
def eliminar_tipo(id_tipo: int, db: Session = Depends(get_db)):
    tipo = db.query(CitaTipo).filter(CitaTipo.id_tipo == id_tipo).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="No encontrado")

    db.delete(tipo)
    db.commit()
    return {"message": "Tipo eliminado"}
