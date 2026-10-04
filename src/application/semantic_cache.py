import logging

logger = logging.getLogger(__name__)

# Definimos variables globales
_model = None
_saludo_vector = None

# Lista de saludos base para promediar o comparar (usaremos uno muy genérico)
SALUDO_BASE = "hola como estas, todo bien?"

def get_model():
    """Carga perezosa del modelo para no bloquear el inicio si no se usa."""
    global _model, _saludo_vector
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Cargando modelo de SentenceTransformers (esto puede tardar unos segundos la primera vez)...")
            # Usamos un modelo súper liviano y rápido optimizado para similitud semántica multilingüe
            _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            _saludo_vector = _model.encode(SALUDO_BASE)
            logger.info("Modelo semántico cargado correctamente.")
        except ImportError:
            logger.error("sentence-transformers no está instalado. Ejecuta: pip install sentence-transformers")
            return None
        except Exception as e:
            logger.error(f"Error cargando el modelo semántico: {e}")
            return None
    return _model

def is_greeting(message: str, umbral: float = 0.70) -> bool:
    """
    Verifica si el mensaje es semánticamente un saludo.
    Si sentence-transformers falla, hace un fallback basado en reglas (regex).
    """
    model = get_model()
    
    # Fallback basado en reglas simples si el modelo no cargó
    if not model:
        saludos_simples = {"hola", "buenas", "buen dia", "hola como estas", "todo bien", "buenas tardes", "que tal", "holis"}
        msg_limpio = message.lower().strip()
        # Eliminar signos de interrogación y exclamación
        for char in ['¿', '?', '¡', '!', ',', '.']:
            msg_limpio = msg_limpio.replace(char, '')
        msg_limpio = msg_limpio.strip()
        
        # Si tiene pocas palabras y alguna coincide, es un saludo
        palabras = msg_limpio.split()
        if len(palabras) <= 3 and any(p in saludos_simples for p in palabras) or msg_limpio in saludos_simples:
            return True
        return False

    # Proceso semántico (No consume tokens)
    try:
        from sentence_transformers import util
        # Limitamos la longitud por seguridad (un saludo normal no tiene 50 palabras)
        if len(message.split()) > 10:
            return False
            
        mensaje_vector = model.encode(message)
        similitud = util.cos_sim(_saludo_vector, mensaje_vector).item()
        
        logger.info(f"Similitud semántica de '{message}' con saludo base: {similitud:.2f}")
        return similitud > umbral
    except Exception as e:
        logger.error(f"Error procesando similitud: {e}")
        return False
