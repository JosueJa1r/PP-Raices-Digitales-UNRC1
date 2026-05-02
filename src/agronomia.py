# ==========================================
# 4. MODELOS AGRONÓMICOS ESPECIALIZADOS
# ==========================================

def indice_estres_salino(ce_observada, ce_umbral, factor_perdida):
    """
    Índice de Estrés Salino (IES). 
    Mide el impacto de la salinidad del agua (como en canales de Xochimilco).
    Devuelve el % de reducción en la cosecha.
    """
    if ce_observada <= ce_umbral:
        return 0.0 # No hay estrés si la salinidad está por debajo del umbral
    
    ies = (ce_observada - ce_umbral) * factor_perdida
    # La pérdida no puede ser mayor al 100%
    return round(min(ies, 100.0), 2)
