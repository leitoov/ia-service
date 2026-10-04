# AI Service (Nefetech)

Microservicio orquestador de Inteligencia Artificial para el ecosistema Nefetech.
Construido con Python y FastAPI.

## Propósito
- Centralizar las peticiones a LLMs (OpenAI, Anthropic, Gemini, etc.).
- Gestionar Caché (Redis) para ahorrar costos de tokens.
- Actuar como un Agente que puede consumir otros microservicios (Function Calling).

## Requisitos
- Python 3.10+
- Redis (Opcional, para caché)

## Instalación y Ejecución Local

1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar variables de entorno:
   Copiar `.env.example` a `.env` y completar los valores.
4. Ejecutar el servidor de desarrollo:
   ```bash
   uvicorn src.main:app --reload
   ```

El servicio estará disponible en http://localhost:8000
La documentación de la API estará en http://localhost:8000/docs
