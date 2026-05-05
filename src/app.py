import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bd import registrar_productor, login_productor, registrar_cliente, login_cliente, obtener_cosechas_productor, obtener_semillas, obtener_stats_productor, obtener_inventario_productor, registrar_producto_inventario, obtener_analiticas_globales
from src.ia.bot import generar_respuesta_bot
from src.contabiliad import calcular_roi, calcular_punto_equilibrio, calcular_utilidad_neta
from src.agronomia import indice_estres_salino
from src.probabilidad import probabilidad_bayesiana
from src.integral import integral_acumulacion_precipitacion

# Cargar variables de entorno (API Keys)
load_dotenv()

# Inicializar Flask (sólo como API Backend)
app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el frontend (puerto 5501)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat_bot_route():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        reply = generar_respuesta_bot(user_message)
        return jsonify({"reply": reply})
        
    except Exception as e:
        print("Error en RaícesBot IA:", e)
        return jsonify({"error": str(e) or "Hubo un problema al conectar con la IA. Intenta de nuevo más tarde."}), 500

@app.route('/api/register/productor', methods=['POST'])
def register_productor_route():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        hectareas = data.get('terreno')
        filtros = data.get('filtros')
        
        result = registrar_productor(nombre, correo, password, hectareas, filtros)
        
        if result['success']:
            return jsonify({"message": "Registro exitoso", "id_productor": result['id_productor']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta registro:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/login/productor', methods=['POST'])
def login_productor_route():
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        result = login_productor(correo, password)
        
        if result['success']:
            return jsonify({"message": "Login exitoso", "user": result['user']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta login:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/register/cliente', methods=['POST'])
def register_cliente_route():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        telefono = data.get('telefono')
        localidad = data.get('localidad')
        correo = data.get('correo')
        password = data.get('password')
        
        result = registrar_cliente(nombre, telefono, localidad, correo, password)
        
        if result['success']:
            return jsonify({"message": "Registro de cliente exitoso", "id_cliente": result['id_cliente']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta registro cliente:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/login/cliente', methods=['POST'])
def login_cliente_route():
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        result = login_cliente(correo, password)
        
        if result['success']:
            return jsonify({"message": "Login de cliente exitoso", "user": result['user']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta login cliente:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/cosechas', methods=['GET'])
def get_cosechas_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_cosechas_productor(id_productor)
        
        if result['success']:
            # Aplicar modelos matemáticos a cada cosecha antes de enviarla
            for cos in result['cosechas']:
                # Simulamos un costo base (ej. 70% del valor neto) para calcular el ROI
                # TODO: Usar costo real de la BD cuando esté disponible
                valor_neto = cos.get('Valor_Neto', 0)
                costo_simulado = valor_neto * 0.7 
                cos['roi_calculado'] = calcular_roi(valor_neto, costo_simulado)
                
            return jsonify(result['cosechas']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta obtener cosechas:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/semillas', methods=['GET'])
def get_semillas_route():
    try:
        id_productor = request.args.get('id_productor')
        result = obtener_semillas(id_productor)
        if result['success']:
            return jsonify(result['semillas']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener semillas:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/stats', methods=['GET'])
def get_stats_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_stats_productor(id_productor)
        if result['success']:
            return jsonify(result['stats']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener stats:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/inventario', methods=['GET'])
def get_inventario_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_inventario_productor(id_productor)
        if result['success']:
            # Aplicar modelos agronómicos y probabilísticos
            for prod in result['productos']:
                prob_perdida = 0.15
                precio_actual = prod.get('Precio_Actual', 0)
                prod['merma_proyectada'] = (prod['Cantidad'] * prob_perdida) * precio_actual
            
            # Calcular KPIs de inventario
            productos_ordenados = sorted(result['productos'], key=lambda x: x['Cantidad'])
            stock_critico = productos_ordenados[0] if productos_ordenados else None
            atencion_proxima = productos_ordenados[1] if len(productos_ordenados) > 1 else None
            
            return jsonify({
                "items": result['productos'],
                "stats": {
                    "critico": stock_critico['Lote'] if stock_critico else "N/A",
                    "critico_cant": stock_critico['Cantidad'] if stock_critico else 0,
                    "atencion": atencion_proxima['Lote'] if atencion_proxima else "N/A",
                    "estado": "Óptimo" if len(productos_ordenados) > 2 else "Limitado"
                }
            }), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener inventario:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/inventario', methods=['POST'])
def post_inventario_productor_route():
    try:
        data = request.get_json()
        id_productor = data.get('id_productor')
        lote = data.get('lote')
        cantidad = data.get('cantidad')
        precio = data.get('precio')
        observaciones = data.get('observaciones', '')
        
        result = registrar_producto_inventario(id_productor, lote, cantidad, precio, observaciones)
        if result['success']:
            return jsonify({"message": "Producto registrado en inventario", "id": result['id_inventario']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta registrar inventario:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/analiticas/global', methods=['GET'])
def get_analiticas_global_route():
    try:
        result = obtener_analiticas_globales()
        if result['success']:
            return jsonify(result['data']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener analiticas:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

# --- RUTAS DE MODELOS MATEMÁTICOS ---

@app.route('/api/calculos/roi', methods=['POST'])
def post_calculo_roi():
    data = request.get_json()
    res = calcular_roi(float(data['ganancia']), float(data['costo']))
    return jsonify({"resultado": res, "unidad": "%"})

@app.route('/api/calculos/estres', methods=['POST'])
def post_calculo_estres():
    data = request.get_json()
    res = indice_estres_salino(float(data['ce_obs']), float(data['ce_umbral']), float(data['factor']))
    return jsonify({"resultado": res, "unidad": "% de riesgo"})

@app.route('/api/calculos/bayes', methods=['POST'])
def post_calculo_bayes():
    data = request.get_json()
    res = probabilidad_bayesiana(float(data['p_clima_exito']), float(data['p_exito']), float(data['p_clima']))
    return jsonify({"resultado": res * 100, "unidad": "% de probabilidad"})

if __name__ == '__main__':
    # Inicia el servidor local en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)


