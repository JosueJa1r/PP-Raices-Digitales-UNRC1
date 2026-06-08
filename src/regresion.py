# ==========================================
# 5. PREDICCIÓN CON REGRESIÓN LINEAL SIMPLE
# ==========================================

def calcular_regresion_lineal(x, y):
    """
    Calcula la pendiente (m), intersección (b) y R² para un conjunto de puntos (x, y).
    x: lista de números (independiente: tiempo en semanas o periodos).
    y: lista de números (dependiente: humedad o lluvia acumulada).
    """
    n = len(x)
    if n < 2:
        return {"error": "Se requieren al menos 2 puntos de datos históricos para la regresión lineal."}

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(val * val for val in x)
    sum_yy = sum(val * val for val in y)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    denominador_m = (n * sum_xx - sum_x * sum_x)
    if denominador_m == 0:
        m = 0
    else:
        m = (n * sum_xy - sum_x * sum_y) / denominador_m

    b = (sum_y - m * sum_x) / n

    # Calcular Coeficiente de Determinación R²
    y_prom = sum_y / n
    ss_tot = sum((val - y_prom) ** 2 for val in y)
    
    if ss_tot == 0:
        r_cuadrado = 1.0
    else:
        ss_res = sum((y[i] - (m * x[i] + b)) ** 2 for i in range(n))
        r_cuadrado = 1.0 - (ss_res / ss_tot)

    return {
        "pendiente": round(m, 4),
        "interseccion": round(b, 4),
        "r_cuadrado": round(max(0.0, min(1.0, r_cuadrado)), 4)
    }

def proyectar_valores(m, b, periodos_futuros, ultimo_x):
    """
    Proyecta valores futuros basados en los coeficientes m y b de la recta.
    periodos_futuros: número de pasos hacia adelante.
    ultimo_x: el último valor de tiempo (x) en los datos históricos.
    """
    proyecciones = []
    for i in range(1, periodos_futuros + 1):
        x_futuro = ultimo_x + i
        y_futuro = m * x_futuro + b
        # No permitir valores absurdamente negativos para humedad
        y_futuro_acotado = max(0.0, y_futuro)
        proyecciones.append({
            "periodo": x_futuro,
            "valor": round(y_futuro_acotado, 2)
        })
    return proyecciones
