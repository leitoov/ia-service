from fastapi import APIRouter
from pydantic import BaseModel
from src.application.discovery_service import get_discovered_tools

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None

@router.get("/health")
async def health_check():
    tools = get_discovered_tools()
    return {"status": "ok", "service": "ai-service", "tools_loaded": len(tools)}

@router.get("/api/v1/tools")
async def get_tools():
    """Devuelve las herramientas que el ai-service ha descubierto y puede usar"""
    tools = get_discovered_tools()
    return {"tools": list(tools.values())}

from src.application.semantic_cache import is_greeting
import random

@router.post("/api/v1/chat")
async def chat(request: ChatRequest):
    # 1. Enrutamiento de Intenciones (Ahorro de tokens)
    if is_greeting(request.message):
        respuestas_saludo = [
            "¡Hola! Soy el asistente de Nefetech. ¿En qué puedo ayudarte?",
            "¡Qué tal! ¿Cómo puedo asistirte hoy?",
            "¡Hola! Estoy aquí para resolver tus dudas sobre Nefetech."
        ]
        return {
            "reply": random.choice(respuestas_saludo),
            "tools_available": [],
            "cached": True
        }

    # 2. Lógica normal con LLM (Consume tokens)
    # TODO: Llamar al caso de uso (Application Layer) que orquesta Mongo, Redis y LangChain
    tools = get_discovered_tools()
    return {
        "reply": f"Mensaje recibido: '{request.message}'. Actualmente conozco {len(tools)} herramientas. Pronto procesaré esto con LLM.",
        "tools_available": [t["description"] for t in tools.values()],
        "cached": False
    }
