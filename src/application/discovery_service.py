import os
import requests

_DISCOVERED_TOOLS = {}

def fetch_openapi_specs():
    """Descubre dinámicamente los endpoints de otros microservicios"""
    auth_service_url = os.getenv("AUTH_SERVICE_OPENAPI_URL", "http://localhost:8080/v3/api-docs")
    print(f"[*] Iniciando Descubrimiento de APIs en: {auth_service_url}")
    try:
        response = requests.get(auth_service_url, timeout=5)
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get("paths", {})
            
            for path, methods in paths.items():
                for method, details in methods.items():
                    operation_id = details.get("operationId", f"{method}_{path}".replace("/", "_"))
                    summary = details.get("summary", "Sin resumen")
                    desc = details.get("description", "Sin descripción")
                    
                    _DISCOVERED_TOOLS[operation_id] = {
                        "name": operation_id,
                        "description": f"{summary}: {desc}",
                        "method": method.upper(),
                        "url": path
                    }
            print(f"[*] ¡Éxito! Se descubrieron {len(_DISCOVERED_TOOLS)} endpoints dinámicamente.")
        else:
            print(f"[*] Error HTTP al descubrir APIs: {response.status_code}")
    except Exception:
        print(f"[*] auth-service no está corriendo o no se pudo alcanzar.")

def get_discovered_tools():
    return _DISCOVERED_TOOLS
