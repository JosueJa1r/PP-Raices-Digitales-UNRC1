from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio 

app = Flask(__name__)

@app.route('/')
def home():
    # Creamos la gráfica aquí adentro
    fig = px.bar(x=["A", "B", "C"], y=[1, 3, 2])
    
    # La convertimos a HTML (solo el div)
    graph_html = pio.to_html(fig, full_html=False)
    
    # Enviamos la gráfica al template
    return render_template('index.html', grafico=graph_html)




def procesar_datos():
    try:
        # 1. Recolección de datos del formulario web
        # Variables Ambientales
        s_actual = float(request.form['s_actual'])
        s_optima = float(request.form['s_optima'])
        s_critica = float(request.form['s_critica'])
        
        # Variables Financieras
        cf = float(request.form['costos_fijos'])
        p_u = float(request.form['precio_unitario'])
        cv_u = float(request.form['costo_variable'])
        
        # Variables de Producción
        r_historico = float(request.form['r_historico'])
        r_actual = float(request.form['r_actual'])

        # 2. Aplicación de Fórmulas Matemáticas (Sección 6.3)
        
        # A. Índice de Estrés Salino (IES)
        ies = (s_actual - s_optima) / (s_critica - s_optima)
        alerta_ies = "RIESGO GRAVE: Condiciones no aptas" if ies >= 1.0 else "Riesgo Aceptable"
        
        # B. Punto de Equilibrio Financiero (PEF)
        margen_contribucion = p_u - cv_u
        if margen_contribucion > 0:
            pef = cf / margen_contribucion
            estado_pef = f"Se necesitan vender {pef:.2f} unidades para no tener pérdidas."
        else:
            pef = 0
            estado_pef = "ERROR: El costo variable es mayor o igual al precio de venta."

        # C. Merma Económica Proyectada (ME)
        if r_actual < r_historico:
            me = (r_historico - r_actual) * p_u
            estado_me = f"Pérdida proyectada de ${me:.2f} MXN."
        else:
            me = 0
            estado_me = "Sin merma proyectada. Rendimiento óptimo."

        # 3. Respuesta de la Capa de Salida (JSON / Diccionario)
        resultados = {
            "1_Indice_Estres_Salino": {
                "valor_calculado": round(ies, 2),
                "diagnostico": alerta_ies
            },
            "2_Punto_Equilibrio": {
                "unidades_minimas": round(pef, 2),
                "diagnostico": estado_pef
            },
            "3_Merma_Economica": {
                "perdida_financiera_mxn": round(me, 2),
                "diagnostico": estado_me
            }
        }
        
        # Retornamos los resultados en formato JSON para que puedan ser leídos por el dashboard
        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Inicia el servidor local en el puerto 5000
    app.run(debug=True, port=5000)

