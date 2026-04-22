# Lógica para calcular el nivel de salinidad
def nivelSalinidad(x):    
    if x <= 0.5:
        return "Bajo"
    elif 0.5 < x <= 1.5:   
        return "Moderado"
    else:
        return "Alto"
    
 # Lógica para calcular el punto de equilibrio   
def calcular_punto_equilibrio(costos_fijos, precio_unitario, costo_variable_unitario):
    margen_contribucion = precio_unitario - costo_variable_unitario
    if margen_contribucion <= 0:
        return "Error: El costo variable es mayor o igual al precio de venta."        
    pef = costos_fijos / margen_contribucion
    return pef # Retorna las unidades que deben venderse