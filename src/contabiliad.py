import math

# ==========================================
# 1. CONTABILIDAD FINANCIERA
# ==========================================

def calcular_utilidad_neta(ingresos_totales, costos_insumos, costos_operativos):
    """
    Calcula el Valor Estimado Neto de las cosechas.
    """
    costos_totales = costos_insumos + costos_operativos
    utilidad = ingresos_totales - costos_totales
    return round(utilidad, 2)

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

def calcular_merma_economica(volumen_esperado, probabilidad_perdida, precio_venta):
    """
    Cálculo de Merma Económica Proyectada (ME) por clima o plagas.
    """
    merma = (volumen_esperado * probabilidad_perdida) * precio_venta
    return round(merma, 2)
