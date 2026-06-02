import os
import google.generativeai as genai
from src.bd import obtener_stats_productor, obtener_cosechas_productor
from src.contabilidad import calcular_costo_siembra_realista, calcular_roi

# Variable global para mantener el modelo instanciado
_generative_model = None

def configurar_bot():
    """Configura la API de Gemini usando la variable de entorno."""
    api_key = os.getenv("BOT_CHAT")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.5-flash')
    return None

def generar_respuesta_bot(user_message, id_productor=None):
    """
    Genera la respuesta de ChinampaAmigo dado un mensaje de usuario.
    """
    global _generative_model
    
    # Configurar el bot en el primer uso (Lazy Loading)
    if _generative_model is None:
        _generative_model = configurar_bot()
        
    if not _generative_model:
        raise Exception("API Key de Gemini no está configurada o es inválida.")
        
    contexto = ""
    if id_productor:
        # Recuperar datos del productor
        stats_res = obtener_stats_productor(id_productor)
        cosechas_res = obtener_cosechas_productor(id_productor)
        if stats_res['success']:
            stats = stats_res['stats']
            contexto += f"\n- Terreno: {stats.get('terreno_total', 0)} metros cuadrados (m²)."
            contexto += f"\n- Cosechas Activas: {stats.get('cosechas_activas', 0)}."
            contexto += f"\n- Valor Neto Estimado: ${stats.get('valor_neto', 0)} MXN."
        if cosechas_res['success']:
            cosechas_info = []
            for c in cosechas_res.get('cosechas', []):
                nombre = c.get('Nombre_Semilla') or c.get('Lote') or 'Cultivo'
                valor_neto = c.get('Valor_Neto') or 0.0
                precio_costal = c.get('Valor_Semilla') or 0.0
                area_m2 = c.get('Metros_Cuadrados') or 0.0
                tiempo_prod = c.get('Tiempo_Produccion') or 90
                costo_semilla = calcular_costo_siembra_realista(precio_costal, area_m2)
                costo_real = costo_semilla + (350.0 * tiempo_prod) + 400.0 + 900.0
                roi = calcular_roi(valor_neto, costo_real) if valor_neto > 0 else 0.0
                
                info = f"{nombre} (Área: {area_m2} m², Costo estimado de siembra: ${costo_real} MXN, Ingreso Bruto: ${valor_neto} MXN, ROI calculado: {roi}%)"
                cosechas_info.append(info)
            if cosechas_info:
                contexto += f"\n- Detalles de cultivos con costos y ROI reales:\n  " + "\n  ".join(cosechas_info)
            
    # Prompt de sistema para mantener el contexto del bot
    prompt = f"""Eres 'ChinampaAmigo', un experto agrícola y asistente de la plataforma Raíces Digitales para los productores chinamperos de Xochimilco. 
Responde de manera breve, amable, útil y profesional a la siguiente consulta del productor.
{f"Contexto del productor (Úsalo para dar consejos personalizados):{contexto}" if contexto else ""}
 
Consulta: {user_message}"""
 
    # Generar contenido
    response = _generative_model.generate_content(prompt)
    return response.text
