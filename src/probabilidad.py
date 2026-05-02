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
