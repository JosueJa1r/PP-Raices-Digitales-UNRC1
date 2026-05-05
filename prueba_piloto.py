# =================================================================
# SISTEMA RAÍCES DIGITALES - MÓDULO DE AUDITORÍA E INTELIGENCIA
# Desarrollado por: Equipo Raíces Digitales
# Propósito: Módulo de cálculos avanzado para validación de negocios
# =================================================================

import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# =================================================================
# 1. MODELOS MATEMÁTICOS AVANZADOS
# =================================================================

def calcular_roi(ganancia_esperada, costo_siembra):
    # Retorno de Inversión (%)
    if costo_siembra == 0: return 0
    roi = ((ganancia_esperada - costo_siembra) / costo_siembra) * 100
    return round(roi, 2)

def calcular_punto_equilibrio(costos_fijos, precio_venta_unidad, costo_variable_unidad):
    # Unidades necesarias para no tener pérdidas
    margen = precio_venta_unidad - costo_variable_unidad
    if margen <= 0: return "Infinito (Margen no rentable)"
    return round(costos_fijos / margen, 2)

def calcular_merma_economica(cantidad_inventario, precio_unitario, riesgo_probabilidad=0.15):
    # Pérdida de dinero proyectada por factores externos
    perdida = cantidad_inventario * precio_unitario * riesgo_probabilidad
    return round(perdida, 2)

def indice_estres_salino(ce_observada, ce_umbral, factor_pendiente=2.5):
    # Riesgo agronómico por calidad de agua
    if ce_observada <= ce_umbral: return 0
    riesgo = (ce_observada - ce_umbral) * factor_pendiente
    return min(round(riesgo, 2), 100)

def probabilidad_bayesiana(p_clima_exito, p_exito_historico, p_clima_general):
    # Teorema de Bayes para éxito de cosecha
    if p_clima_general == 0: return 0
    probabilidad = (p_clima_exito * p_exito_historico) / p_clima_general
    return round(probabilidad * 100, 2)

# =================================================================
# 2. CONSULTAS E INTELIGENCIA DE DATOS
# =================================================================

def conexion_db():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'raices_digitales')
        )
    except Error as e:
        print(f"Error conexión: {e}")
        return None

def auditoria_productor(id_productor):
    # Analiza el estado real de un productor en la BD
    conn = conexion_db()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    
    # 1. Valor total de terrenos
    cursor.execute("SELECT SUM(Hectareas) as total FROM terreno WHERE Id_Productor = %s", (id_productor,))
    terrenos = cursor.fetchone()
    
    # 2. Conteo de cosechas
    cursor.execute("SELECT COUNT(*) as total FROM cosecha c JOIN terreno t ON c.Id_Terreno = t.Id_Terreno WHERE t.Id_Productor = %s", (id_productor,))
    cosechas = cursor.fetchone()
    
    conn.close()
    return {
        "hectareas": terrenos['total'] if terrenos['total'] else 0,
        "cosechas": cosechas['total'] if cosechas['total'] else 0
    }

# =================================================================
# 3. INTERFAZ DE TERMINAL Y REPORTES
# =================================================================

def guardar_reporte(texto):
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_auditoria_{fecha}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n[OK] Reporte guardado como: {nombre_archivo}")

def menu_principal():
    print("\n" + "╔" + "═"*45 + "╗")
    print("║   SISTEMA DE AUDITORÍA RAÍCES DIGITALES     ║")
    print("╚" + "═"*45 + "╝")
    print("1. Análisis de Rentabilidad (ROI)")
    print("2. Cálculo de Punto de Equilibrio (Ventas)")
    print("3. Proyección de Merma (Riesgo Inventario)")
    print("4. Riesgo de Suelo (IES - Agronomía)")
    print("5. Auditoría de Productor Real (Desde BD)")
    print("6. Salir")
    
    op = input("\nSeleccione opción: ")
    res_texto = ""

    if op == "1":
        g = float(input("Ganancia ($): "))
        c = float(input("Costo ($): "))
        res = f"ROI Calculado: {calcular_roi(g, c)}%"
        print(f"--> {res}")
        res_texto = f"Auditoría ROI\nGanancia: {g}\nCosto: {c}\nResultado: {res}"

    elif op == "2":
        fijos = float(input("Costos Fijos ($): "))
        precio = float(input("Precio Venta por Unidad ($): "))
        var = float(input("Costo Variable por Unidad ($): "))
        unidades = calcular_punto_equilibrio(fijos, precio, var)
        print(f"--> PUNTO DE EQUILIBRIO: {unidades} unidades")
        res_texto = f"Análisis de Equilibrio\nUnidades necesarias: {unidades}"

    elif op == "3":
        cant = float(input("Cantidad en Inventario: "))
        precio = float(input("Precio Unitario ($): "))
        merma = calcular_merma_economica(cant, precio)
        print(f"--> MERMA PROYECTADA: ${merma} MXN")
        res_texto = f"Riesgo de Inventario\nCantidad: {cant}\nPérdida potencial: ${merma}"

    elif op == "5":
        id_p = input("ID del Productor a auditar: ")
        data = auditoria_productor(id_p)
        if data:
            reporte = f"AUDITORÍA REAL - PRODUCTOR {id_p}\nTotal Hectáreas: {data['hectareas']}\nCosechas en curso: {data['cosechas']}"
            print(f"\n{reporte}")
            res_texto = reporte
        else:
            print("Error al conectar con la base de datos.")

    elif op == "6":
        exit()

    if res_texto and input("\n¿Desea guardar este resultado en un reporte TXT? (s/n): ").lower() == 's':
        guardar_reporte(res_texto)

if __name__ == "__main__":
    while True:
        menu_principal()
