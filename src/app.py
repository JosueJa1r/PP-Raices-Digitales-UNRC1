from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.bd import registrar_productor, login_productor, registrar_cliente, login_cliente, obtener_cosechas_productor, obtener_semillas, obtener_stats_productor, obtener_inventario_productor, registrar_producto_inventario, obtener_analiticas_globales, registrar_publicacion_cosecha, obtener_categorias, eliminar_producto_inventario, obtener_catalogo_publicado, descontar_stock_inventario, obtener_perfil_productor, actualizar_perfil_productor, eliminar_cuenta_productor, registrar_estudiante, login_estudiante, registrar_monitoreo, obtener_monitoreos_estudiante, obtener_productores, obtener_monitoreos_productor, obtener_notificaciones_productor, registrar_siembra, cosechar_cultivo, eliminar_cosecha
from src.ia.bot import generar_respuesta_bot
from src.contabilidad import calcular_roi, calcular_punto_equilibrio, calcular_costo_siembra_realista
from src.agronomia import indice_estres_salino
from src.probabilidad import probabilidad_bayesiana
from src.integral import integral_acumulacion_precipitacion
from src.regresion import calcular_regresion_lineal, proyectar_valores

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
            # Obtener el pH y Salinidad más recientes del monitoreo de este productor
            from src.bd import conexion_db
            import math
            ph_actual = 7.0
            salinidad_actual = 1.2
            conn = conexion_db()
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT PH, Salinidad FROM monitoreo_chinampa 
                        WHERE Id_Productor = %s 
                        ORDER BY Fecha DESC LIMIT 1
                    """, (id_productor,))
                    last_m = cursor.fetchone()
                    if last_m:
                        ph_actual = float(last_m['PH'])
                        salinidad_actual = float(last_m['Salinidad'])
                    cursor.close()
                    conn.close()
                except Exception as db_e:
                    print("Error al obtener último monitoreo en cosechas:", db_e)

            # Aplicar modelos matemáticos a cada cosecha antes de enviarla
            for cos in result['cosechas']:
                valor_neto = cos.get('Valor_Neto') or 0.0
                precio_costal = cos.get('Valor_Semilla') or 0.0
                area_m2 = cos.get('Metros_Cuadrados') or 0.0
                
                # Calcular costo de siembra real con las fórmulas de contabilidad (Opción 2: Escalar según m2 con 15% dedicación de mano de obra)
                tiempo_prod = cos.get('Tiempo_Produccion') or 90
                costo_semilla = calcular_costo_siembra_realista(precio_costal, area_m2)
                
                escala_area = area_m2 / 500.0 if area_m2 > 0 else 0.2
                costo_mano_obra = (350.0 * tiempo_prod) * escala_area * 0.15
                costo_herramientas = 400.0 * escala_area
                costo_mantenimiento = 900.0 * escala_area
                
                costo_real = costo_semilla + costo_mano_obra + costo_herramientas + costo_mantenimiento
                cos['costo_calculado'] = costo_real
                cos['roi_calculado'] = calcular_roi(valor_neto, costo_real) if valor_neto > 0 else 0.0

                # Modelos agronómicos y probabilísticos para siembra
                ph_optimo_val = cos.get('pH_Optimo')
                if ph_optimo_val is None:
                    ph_optimo_val = cos.get('ph_optimo')
                ph_optimo = float(ph_optimo_val) if ph_optimo_val is not None else 6.5
                diff_ph = abs(ph_actual - ph_optimo)
                p_base = 0.88
                
                if diff_ph <= 0.5:
                    factor_ph = 1.0
                elif diff_ph <= 1.2:
                    factor_ph = 1.0 - (diff_ph - 0.5) * 0.35
                else:
                    factor_ph = max(0.15, 0.75 - (diff_ph - 1.2) * 0.30)
                    
                if salinidad_actual <= 1.5:
                    factor_sal = 1.0
                elif salinidad_actual <= 3.0:
                    factor_sal = 1.0 - (salinidad_actual - 1.5) * 0.20
                else:
                    factor_sal = max(0.20, 0.70 - (salinidad_actual - 3.0) * 0.15)
                
                # Factor de Temporada (Desviación estacional)
                temporada_ciclo = cos.get('Temporada')
                temporada_semilla = cos.get('Temporada_Semilla')
                factor_temp = 1.0
                if temporada_ciclo and temporada_semilla and temporada_semilla != 'Perennes':
                    # Si la temporada elegida no coincide con la de la semilla, se penaliza un 25%
                    if (temporada_ciclo == 'Primavera-Verano' and temporada_semilla == 'Otoño-Invierno') or \
                        (temporada_ciclo == 'Otoño-Invierno' and temporada_semilla == 'Primavera-Verano'):
                        factor_temp = 0.75
                
                p_germinacion = max(0.0, min(p_base * factor_ph * factor_sal * factor_temp, 1.0))
                prob_perdida = 1.0 - p_germinacion
                
                cos['ph_actual'] = ph_actual
                cos['salinidad_actual'] = salinidad_actual
                cos['ph_optimo'] = ph_optimo
                cos['p_germinacion'] = round(p_germinacion * 100, 1)
                cos['prob_perdida'] = round(prob_perdida * 100, 1)
                
                # Riesgo desabasto
                # Simular cantidad total esperada en base a un estándar
                cant_simulada = 100
                pedido_simulado = 80
                from src.probabilidad import probabilidad_binomial_pmf
                prob_falla = 0.0
                for x in range(int(pedido_simulado)):
                    prob_falla += probabilidad_binomial_pmf(cant_simulada, x, p_germinacion)
                cos['riesgo_insuficiencia'] = round(prob_falla * 100, 1)
                
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
            # Obtener el pH y Salinidad más recientes del monitoreo de este productor
            from src.bd import conexion_db
            import math
            ph_actual = 7.0
            salinidad_actual = 1.2
            conn = conexion_db()
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT PH, Salinidad FROM monitoreo_chinampa 
                        WHERE Id_Productor = %s 
                        ORDER BY Fecha DESC LIMIT 1
                    """, (id_productor,))
                    last_m = cursor.fetchone()
                    if last_m:
                        ph_actual = float(last_m['PH'])
                        salinidad_actual = float(last_m['Salinidad'])
                    cursor.close()
                    conn.close()
                except Exception as db_e:
                    print("Error al obtener último monitoreo:", db_e)

            # Aplicar modelos agronómicos y probabilísticos de post-cosecha (Opción A)
            import datetime
            import math
            for prod in result['productos']:
                # 1. Calcular días en almacenamiento desde la cosecha
                dias_almacenamiento = 0
                fecha_cosecha_val = prod.get('Fecha_Cosecha')
                if fecha_cosecha_val:
                    try:
                        if isinstance(fecha_cosecha_val, (datetime.datetime, datetime.date)):
                            if isinstance(fecha_cosecha_val, datetime.datetime):
                                fecha_cosecha_dt = fecha_cosecha_val.date()
                            else:
                                fecha_cosecha_dt = fecha_cosecha_val
                        else:
                            fecha_cosecha_dt = datetime.datetime.strptime(str(fecha_cosecha_val)[:10], '%Y-%m-%d').date()
                        dias_almacenamiento = max(0, (datetime.date.today() - fecha_cosecha_dt).days)
                    except Exception as dt_e:
                        print("Error al calcular dias_almacenamiento:", dt_e)
                
                # 2. Índice de decaimiento post-cosecha (tasa exponencial)
                # Hortalizas de hoja o flores se degradan más rápido (12% diario) que tubérculos o frutos (4% diario)
                id_cat = prod.get('Id_Categoria')
                lambda_factor = 0.12 if id_cat in (2, 3) else 0.04
                
                # Probabilidad de merma acumulada por almacenamiento
                p_merma = 1.0 - math.exp(-lambda_factor * dias_almacenamiento)
                
                # Guardar valores de almacenamiento en el producto
                prod['dias_almacenamiento'] = dias_almacenamiento
                prod['riesgo_merma'] = round(p_merma * 100, 1)
                
                precio_actual = prod.get('Precio_Actual') or 0.0
                prod['merma_proyectada'] = (prod['Cantidad'] * p_merma) * precio_actual
                
                # 3. Calcular costo de siembra real y ROI con las fórmulas de contabilidad (Opción 2: Escalar según m2 con 15% dedicación de mano de obra)
                valor_neto = prod.get('Valor_Neto') or 0.0
                # Si el valor neto no está definido, estimar según cantidad * precio_actual
                if valor_neto <= 0:
                    valor_neto = prod['Cantidad'] * precio_actual
                
                precio_costal = prod.get('Valor_Semilla') or 0.0
                area_m2 = prod.get('Metros_Cuadrados') or 0.0
                
                tiempo_prod = prod.get('Tiempo_Produccion') or 90
                costo_semilla = calcular_costo_siembra_realista(precio_costal, area_m2)
                
                escala_area = area_m2 / 500.0 if area_m2 > 0 else 0.2
                costo_mano_obra = (350.0 * tiempo_prod) * escala_area * 0.15
                costo_herramientas = 400.0 * escala_area
                costo_mantenimiento = 900.0 * escala_area
                
                costo_real = costo_semilla + costo_mano_obra + costo_herramientas + costo_mantenimiento
                prod['costo_calculado'] = costo_real
                prod['roi_esperado'] = calcular_roi(valor_neto, costo_real) if costo_real > 0 else 0.0
                
                # ROI Real basado en ventas reales
                total_vendido_monto = prod.get('Total_Vendido_Monto') or 0.0
                prod['roi_real'] = calcular_roi(total_vendido_monto, costo_real) if total_vendido_monto > 0 else 0.0
                
                # Calcular Punto de Equilibrio
                pef = 0
                if precio_actual > 0:
                    costo_var_unidad = costo_semilla / (prod['Cantidad'] if prod['Cantidad'] > 0 else 1.0)
                    costos_fijos = costo_mano_obra + costo_herramientas + costo_mantenimiento
                    pef = calcular_punto_equilibrio(costos_fijos, precio_actual, costo_var_unidad)
                prod['punto_equilibrio'] = pef
            
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

@app.route('/api/productor/cosechas/<int:id_cosecha>', methods=['DELETE'])
def delete_cosecha_route(id_cosecha):
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = eliminar_cosecha(id_cosecha, id_productor)
        if result['success']:
            return jsonify({"message": "Proyección eliminada"}), result['status']
        else:
            return jsonify({"error": result['error']}), result.get('status', 500)
    except Exception as e:
        print("Error en ruta eliminar cosecha:", e)
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
        precio = data.get('precio')  # Opcional si se quiere poner precio al publicar
        if not nuevo_estado:
            return jsonify({"error": "Estado requerido"}), 400
        result = actualizar_estado_inventario(id_inventario, nuevo_estado, precio)
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

@app.route('/api/calculos/integral', methods=['POST'])
def post_calculo_integral():
    try:
        data = request.get_json()
        tasas = data.get('tasas', [])
        tasas_float = [float(x) for x in tasas]
        res = integral_acumulacion_precipitacion(tasas_float)
        return jsonify({"resultado": res, "unidad": "L/m² (mm acumulados)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/calculos/regresion', methods=['POST'])
def post_calculo_regresion():
    try:
        data = request.get_json()
        x = data.get('x', [])
        y = data.get('y', [])
        periodos_futuros = int(data.get('periodos_futuros', 4))
        
        x_float = [float(val) for val in x]
        y_float = [float(val) for val in y]
        
        if len(x_float) != len(y_float):
            return jsonify({"error": "Las listas X e Y deben tener la misma longitud."}), 400
            
        res_reg = calcular_regresion_lineal(x_float, y_float)
        
        if "error" in res_reg:
            return jsonify({"error": res_reg["error"]}), 400
            
        m = res_reg["pendiente"]
        b = res_reg["interseccion"]
        r2 = res_reg["r_cuadrado"]
        
        ultimo_x = x_float[-1] if x_float else 0
        proyecciones = proyectar_valores(m, b, periodos_futuros, ultimo_x)
        
        # Calcular los valores ajustados para la línea histórica
        valores_ajustados = [round(m * val + b, 2) for val in x_float]
        
        return jsonify({
            "pendiente": m,
            "interseccion": b,
            "r_cuadrado": r2,
            "valores_ajustados": valores_ajustados,
            "proyecciones": proyecciones
        })
    except Exception as e:
        print("Error en calculo de regresion lineal:", e)
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


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
        id_semilla = data.get('id_semilla') # Opcional, para autolink
        
        if not id_productor or not lote or not cantidad:
            return jsonify({"error": "Faltan campos obligatorios (productor, nombre o cantidad)"}), 400

        result = registrar_publicacion_cosecha(
            id_productor, lote, cantidad, precio, vender_directo, id_cosecha, unidad, id_semilla
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
            
        # Validación: compra mínima de 2 kilos/unidades
        try:
            cant_val = float(cantidad)
            if cant_val < 2.0:
                return jsonify({"error": "La compra mínima es de 2 kilos/unidades."}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Cantidad no válida"}), 400
        
        id_cliente = data.get('id_cliente')
        result = descontar_stock_inventario(id_inventario, cantidad, id_cliente)
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

@app.route('/api/productor/notificaciones', methods=['GET'])
def get_notificaciones_productor_route():
    try:
        id_productor = request.args.get('id_productor')
        if not id_productor:
            return jsonify({"error": "ID de productor requerido"}), 400
            
        result = obtener_notificaciones_productor(id_productor)
        if result['success']:
            return jsonify(result['notificaciones']), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta obtener notificaciones:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/siembras', methods=['POST'])
def post_registrar_siembra():
    try:
        data = request.get_json()
        id_productor = data.get('id_productor')
        id_semilla = data.get('id_semilla')
        metros_cuadrados = data.get('metros_cuadrados')
        temporada = data.get('temporada')
        
        if not id_productor or not id_semilla:
            return jsonify({"error": "ID de productor e ID de semilla son requeridos"}), 400
            
        result = registrar_siembra(id_productor, id_semilla, metros_cuadrados, temporada)
        if result['success']:
            return jsonify({"message": "Siembra registrada exitosamente", "id_cosecha": result['id_cosecha']}), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta registrar siembra:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/productor/cosechas/finalizar', methods=['POST'])
def post_finalizar_cosecha():
    try:
        data = request.get_json()
        id_cosecha = data.get('id_cosecha')
        cantidad = data.get('cantidad')
        unidad_medida = data.get('unidad_medida', 'Kg')
        precio = data.get('precio', 0.0)
        vender_directamente = data.get('vender_directamente', False)
        
        if not id_cosecha or cantidad is None:
            return jsonify({"error": "ID de cosecha y cantidad son requeridos"}), 400
            
        result = cosechar_cultivo(id_cosecha, cantidad, unidad_medida, precio, vender_directamente)
        if result['success']:
            return jsonify({
                "message": f"Cultivo cosechado y guardado en {result['estado']}",
                "id_inventario": result['id_inventario'],
                "estado": result['estado']
            }), result['status']
        else:
            return jsonify({"error": result['error']}), result['status']
    except Exception as e:
        print("Error en ruta finalizar cosecha:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Inicia el servidor local en el puerto 5000
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)