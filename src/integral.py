# ==========================================
# 3. CÁLCULO INTEGRAL (Aproximación Discreta)
# ==========================================

def integral_acumulacion_precipitacion(tasa_lluvia_diaria):
    """
    Aproxima la integral del volumen total de agua recibida: Integral de p(t) dt.
    tasa_lluvia_diaria: Lista de milímetros de lluvia por día (ej. [5.2, 0, 1.1, 10.5]).
    Usamos la suma discreta (Riemann) asumiendo dt = 1 día.
    """
    acumulacion_total = sum(tasa_lluvia_diaria)
    return round(acumulacion_total, 2)

def integral_volumen_biomasa(tasa_crecimiento_diario):
    """
    Aproxima el volumen / peso de la planta integrando su tasa de crecimiento.
    tasa_crecimiento_diario: Lista de gramos/cm crecidos por día.
    """
    volumen_final = sum(tasa_crecimiento_diario)
    return round(volumen_final, 2)
