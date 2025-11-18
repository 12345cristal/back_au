# schemas/citas.py
from datetime import date, time
from pydantic import BaseModel
from typing import Optional


class CitaBase(BaseModel):
    # Asociaciones posibles
    id_nino: Optional[int] = None
    id_nino_prospecto: Optional[int] = None
    nombre_nino_libre: Optional[str] = None

    id_personal: Optional[int] = None
    id_terapia: Optional[int] = None
    id_tipo: Optional[int] = None  # Valoración, observación, etc.

    fecha: Optional[date] = None
    hora: Optional[time] = None
    tipo: Optional[str] = None      # texto libre opcional
    notas: Optional[str] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[time] = None
    id_terapia: Optional[int] = None
    id_nino: Optional[int] = None
    id_nino_prospecto: Optional[int] = None
    nombre_nino_libre: Optional[str] = None
    id_personal: Optional[int] = None
    id_tipo: Optional[int] = None
    tipo: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[str] = None


class CitaResponse(CitaBase):
    id_cita: int
    estado: str

    model_config = {"from_attributes": True}
