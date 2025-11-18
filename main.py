import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.session import engine
from database.base import Base
from config.settings import settings

# ===============================
# 📌 IMPORTACIÓN DE MODELOS
#   (Necesario para que SQLAlchemy registre TODAS las tablas)
# ===============================
import models.usuarios
import models.roles
import models.personal
import models.ninos
import models.tutores
import models.terapias
import models.citas
import models.ninos_prospecto
import models.cita_tipos


# ===============================
# 📌 Routers existentes
# ===============================
from auth.auth_router import router as auth_router
from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.personal import router as personal_router
from routers.grados_academicos import router as grados_router
from routers.citas import router as citas_router

# ===============================
# 📌 Routers nuevos completos
# ===============================
from routers.tutores import router as tutores_router
from routers.ninos import router as ninos_router
from routers.terapias import router as terapias_router
from routers.ninos_prospecto import router as prospectos_router
from routers.cita_tipos import router as cita_tipos_router


# ================================================================
# 🚀 FastAPI App
# ================================================================
app = FastAPI(title=settings.PROJECT_NAME)


# ================================================================
# 🗂️ Crear todas las tablas automáticamente
# ================================================================
Base.metadata.create_all(bind=engine)


# ================================================================
# 🌐 CORS (necesario para Angular en puerto 4200)
# ================================================================
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================================================
# 📁 Archivos estáticos (/static -> carpeta uploads)
# ================================================================
app.mount("/static", StaticFiles(directory="uploads"), name="static")


# ================================================================
# 🔗 Registrar todos los Routers
# ================================================================
# 🔐 Auth + Base
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(personal_router)
app.include_router(grados_router)

# 🧑‍🤝‍🧑 Tutores / Niños / Terapias
app.include_router(tutores_router)
app.include_router(ninos_router)
app.include_router(terapias_router)

# 🧒 Prospectos de niños
app.include_router(prospectos_router)

# 🏷 Tipos de cita
app.include_router(cita_tipos_router)

# 📅 Citas completas (con niño, prospecto o nombre libre)
app.include_router(citas_router)


# ================================================================
# 🏠 Ruta principal
# ================================================================
@app.get("/")
def root():
    return {
        "mensaje": "API Autismo Mochis IA funcionando 🚀",
        "version": "1.0.0"
    }
