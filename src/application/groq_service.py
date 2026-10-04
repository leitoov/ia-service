import os
from dotenv import load_dotenv

load_dotenv()

def generate_ai_response(user_message: str) -> str:
    """
    Genera una respuesta utilizando una Cascada de Modelos (LLM Router).
    Intenta responder con un modelo pequeño y ultra-rápido primero.
    Si el modelo pequeño determina que la consulta es muy compleja, delega al modelo grande.
    """
    try:
        from groq import Groq
        client = Groq()
        
        # 1. Intentamos con el modelo pequeño y rápido
        small_model = "llama-3.1-8b-instant"
        
        small_completion = client.chat.completions.create(
            model=small_model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un clasificador y asistente básico de Nefetech. Si el mensaje es una pregunta sencilla, respóndela amigablemente en menos de 30 palabras. Si el mensaje requiere razonamiento profundo, buscar en bases de datos, o es muy técnico, responde EXACTAMENTE con la palabra: ESCALAR"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.3,
            max_tokens=256,
            stream=False
        )
        
        respuesta_corta = small_completion.choices[0].message.content.strip()
        
        # 2. Si el modelo pequeño decide derivar, usamos el gigante (120B)
        if "ESCALAR" in respuesta_corta.upper():
            print("El modelo pequeño decidió ESCALAR al modelo pesado (70B)...")
            
            big_completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres el asistente avanzado de Nefetech. El usuario tiene una consulta compleja. Responde con sumo detalle, razonamiento y precisión."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=2048,
                stream=False
            )
            return big_completion.choices[0].message.content
            
        # Si no escaló, devolvemos la respuesta del modelo pequeño
        print("El modelo pequeño respondió directamente (Ahorro de costos/tiempo).")
        return respuesta_corta
        
    except ImportError:
        return f"[MOCK] No se encontró la librería 'groq'. Para usar la IA real: pip install groq. Tu mensaje fue: {user_message}"
    except Exception as e:
        return f"[ERROR IA] Ocurrió un error al contactar al enrutador LLM: {e}"

def is_prompt_safe(user_message: str) -> bool:
    """
    Verifica si el mensaje del usuario es seguro (libre de inyecciones de prompt o jailbreaks)
    utilizando el modelo llama-prompt-guard-2-86m a través de Groq.
    """
    try:
        from groq import Groq
        client = Groq()
        
        completion = client.chat.completions.create(
            model="llama-guard-3-8b",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
            max_tokens=1,
            top_p=1,
            stream=False,
            stop=None
        )
        
        # Normalmente los modelos de guard dictan 'safe' o 'unsafe'/'jailbreak' en el primer token
        resultado = completion.choices[0].message.content.lower().strip()
        # Si devuelve cualquier variante que sugiera inyección de prompt o inseguridad
        if "unsafe" in resultado or "jailbreak" in resultado:
            return False
            
        return True
    except ImportError:
        # Si no hay groq, asumimos seguro en modo de desarrollo
        return True
    except Exception as e:
        print(f"Error evaluando seguridad del prompt: {e}")
        # En caso de error, podríamos bloquear por precaución o dejar pasar. Optamos por dejar pasar en caso de caída de API.
        return True
