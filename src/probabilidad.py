# ==========================================
# 2. PROBABILIDAD Y ESTADÍSTICA
# ==========================================

def probabilidad_bayesiana(prob_clima_dado_exito, prob_exito_historico, prob_clima_general):
    """
    Teorema de Bayes: Calcula P(Éxito | Clima)
    Ejemplo: Probabilidad de que la cosecha sea exitosa dado que llovió fuerte.
    """
    if prob_clima_general <= 0:
        return 0.0
    prob_condicional = (prob_clima_dado_exito * prob_exito_historico) / prob_clima_general
    return round(prob_condicional, 4)

import math

def calcular_p_germinacion(ph, p_base=0.85):
    """
    Ajusta la probabilidad de germinación en base al pH del agua.
    El rango óptimo para chinampas es 6.0 a 7.2.
    """
    if 6.0 <= ph <= 7.2:
        factor = 1.0
    elif 5.0 <= ph < 6.0:
        factor = 1.0 - (6.0 - ph) * 0.4  # Reducción por acidez
    elif 7.2 < ph <= 8.5:
        factor = 1.0 - (ph - 7.2) * 0.4  # Reducción por alcalinidad
    else:
        factor = 0.15  # Reducción crítica por valores extremos
        
    return max(0.0, min(p_base * factor, 1.0))

def coeficiente_binomial(n, k):
    """Calcula las combinaciones posibles de n en k."""
    return math.comb(n, k)

def probabilidad_binomial_pmf(n, k, p):
    """Fórmula clásica de distribución binomial para exactamente k éxitos."""
    if not (0 <= k <= n):
        return 0.0
    return coeficiente_binomial(n, k) * (p**k) * ((1 - p)**(n - k))



