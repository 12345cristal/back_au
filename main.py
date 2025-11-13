import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.session import engine
from database.base import Base
from config.settings import settings

# Routers
from auth.auth_router import router as auth_router
from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.coordinadores import router as coordinadores_router
from routers.permisos import router as permisos_router
from routers.permisos import router as roles_permisos_router

# ================================================================
# 🚀 Inicialización general
# ================================================================
app = FastAPI(title=settings.PROJECT_NAME)

# ✅ Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# ================================================================
# 🌐 Configuración de CORS
# ================================================================
origins = [
    "http://localhost:4200",  # Angular local
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # puedes usar ["*"] para permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================================
# 🧩 Incluir todos los routers
# ================================================================
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(coordinadores_router)
app.include_router(permisos_router)
app.include_router(roles_permisos_router)

# ================================================================
# 🏠 Ruta raíz
# ================================================================
@app.get("/")
def root():
    return {"mensaje": "🚀 API Autismo Mochis IA en funcionamiento"}
