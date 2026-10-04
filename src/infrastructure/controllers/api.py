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

from src.application.semantic_cache import is_greeting, is_farewell
import random

from src.application.groq_service import generate_ai_response, is_prompt_safe

@router.post("/api/v1/chat")
async def chat(request: ChatRequest):
    if is_greeting(request.message):
        return {
            "reply": "Hola, como estas?, estoy para ayudarte, dime que necesitas",
            "tools_available": [],
            "cached": True
        }
        
    if is_farewell(request.message):
        return {
            "reply": "¡De nada! Ha sido un placer ayudarte. Nos vemos pronto.",
            "tools_available": [],
            "cached": True
        }

    # 2. Guardia de Seguridad Semántica (Prompt Guard)
    if not is_prompt_safe(request.message):
        return {
            "reply": "He detectado un posible intento de evadir las directivas de seguridad (Jailbreak / Prompt Injection). No puedo responder a esta solicitud.",
            "tools_available": [],
            "cached": False,
            "security_flag": True
        }

    # 3. Lógica normal con LLM (Consume tokens en Groq)
    tools = get_discovered_tools()
    ai_reply = generate_ai_response(request.message)
    
    return {
        "reply": ai_reply,
        "tools_available": [t["description"] for t in tools.values()],
        "cached": False,
        "security_flag": False
    }
