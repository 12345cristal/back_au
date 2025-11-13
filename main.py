import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.session import engine
from database.base import Base
from config.settings import settings

from auth.auth_router import router as auth_router
from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.personal import router as personal_router
from routers.grados_academicos import router as grados_router

app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)

origins = ["http://localhost:4200", "http://127.0.0.1:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(personal_router)
app.include_router(grados_router)

@app.get("/")
def root():
    return {"mensaje": "API Autismo Mochis IA funcionando 🚀"}
