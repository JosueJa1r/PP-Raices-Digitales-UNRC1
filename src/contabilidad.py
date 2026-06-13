import math

# ==========================================
# 1. CONTABILIDAD FINANCIERA
# ==========================================

def calcular_roi(ganancia_cosecha, costo_siembra):
    """
    Retorno de Inversión (ROI). Devuelve el porcentaje de rentabilidad.
    """
    if costo_siembra <= 0:
        return 0.0
    roi = ((ganancia_cosecha - costo_siembra) / costo_siembra) * 100
    return round(roi, 2)

def calcular_punto_equilibrio(costos_fijos, precio_venta_unidad, costo_variable_unidad):
    """
    Punto de Equilibrio Financiero (PEF). 
    Cuántas unidades se necesitan vender para no perder dinero.
    """
    if precio_venta_unidad <= costo_variable_unidad:
        return float('inf') # Evita división por cero o resultados ilógicos si no hay margen
    pef = costos_fijos / (precio_venta_unidad - costo_variable_unidad)
    return math.ceil(pef) # Redondeamos hacia arriba porque no puedes vender "media" lechuga




# ==========================================
# CONSTANTES CONTABLES FIJAS
# ==========================================
COSTO_JORNALES = 130.50  # Costo diario de mano de obra
PESO_COSTAL = 55.0      # Peso de un costal de semilla en Kg


#JORNADAS DE TRABAJO 



#COSTO DE SEMILLA
def calcular_costo_semilla(precio_costal, peso_costal, densidad_m2, area_m2):
    """
    Calcula el costo total de la semilla utilizada en base a la superficie y densidad.
    """
    if peso_costal <= 0:
        return 0.0
    costo_por_unidad = precio_costal / peso_costal
    cantidad_usada = densidad_m2 * area_m2
    return cantidad_usada * costo_por_unidad


#COSTO DE HERRAMIENTAS 



def calcular_costo_siembra_realista(precio_costal, area_m2, densidad_m2=0.02):
    """
    Calcula el costo total de la siembra basado en el costo proporcional de la semilla (removiendo costos fijos).
    """
    if area_m2 <= 0:
        return 0.0
    
    # Costo de la semilla
    precio_costal_val = precio_costal if (precio_costal and precio_costal > 0) else 100.0
    costo_semilla_total = calcular_costo_semilla(precio_costal_val, PESO_COSTAL, densidad_m2, area_m2)
    
    return round(costo_semilla_total, 2)

