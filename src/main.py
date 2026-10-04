from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infrastructure.controllers.api import router
from src.application.discovery_service import fetch_openapi_specs

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de arranque (Ejecutar descubrimiento)
    fetch_openapi_specs()
    yield
    # Lógica de apagado
    print("[*] Apagando ai-service...")

app = FastAPI(
    title="Nefetech AI Service",
    description="Microservicio Orquestador de IA (Clean Architecture)",
    version="0.1.0",
    lifespan=lifespan
)

# Registramos el controlador (rutas)
app.include_router(router)

