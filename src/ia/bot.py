import os
import google.generativeai as genai

# Variable global para mantener el modelo instanciado
_generative_model = None

def configurar_bot():
    """Configura la API de Gemini usando la variable de entorno."""
    api_key = os.getenv("BOT_CHAT")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.5-flash')
    return None

def generar_respuesta_bot(user_message):
    """
    Genera la respuesta de RaícesBot IA dado un mensaje de usuario.
    """
    global _generative_model
    
    # Configurar el bot en el primer uso (Lazy Loading)
    if _generative_model is None:
        _generative_model = configurar_bot()
        
    if not _generative_model:
        raise Exception("API Key de Gemini no está configurada o es inválida.")
        
    # Prompt de sistema para mantener el contexto del bot
    prompt = f"""Eres 'RaícesBot IA', un experto agrícola y asistente de la plataforma Raíces Digitales para los productores chinamperos de Xochimilco. 
Responde de manera breve, amable, útil y profesional a la siguiente consulta del productor:
Consulta: {user_message}"""

    # Generar contenido
    response = _generative_model.generate_content(prompt)
    return response.text
