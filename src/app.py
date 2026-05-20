import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bd import registrar_productor, login_productor, registrar_cliente, login_cliente, obtener_cosechas_productor, obtener_semillas, obtener_stats_productor, obtener_inventario_productor, registrar_producto_inventario, obtener_analiticas_globales, registrar_publicacion_cosecha, obtener_categorias, eliminar_producto_inventario, obtener_catalogo_publicado, descontar_stock_inventario, obtener_perfil_productor, actualizar_perfil_productor, eliminar_cuenta_productor, registrar_estudiante, login_estudiante, registrar_monitoreo, obtener_monitoreos_estudiante, obtener_productores, obtener_monitoreos_productor
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
        id_productor = data.get('id_productor')
        
        reply = generar_respuesta_bot(user_message, id_productor)
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
        telefono = data.get('telefono')
        semillas = data.get('semillas', [])
        
        result = registrar_productor(nombre, correo, password, hectareas, filtros, telefono, semillas)
        
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

@app.route('/api/categorias', methods=['GET'])
def get_categorias_route():
    try:
        result = obtener_categorias()
        if result['success']:
            return jsonify(result['categorias']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener categorias:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/semillas_por_categoria', methods=['GET'])
def get_semillas_por_categoria_route():
    try:
        id_categoria = request.args.get('id_categoria')
        if not id_categoria:
            return jsonify({"error": "ID de categoría requerido"}), 400
        result = obtener_semillas(id_categoria=id_categoria)
        if result['success']:
            return jsonify(result['semillas']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener semillas por categoria:", e)
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
        tipo = request.args.get('tipo')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_inventario_productor(id_productor, tipo)
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

@app.route('/api/productor/inventario/<int:id_inventario>', methods=['DELETE'])
def delete_inventario_route(id_inventario):
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = eliminar_producto_inventario(id_inventario, id_productor)
        if result['success']:
            return jsonify({"message": "Registro eliminado"}), result['status']
        else:
            return jsonify({"error": result['error']}), result.get('status', 500)
    except Exception as e:
        print("Error en ruta eliminar inventario:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/inventario', methods=['POST'])
def post_inventario_productor_route():
    try:
        data = request.get_json()
        id_productor = data.get('id_productor')
        lote = data.get('lote')
        cantidad = data.get('cantidad')
        unidad = data.get('unidad_medida', 'Kg')
        precio = data.get('precio')
        observaciones = data.get('observaciones', '')
        
        result = registrar_producto_inventario(id_productor, lote, cantidad, precio, observaciones, unidad)
        if result['success']:
            return jsonify({"message": "Producto registrado en inventario", "id": result['id_inventario']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta registrar inventario:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/inventario/<int:id_inventario>/estado', methods=['PUT'])
def put_estado_inventario_route(id_inventario):
    try:
        from src.bd import actualizar_estado_inventario
        data = request.get_json()
        nuevo_estado = data.get('estado')
        if not nuevo_estado:
            return jsonify({"error": "Estado requerido"}), 400
        result = actualizar_estado_inventario(id_inventario, nuevo_estado)
        if result['success']:
            return jsonify({"message": "Estado actualizado exitosamente"}), 200
        else:
            return jsonify({"error": result['error']}), 500
    except Exception as e:
        print("Error en ruta estado inventario:", e)
        return jsonify({"error": "Error interno"}), 500

@app.route('/api/analiticas/global', methods=['GET'])
def get_analiticas_global_route():
    try:
        result = obtener_analiticas_globales()
        if result['success']:
            print(f"DEBUG: Enviando analíticas. Volumen: {len(result['data']['volumen'])} items, KPIs: {result['data']['kpis']}")
            return jsonify(result['data']), result['status']
        else:
            print(f"DEBUG: Error en obtención de analíticas: {result['error']}")
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error CRÍTICO en ruta obtener analiticas:", e)
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

@app.route('/api/productor/publicar_cosecha', methods=['POST'])
def post_publicar_cosecha_route():
    try:
        data = request.get_json()
        id_productor = data.get('id_productor')
        lote = data.get('lote')
        cantidad = data.get('cantidad')
        precio = data.get('precio', 0)
        vender_directo = data.get('vender_directamente', False)
        id_cosecha = data.get('id_cosecha') # Opcional
        unidad = data.get('unidad_medida', 'Kg')
        
        if not id_productor or not lote or not cantidad:
            return jsonify({"error": "Faltan campos obligatorios (productor, nombre o cantidad)"}), 400

        result = registrar_publicacion_cosecha(
            id_productor, lote, cantidad, precio, vender_directo, id_cosecha, unidad
        )
        
        if result['success']:
            return jsonify({
                "message": f"Registro exitoso como {result['estado']}",
                "id_inventario": result['id_inventario'],
                "estado": result['estado']
            }), 201
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta publicar cosecha:", e)
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@app.route('/api/catalogo', methods=['GET'])
def get_catalogo_route():
    """Endpoint público: devuelve todos los productos con Estado='Publicado'."""
    try:
        busqueda = request.args.get('q', None)
        result = obtener_catalogo_publicado(busqueda)
        if result['success']:
            return jsonify(result['productos']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta catalogo:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/cliente/comprar', methods=['POST'])
def post_comprar_producto_route():
    """Endpoint de compra: descuenta stock y puede marcar producto como Agotado."""
    try:
        data = request.get_json()
        id_inventario = data.get('id_inventario')
        cantidad = data.get('cantidad', 1)
        
        if not id_inventario:
            return jsonify({"error": "id_inventario requerido"}), 400
        
        result = descontar_stock_inventario(id_inventario, cantidad)
        if result['success']:
            return jsonify({
                "message": f"Compra exitosa: {result['lote']}",
                "nuevo_stock": result['nuevo_stock'],
                "estado": result['estado']
            }), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta comprar:", e)
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@app.route('/api/productor/perfil', methods=['GET'])
def get_perfil_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_perfil_productor(id_productor)
        if result['success']:
            return jsonify(result['perfil']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener perfil:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/perfil', methods=['POST'])
def post_perfil_productor_route():
    try:
        data = request.get_json()
        id_productor = data.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = actualizar_perfil_productor(id_productor, data)
        if result['success']:
            return jsonify({"message": "Perfil actualizado correctamente"}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta actualizar perfil:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/eliminar_cuenta', methods=['DELETE'])
def delete_cuenta_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = eliminar_cuenta_productor(id_productor)
        if result['success']:
            return jsonify({"message": "Cuenta eliminada correctamente"}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta eliminar cuenta:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/register/estudiante', methods=['POST'])
def register_estudiante_route():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        
        result = registrar_estudiante(nombre, correo, password)
        
        if result['success']:
            return jsonify({"message": "Registro de estudiante exitoso", "id_estudiante": result['id_estudiante']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta registro estudiante:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/login/estudiante', methods=['POST'])
def login_estudiante_route():
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')
        
        result = login_estudiante(correo, password)
        
        if result['success']:
            return jsonify({"message": "Login de estudiante exitoso", "user": result['user']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
            
    except Exception as e:
        print("Error en ruta login estudiante:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productores', methods=['GET'])
def get_productores_route():
    try:
        result = obtener_productores()
        if result['success']:
            return jsonify(result['productores']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener productores:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/monitoreo', methods=['POST'])
def post_monitoreo_route():
    try:
        data = request.get_json()
        id_estudiante = data.get('id_estudiante')
        id_productor = data.get('id_productor')
        ph = data.get('ph')
        salinidad = data.get('salinidad')
        humedad = data.get('humedad')
        temperatura = data.get('temperatura')
        observaciones = data.get('observaciones', '')
        
        if not id_estudiante or not id_productor:
            return jsonify({"error": "ID de estudiante y productor son requeridos"}), 400
            
        result = registrar_monitoreo(id_estudiante, id_productor, ph, salinidad, humedad, temperatura, observaciones)
        if result['success']:
            return jsonify({"message": "Monitoreo registrado exitosamente", "id_monitoreo": result['id_monitoreo']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta registrar monitoreo:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/estudiante/monitoreos', methods=['GET'])
def get_monitoreos_estudiante_route():
    try:
        id_estudiante = request.args.get('id_estudiante')
        if not id_estudiante:
            return jsonify({"error": "ID de estudiante requerido"}), 400
            
        result = obtener_monitoreos_estudiante(id_estudiante)
        if result['success']:
            return jsonify(result['monitoreos']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener monitoreos estudiante:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/monitoreos', methods=['GET'])
def get_monitoreos_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_monitoreos_productor(id_productor)
        if result['success']:
            return jsonify(result['monitoreos']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener monitoreos productor:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Inicia el servidor local en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)