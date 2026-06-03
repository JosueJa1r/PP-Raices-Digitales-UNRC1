import mysql.connector
from decouple import config
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

# No tocar JOSUE - Configuración de conexión
def conexion_db():
    try:
        # Extraemos todas las variables del .env
        host = config('MYSQL_HOST', default='localhost')
        port = config('MYSQL_PORT', default='3306')
        user = config('MYSQL_USER')
        password = config('MYSQL_PASSWORD')
        database = config('MYSQL_DATABASE')

        print(f"Intentando conectar a la base de datos: {database} en {host}:{port}...")

        # Creamos el objeto de conexión
        conn = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            print("¡Conexión exitosa!")
            return conn

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def registrar_productor(nombre, correo, password, hectareas, filtros, telefono=None, semillas=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el correo ya existe
        cursor.execute("SELECT * FROM productor WHERE Correo = %s", (correo,))
        if cursor.fetchone():
            return {"success": False, "error": "El correo ya está registrado", "status": 400}
            
        # Insertar Productor
        password_hash = generate_password_hash(password)
        sql_productor = "INSERT INTO productor (Nombre, Correo, Contrasena, Telefono, Filtro_Agua) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_productor, (nombre, correo, password_hash, telefono, filtros))
        id_productor = cursor.lastrowid
        
        # Insertar Terreno
        m2 = float(hectareas) if hectareas else 0.0
        sql_terreno = "INSERT INTO terreno (Id_Productor, Metros_Cuadrados) VALUES (%s, %s)"
        cursor.execute(sql_terreno, (id_productor, m2))
            
        # Insertar Semillas en Inventario si existen
        if semillas and isinstance(semillas, list):
            for semilla in semillas:
                id_semilla = semilla.get('id_semilla')
                cantidad = semilla.get('cantidad', 0)
                
                # Buscar nombre de la semilla para el lote
                cursor.execute("SELECT Nombre_Semilla FROM semilla WHERE Id_Semilla = %s", (id_semilla,))
                res_s = cursor.fetchone()
                nombre_semilla = res_s['Nombre_Semilla'] if res_s else f"Semilla ID {id_semilla}"
                
                unidad = semilla.get('unidad', 'Kg')
                
                sql_inv = """
                    INSERT INTO inventario (Id_Productor, Lote, Cantidad, Unidad_Medida, Precio_Actual, Observaciones, Estado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_inv, (id_productor, f"Stock Inicial: {nombre_semilla}", float(cantidad), unidad, 0.0, "Cargado al registrarse", "En Bodega"))

        conexion.commit()
        return {"success": True, "id_productor": id_productor, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_productor: {e}")
        return {"success": False, "error": f"Error interno de base de datos: {str(e)}", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def login_productor(correo, password):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
        
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Validar credenciales
        sql = "SELECT * FROM productor WHERE Correo = %s"
        cursor.execute(sql, (correo,))
        productor = cursor.fetchone()
        
        if productor and check_password_hash(productor['Contrasena'], password):
            del productor['Contrasena'] # No enviar la contraseña
            return {"success": True, "user": productor, "status": 200}
        else:
            return {"success": False, "error": "Correo o contraseña incorrectos", "status": 401}
    except Error as e:
        print(f"Error en bd.login_productor: {e}")
        return {"success": False, "error": "Error interno de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_cliente(nombre, telefono, localidad, correo, password):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el correo ya existe
        cursor.execute("SELECT * FROM cliente WHERE Correo = %s", (correo,))
        if cursor.fetchone():
            return {"success": False, "error": "El correo ya está registrado", "status": 400}
            
        # Insertar Cliente
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO cliente (Nombre, Telefono, Localidad, Correo, Contrasena) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, telefono, localidad, correo, password_hash))
        id_cliente = cursor.lastrowid
            
        conexion.commit()
        return {"success": True, "id_cliente": id_cliente, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_cliente: {e}")
        return {"success": False, "error": "Error interno de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def login_cliente(correo, password):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
        
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Validar credenciales
        sql = "SELECT * FROM cliente WHERE Correo = %s"
        cursor.execute(sql, (correo,))
        cliente = cursor.fetchone()
        
        if cliente and check_password_hash(cliente['Contrasena'], password):
            del cliente['Contrasena']
            return {"success": True, "user": cliente, "status": 200}
        else:
            return {"success": False, "error": "Correo o contraseña incorrectos", "status": 401}
    except Error as e:
        print(f"Error en bd.login_cliente: {e}")
        return {"success": False, "error": "Error interno de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_cosechas_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT c.*, s.Nombre_Semilla, s.Valor AS Valor_Semilla, s.Tiempo_Produccion, s.pH_Optimo, s.Temporada AS Temporada_Semilla, c.Metros_Cuadrados
            FROM cosecha c
            LEFT JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
            WHERE c.Id_Productor = %s
        """
        cursor.execute(sql, (id_productor,))
        cosechas = cursor.fetchall()
        return {"success": True, "cosechas": cosechas, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_cosechas_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_categorias():
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria")
        categorias = cursor.fetchall()
        return {"success": True, "categorias": categorias, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_categorias: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_semillas(id_productor=None, id_categoria=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        if id_productor:
            # Buscamos en el inventario del productor específico
            sql = """
                SELECT i.Lote as Nombre_Semilla, i.Cantidad, 'Semillas' as Nombre_Categoria 
                FROM inventario i
                WHERE i.Id_Productor = %s AND i.Lote LIKE '%%Semilla%%'
            """
            cursor.execute(sql, (id_productor,))
        elif id_categoria:
            # Semillas por categoría
            sql = "SELECT * FROM semilla WHERE Id_Categoria = %s"
            cursor.execute(sql, (id_categoria,))
        else:
            # Catálogo general
            sql = """
                SELECT s.*, c.Nombre_Categoria 
                FROM semilla s 
                JOIN categoria c ON s.Id_Categoria = c.Id_Categoria
            """
            cursor.execute(sql)
            
        semillas = cursor.fetchall()
        return {"success": True, "semillas": semillas, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_semillas: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_stats_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # 1. Terreno Total
        cursor.execute("SELECT SUM(Metros_Cuadrados) as total_m2 FROM terreno WHERE Id_Productor = %s", (id_productor,))
        res_terreno = cursor.fetchone()
        terreno = res_terreno['total_m2'] if res_terreno and res_terreno['total_m2'] is not None else 0.0
        
        # 2. Cosechas Activas (de acuerdo a lo que se tiene en su inventario)
        cursor.execute("""
            SELECT COUNT(*) as activas 
            FROM inventario 
            WHERE Id_Productor = %s 
              AND Cantidad > 0 
              AND (Observaciones NOT LIKE '%%pH%%' AND Lote NOT LIKE 'Registro Tierra:%%')
        """, (id_productor,))
        res_activas = cursor.fetchone()
        activas = res_activas['activas'] if res_activas else 0
        
        # 3. Valor Neto Total (suma total de sus cosechas)
        cursor.execute("SELECT SUM(Valor_Neto) as valor FROM cosecha WHERE Id_Productor = %s", (id_productor,))
        res_valor = cursor.fetchone()
        valor = res_valor['valor'] if res_valor and res_valor['valor'] is not None else 0.0
        
        return {
            "success": True, 
            "stats": {
                "terreno_total": terreno,
                "cosechas_activas": activas,
                "valor_neto": valor
            }, 
            "status": 200
        }
    except Error as e:
        print(f"Error en bd.obtener_stats_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_inventario_productor(id_productor, tipo=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        # Filtramos según el tipo solicitado
        if tipo == 'cosecha':
            sql = """
                SELECT 
                    i.*,
                    p.Nombre AS Nombre_Productor,
                    s.Nombre_Semilla,
                    s.Valor AS Valor_Semilla,
                    s.Tiempo_Produccion,
                    s.pH_Optimo,
                    s.Id_Semilla,
                    c.Valor_Neto,
                    c.Fecha_Fin AS Fecha_Cosecha,
                    c.Metros_Cuadrados,
                    cat.Nombre_Categoria,
                    COALESCE((SELECT SUM(dv.Cantidad) FROM detalle_venta dv WHERE dv.Id_Inventario = i.Id_Inventario), 0) AS Cantidad_Vendida,
                    COALESCE((SELECT SUM(dv.Cantidad * dv.Precio_Unitario) FROM detalle_venta dv WHERE dv.Id_Inventario = i.Id_Inventario), 0) AS Total_Vendido_Monto
                FROM inventario i
                INNER JOIN productor p ON i.Id_Productor = p.Id_Productor
                LEFT JOIN cosecha c ON i.Id_Cosecha = c.Id_Cosecha
                LEFT JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
                LEFT JOIN categoria cat ON s.Id_Categoria = cat.Id_Categoria
                WHERE i.Id_Productor = %s AND (i.Observaciones NOT LIKE '%pH%' AND i.Lote NOT LIKE 'Registro Tierra:%')
            """
        else:
            sql = """
                SELECT 
                    i.*,
                    p.Nombre AS Nombre_Productor,
                    s.Nombre_Semilla,
                    s.Valor AS Valor_Semilla,
                    s.Tiempo_Produccion,
                    s.pH_Optimo,
                    s.Id_Semilla,
                    c.Valor_Neto,
                    c.Fecha_Fin AS Fecha_Cosecha,
                    c.Metros_Cuadrados,
                    cat.Nombre_Categoria,
                    COALESCE((SELECT SUM(dv.Cantidad) FROM detalle_venta dv WHERE dv.Id_Inventario = i.Id_Inventario), 0) AS Cantidad_Vendida,
                    COALESCE((SELECT SUM(dv.Cantidad * dv.Precio_Unitario) FROM detalle_venta dv WHERE dv.Id_Inventario = i.Id_Inventario), 0) AS Total_Vendido_Monto
                FROM inventario i
                INNER JOIN productor p ON i.Id_Productor = p.Id_Productor
                LEFT JOIN cosecha c ON i.Id_Cosecha = c.Id_Cosecha
                LEFT JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
                LEFT JOIN categoria cat ON s.Id_Categoria = cat.Id_Categoria
                WHERE i.Id_Productor = %s
            """
            
        cursor.execute(sql, (id_productor,))
        productos = cursor.fetchall()
        return {"success": True, "productos": productos, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_inventario_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_producto_inventario(id_productor, lote, cantidad, precio, observaciones, unidad_medida='Kg'):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "INSERT INTO inventario (Id_Productor, Lote, Cantidad, Unidad_Medida, Precio_Actual, Observaciones) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_productor, lote, float(cantidad), unidad_medida, float(precio), observaciones))
        id_inventario = cursor.lastrowid
        conexion.commit()
        return {"success": True, "id_inventario": id_inventario, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_producto_inventario: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def eliminar_producto_inventario(id_inventario, id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM inventario WHERE Id_Inventario = %s AND Id_Productor = %s"
        cursor.execute(sql, (id_inventario, id_productor))
        conexion.commit()
        if cursor.rowcount > 0:
            return {"success": True, "status": 200}
        else:
            return {"success": False, "error": "Registro no encontrado o sin permisos", "status": 404}
    except Error as e:
        print(f"Error en bd.eliminar_producto_inventario: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def eliminar_cosecha(id_cosecha, id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM cosecha WHERE Id_Cosecha = %s AND Id_Productor = %s AND Estatus = 'En proceso'"
        cursor.execute(sql, (id_cosecha, id_productor))
        conexion.commit()
        if cursor.rowcount > 0:
            return {"success": True, "status": 200}
        else:
            return {"success": False, "error": "Proyección no encontrada, ya cosechada o sin permisos", "status": 404}
    except Error as e:
        print(f"Error en bd.eliminar_cosecha: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()


def eliminar_cuenta_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM productor WHERE Id_Productor = %s"
        cursor.execute(sql, (id_productor,))
        conexion.commit()
        if cursor.rowcount > 0:
            return {"success": True, "status": 200}
        else:
            return {"success": False, "error": "Productor no encontrado", "status": 404}
    except Error as e:
        print(f"Error en bd.eliminar_cuenta_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_analiticas_globales():
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        from datetime import datetime
        mes_actual = datetime.now().month
        temporada_actual = "Primavera/Verano" if 2 <= mes_actual <= 7 else "Otoño/Invierno"
        
        cursor = conexion.cursor(dictionary=True)
        
        # Fetch all seeds and their categories
        cursor.execute("""
            SELECT s.*, c.Nombre_Categoria 
            FROM semilla s
            LEFT JOIN categoria c ON s.Id_Categoria = c.Id_Categoria
        """)
        semillas = cursor.fetchall()
        # Sort by name length descending to match the most specific name first (e.g. Zempoalxochitl (planta) before Zempoalxochitl)
        semillas_sorted = sorted(semillas, key=lambda x: len(x['Nombre_Semilla']), reverse=True)
        
        # Fetch all active inventory items
        cursor.execute("SELECT * FROM inventario WHERE Lote NOT LIKE 'Registro Tierra:%'")
        inventario = cursor.fetchall()
        
        # 1. Aggregate Volume and Value by Matched Seed
        seed_stats = {}
        for item in inventario:
            lote = item['Lote']
            matched_seed = None
            for s in semillas_sorted:
                if s['Nombre_Semilla'].lower() in lote.lower():
                    matched_seed = s
                    break
            
            name = matched_seed['Nombre_Semilla'] if matched_seed else lote
            cat = matched_seed['Nombre_Categoria'] if matched_seed else 'General'
            val = matched_seed['Valor'] if matched_seed and matched_seed['Valor'] is not None else 0.0
            
            if name not in seed_stats:
                seed_stats[name] = {
                    'Nombre_Semilla': name,
                    'Nombre_Categoria': cat,
                    'Total_Hectareas': 0.0,
                    'Valor_Semilla': val,
                    'Valor_Ganado': 0.0,
                    'Unidad_Medida': item['Unidad_Medida'] or 'Kg'
                }
            
            qty = item['Cantidad'] if item['Cantidad'] is not None else 0.0
            price = item['Precio_Actual'] if item['Precio_Actual'] is not None else 0.0
            
            seed_stats[name]['Total_Hectareas'] += qty
            seed_stats[name]['Valor_Ganado'] += qty * price

        volumen = list(seed_stats.values())
        volumen.sort(key=lambda x: x['Total_Hectareas'], reverse=True)
        
        # 2. Top Productores by Metros Cuadrados & Ganancia (Calculado antes de la inversión para reuso)
        cursor.execute("SELECT Id_Productor, Nombre FROM productor")
        productores = cursor.fetchall()
        
        producer_list = []
        for prod in productores:
            id_prod = prod['Id_Productor']
            cursor.execute("SELECT * FROM inventario WHERE Id_Productor = %s AND Lote NOT LIKE 'Registro Tierra:%'", (id_prod,))
            prod_inv = cursor.fetchall()
            
            ganancia_total = 0.0
            for item in prod_inv:
                qty = item['Cantidad'] if item['Cantidad'] is not None else 0.0
                price = item['Precio_Actual'] if item['Precio_Actual'] is not None else 0.0
                ganancia_total += qty * price
                
            # Fetch actual terrain size in square meters
            cursor.execute("SELECT SUM(Metros_Cuadrados) as total_m2 FROM terreno WHERE Id_Productor = %s", (id_prod,))
            res_terreno = cursor.fetchone()
            m2_total = res_terreno['total_m2'] if res_terreno and res_terreno['total_m2'] is not None else 0.0
                
            producer_list.append({
                'Nombre': prod['Nombre'],
                'Metros_Cuadrados': round(m2_total, 2),
                'Ganancia': round(ganancia_total, 2)
            })
            
        # 3. Inversion (mapeado para mostrar el Valor Ganado por Usuario Agricultor)
        inversion = []
        for prod in producer_list:
            if prod['Ganancia'] > 0:
                inversion.append({
                    'Nombre_Semilla': prod['Nombre'],
                    'Total_Valor': prod['Ganancia']
                })
        # Si no hay productores con ganancia, dejamos un marcador para evitar gráficos vacíos rotos
        if not inversion:
            inversion.append({
                'Nombre_Semilla': 'Sin datos de ganancias',
                'Total_Valor': 0.0
            })
            
        # Ordenar productores por Ganancia descendente y limitar a los top 5
        producer_list.sort(key=lambda x: x['Ganancia'], reverse=True)
        top_productores = producer_list[:5]
        
        # 4. KPIs
        # RIESGO: Seed with the highest volume in inventory
        riesgo = volumen[0]['Nombre_Semilla'] if volumen else "Equilibrado"
        
        # OPORTUNIDAD: Seed for current season (or Perennes) with lowest total quantity in inventory (representing high market opportunity)
        is_primavera_verano = (2 <= mes_actual <= 7)
        opportunity_seed = None
        min_qty = float('inf')
        
        for s in semillas:
            temporada = s['Temporada'].lower() if s['Temporada'] else ""
            # Match current season
            if is_primavera_verano and ('primavera' in temporada or 'perennes' in temporada):
                is_match = True
            elif not is_primavera_verano and ('oto' in temporada or 'perennes' in temporada):
                is_match = True
            else:
                is_match = False
                
            if is_match:
                # Calculate total qty in active inventory
                total_qty = 0.0
                for item in inventario:
                    if s['Nombre_Semilla'].lower() in item['Lote'].lower():
                        total_qty += item['Cantidad'] if item['Cantidad'] is not None else 0.0
                
                if total_qty < min_qty:
                    min_qty = total_qty
                    opportunity_seed = s
                    
        oportunidad = "Diversificado"
        if opportunity_seed:
            oportunidad = f"{opportunity_seed['Nombre_Semilla']} (pH Óptimo: {opportunity_seed['pH_Optimo']})"
            
        # Total Agricultores
        sql_total_prod = "SELECT COUNT(*) as total FROM productor"
        cursor.execute(sql_total_prod)
        total_prod = cursor.fetchone()
        
        return {
            "success": True, 
            "data": {
                "volumen": volumen,
                "inversion": inversion,
                "top_productores": top_productores,
                "temporada": temporada_actual,
                "kpis": {
                    "riesgo": riesgo,
                    "oportunidad": oportunidad,
                    "total_agricultores": total_prod['total'] if total_prod else 0
                }
            }, 
            "status": 200
        }
    except Error as e:
        print(f"Error en bd.obtener_analiticas_globales: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_publicacion_cosecha(id_productor, lote, cantidad, precio, vender_directamente, id_cosecha=None, unidad_medida='Kg', id_semilla=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Si no viene id_cosecha, intentamos crear una automáticamente
        if not id_cosecha:
            # 1. Buscar la semilla
            seed = None
            if id_semilla:
                cursor.execute("SELECT * FROM semilla WHERE Id_Semilla = %s", (id_semilla,))
                seed = cursor.fetchone()
            if not seed and lote:
                cursor.execute("SELECT * FROM semilla WHERE Nombre_Semilla = %s", (lote,))
                seed = cursor.fetchone()
            if not seed and lote:
                cursor.execute("SELECT * FROM semilla WHERE Nombre_Semilla LIKE %s LIMIT 1", (f"%{lote}%",))
                seed = cursor.fetchone()
                
            if seed:
                id_semilla_val = seed['Id_Semilla']
                temporada = seed['Temporada'] or 'Primavera-Verano'
                tiempo_prod = seed['Tiempo_Produccion'] or 90
                
                # 2. Buscar/crear terreno del productor
                cursor.execute("SELECT * FROM terreno WHERE Id_Productor = %s LIMIT 1", (id_productor,))
                terrain = cursor.fetchone()
                if not terrain:
                    cursor.execute("INSERT INTO terreno (Id_Productor, Metros_Cuadrados) VALUES (%s, %s)", (id_productor, 500.0))
                    conexion.commit()
                    cursor.execute("SELECT * FROM terreno WHERE Id_Productor = %s LIMIT 1", (id_productor,))
                    terrain = cursor.fetchone()
                
                id_terreno = terrain['Id_Terreno']
                
                # 3. Calcular Valor_Neto estimado para la cosecha con conversión de unidades
                precio_unitario = float(precio) if (precio and float(precio) > 0) else (float(seed['Precio_Venta']) if (seed.get('Precio_Venta') is not None and seed['Precio_Venta'] > 0) else float(seed['Valor']))
                
                id_cat = seed.get('Id_Categoria')
                # Determinar si la semilla es por peso o por pieza/conteo
                # Categorías por peso: 1 (Frutas), 4 (Granos), 5 (Tubérculos)
                es_peso = True
                if id_cat in [2, 3]: # Hortaliza de hoja, Ornamental / Flor
                    es_peso = False
                    
                cant_val = float(cantidad)
                uni = (unidad_medida or 'Kg').lower().strip()
                
                # Conversión a la unidad base de venta/precio
                if es_peso:
                    # La unidad de precio base es el Kg
                    if uni in ['kg', 'kilo', 'kilogramo', 'kilogramos']:
                        factor = 1.0
                    elif uni in ['gramos', 'gramo', 'gr', 'g']:
                        factor = 0.001
                    elif uni in ['libras', 'libra', 'lb', 'lbs']:
                        factor = 0.453592
                    elif uni in ['costales', 'costal']:
                        factor = 55.0
                    elif uni in ['bultos', 'bulto']:
                        factor = 50.0
                    else:
                        factor = 1.0
                else:
                    # La unidad de precio base es la pieza/manojo/unidad individual
                    if uni in ['unidades', 'unidad', 'pieza', 'piezas', 'manojos', 'manojo', 'tallos', 'tallo', 'esquejes', 'esqueje']:
                        factor = 1.0
                    elif uni in ['cajas', 'caja']:
                        factor = 20.0
                    elif uni in ['kg', 'kilo', 'kilogramo', 'kilogramos']:
                        factor = 10.0
                    else:
                        factor = 1.0
                        
                cantidad_base = cant_val * factor
                valor_neto = cantidad_base * precio_unitario
                
                # 4. Insertar la cosecha
                import datetime
                fecha_fin = datetime.date.today()
                fecha_inicio = fecha_fin - datetime.timedelta(days=int(tiempo_prod))
                
                m2_val = float(terrain['Metros_Cuadrados']) if (terrain and terrain.get('Metros_Cuadrados') is not None) else 500.0
                cursor.execute("""
                    INSERT INTO cosecha (Id_Productor, Id_Terreno, Id_Semilla, Temporada, Estatus, Fecha_Inicio, Fecha_Fin, Valor_Neto, Metros_Cuadrados)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_productor, id_terreno, id_semilla_val, temporada, 'Terminada', fecha_inicio, fecha_fin, valor_neto, m2_val))
                id_cosecha = cursor.lastrowid
        
        # Estado según el flujo: SI vender -> 'Publicado', NO -> 'En Bodega'
        estado = "Publicado" if vender_directamente else "En Bodega"
        precio_final = float(precio) if vender_directamente else 0.0
        
        sql = """
            INSERT INTO inventario 
            (Id_Productor, Id_Cosecha, Lote, Cantidad, Unidad_Medida, Precio_Actual, Observaciones, Estado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        obs = f"Registro automático desde formulario de cosecha. Estatus: {estado}"
        
        cursor.execute(sql, (id_productor, id_cosecha, lote, float(cantidad), unidad_medida, precio_final, obs, estado))
        id_inventario = cursor.lastrowid
        
        conexion.commit()
        return {"success": True, "id_inventario": id_inventario, "estado": estado, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_publicacion_cosecha: {e}")
        return {"success": False, "error": str(e), "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def actualizar_estado_inventario(id_inventario, estado, precio=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión"}
    
    try:
        cursor = conexion.cursor()
        if precio is not None:
            sql = "UPDATE inventario SET Estado = %s, Precio_Actual = %s WHERE Id_Inventario = %s"
            cursor.execute(sql, (estado, float(precio), id_inventario))
        else:
            sql = "UPDATE inventario SET Estado = %s WHERE Id_Inventario = %s"
            cursor.execute(sql, (estado, id_inventario))
        conexion.commit()
        return {"success": True}
    except Exception as e:
        print(f"Error en actualizar_estado_inventario: {e}")
        return {"success": False, "error": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_catalogo_publicado(busqueda=None):
    """Obtiene todos los productos publicados en la tienda, con nombre del productor y categoría."""
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT 
                i.Id_Inventario,
                i.Lote,
                i.Cantidad,
                i.Unidad_Medida,
                i.Precio_Actual,
                i.Estado,
                p.Nombre AS Nombre_Productor,
                p.Id_Productor,
                cat.Nombre_Categoria AS Categoria
            FROM inventario i
            JOIN productor p ON i.Id_Productor = p.Id_Productor
            LEFT JOIN cosecha c ON i.Id_Cosecha = c.Id_Cosecha
            LEFT JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
            LEFT JOIN categoria cat ON s.Id_Categoria = cat.Id_Categoria
            WHERE i.Estado = 'Publicado' AND i.Cantidad > 0
        """
        params = []
        if busqueda:
            sql += " AND i.Lote LIKE %s"
            params.append(f"%{busqueda}%")
        
        sql += " ORDER BY i.Id_Inventario DESC"
        cursor.execute(sql, params)
        productos = cursor.fetchall()
        return {"success": True, "productos": productos, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_catalogo_publicado: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def descontar_stock_inventario(id_inventario, cantidad_compra, id_cliente=None):
    """Descuenta stock de un producto tras una compra. Lo marca Agotado si llega a 0."""
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar stock actual y precio
        cursor.execute("SELECT Cantidad, Lote, Precio_Actual, Id_Productor FROM inventario WHERE Id_Inventario = %s AND Estado = 'Publicado'", (id_inventario,))
        producto = cursor.fetchone()
        
        if not producto:
            return {"success": False, "error": "Producto no disponible o no publicado", "status": 404}
        
        nuevo_stock = float(producto['Cantidad']) - float(cantidad_compra)
        
        if nuevo_stock < 0:
            return {"success": False, "error": f"Stock insuficiente. Disponible: {producto['Cantidad']}", "status": 400}
        
        # Actualizar stock; si llega a 0 -> Agotado
        nuevo_estado = 'Agotado' if nuevo_stock == 0 else 'Publicado'
        cursor.execute(
            "UPDATE inventario SET Cantidad = %s, Estado = %s WHERE Id_Inventario = %s",
            (nuevo_stock, nuevo_estado, id_inventario)
        )
        
        # Registrar en la tabla venta y detalle_venta si es posible
        try:
            if not id_cliente:
                # Buscar un cliente por defecto si no se pasa ID
                cursor.execute("SELECT Id_Cliente FROM cliente LIMIT 1")
                row = cursor.fetchone()
                if row:
                    id_cliente = row['Id_Cliente']
                else:
                    # Crear cliente general de respaldo si no hay ninguno
                    cursor.execute(
                        "INSERT INTO cliente (Nombre, Correo, Contrasena, Telefono, Localidad) VALUES (%s, %s, %s, %s, %s)",
                        ("Cliente General", "general@unrc.edu.mx", "pbkdf2:sha256:600000$hQ3Y7B8W$65c02b1f81014e7a83d7890fe0cfb0e9d6d84a7e93011a681c2e4726ef3565f1", "5500000000", "Xochimilco")
                    )
                    id_cliente = cursor.lastrowid
            
            precio_unitario = float(producto['Precio_Actual'])
            total_venta = float(cantidad_compra) * precio_unitario
            
            cursor.execute(
                "INSERT INTO venta (Id_Cliente, Total, Metodo_Pago, Estatus) VALUES (%s, %s, 'Efectivo', 'Completada')",
                (id_cliente, total_venta)
            )
            id_venta = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO detalle_venta (Id_Venta, Id_Inventario, Cantidad, Precio_Unitario) VALUES (%s, %s, %s, %s)",
                (id_venta, id_inventario, cantidad_compra, precio_unitario)
            )
        except Exception as e_venta:
            print(f"Error al registrar venta/detalle_venta: {e_venta}")
            # Continuamos aunque falle la inserción secundaria para no romper la compra
            
        conexion.commit()
        
        return {
            "success": True,
            "nuevo_stock": nuevo_stock,
            "estado": nuevo_estado,
            "lote": producto['Lote'],
            "status": 200
        }
    except Error as e:
        print(f"Error en bd.descontar_stock_inventario: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_perfil_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT Nombre, Correo, Telefono, Filtro_Agua FROM productor WHERE Id_Productor = %s"
        cursor.execute(sql, (id_productor,))
        perfil = cursor.fetchone()
        
        if perfil:
            cursor.execute("SELECT SUM(Metros_Cuadrados) as total_m2 FROM terreno WHERE Id_Productor = %s", (id_productor,))
            res_terreno = cursor.fetchone()
            perfil['Hectareas'] = res_terreno['total_m2'] if res_terreno and res_terreno['total_m2'] is not None else 0.0
            perfil.update({"Clabe": "", "Envio_Nacional": 1, "Alerta_Saturacion": 1, "Aviso_Compra": 1})
            return {"success": True, "perfil": perfil, "status": 200}
        else:
            return {"success": False, "error": "Productor no encontrado", "status": 404}
    except Error as e:
        print(f"Error en bd.obtener_perfil_productor: {e}")
        return {"success": False, "error": str(e), "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()
 
def actualizar_perfil_productor(id_productor, data):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE productor 
            SET Nombre = %s, Correo = %s, Telefono = %s, Filtro_Agua = %s
            WHERE Id_Productor = %s
        """
        cursor.execute(sql, (
            data.get('Nombre'), 
            data.get('Correo'), 
            data.get('Telefono'), 
            data.get('Filtro_Agua'), 
            id_productor
        ))

        # Actualizar terreno en metros cuadrados (recibido bajo la clave legacy 'Hectareas')
        hectareas_val = data.get('Hectareas')
        m2 = float(hectareas_val) if hectareas_val else 0.0
        
        cursor.execute("SELECT Id_Terreno FROM terreno WHERE Id_Productor = %s LIMIT 1", (id_productor,))
        terreno_row = cursor.fetchone()
        if terreno_row:
            cursor.execute("UPDATE terreno SET Metros_Cuadrados = %s WHERE Id_Terreno = %s", (m2, terreno_row[0]))
        else:
            cursor.execute("INSERT INTO terreno (Id_Productor, Metros_Cuadrados) VALUES (%s, %s)", (id_productor, m2))

        # 3. Actualizar contraseña si se requiere
        if data.get('password'):
            from werkzeug.security import generate_password_hash
            hashed_pw = generate_password_hash(data.get('password'))
            sql_pw = "UPDATE productor SET Contrasena = %s WHERE Id_Productor = %s"
            cursor.execute(sql_pw, (hashed_pw, id_productor))

        conexion.commit()
        return {"success": True, "status": 200}
    except Error as e:
        print(f"Error en bd.actualizar_perfil_productor: {e}")
        return {"success": False, "error": str(e), "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_estudiante(nombre, correo, password):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el correo ya existe en productores, clientes o estudiantes para evitar duplicados
        cursor.execute("SELECT * FROM estudiante WHERE Correo = %s", (correo,))
        if cursor.fetchone():
            return {"success": False, "error": "El correo ya está registrado", "status": 400}
            
        # Insertar Estudiante
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO estudiante (Nombre, Correo, Contrasena) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, correo, password_hash))
        id_estudiante = cursor.lastrowid
            
        conexion.commit()
        return {"success": True, "id_estudiante": id_estudiante, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_estudiante: {e}")
        return {"success": False, "error": f"Error interno de base de datos: {str(e)}", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def login_estudiante(correo, password):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión a la BD", "status": 500}
        
    try:
        cursor = conexion.cursor(dictionary=True)
        
        sql = "SELECT * FROM estudiante WHERE Correo = %s"
        cursor.execute(sql, (correo,))
        estudiante = cursor.fetchone()
        
        if estudiante and check_password_hash(estudiante['Contrasena'], password):
            del estudiante['Contrasena']
            return {"success": True, "user": estudiante, "status": 200}
        else:
            return {"success": False, "error": "Correo o contraseña incorrectos", "status": 401}
    except Error as e:
        print(f"Error en bd.login_estudiante: {e}")
        return {"success": False, "error": "Error interno de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_monitoreo(id_estudiante, id_productor, ph, salinidad, humedad, temperatura, observaciones):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            INSERT INTO monitoreo_chinampa 
            (Id_Estudiante, Id_Productor, PH, Salinidad, Humedad, Temperatura, Observaciones) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            id_estudiante, 
            id_productor, 
            float(ph) if ph is not None else None, 
            float(salinidad) if salinidad is not None else None, 
            float(humedad) if humedad is not None else None, 
            float(temperatura) if temperatura is not None else None, 
            observaciones
        ))
        id_monitoreo = cursor.lastrowid
        conexion.commit()
        return {"success": True, "id_monitoreo": id_monitoreo, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_monitoreo: {e}")
        return {"success": False, "error": f"Error de base de datos: {str(e)}", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_monitoreos_estudiante(id_estudiante):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT m.*, p.Nombre as Nombre_Productor 
            FROM monitoreo_chinampa m
            JOIN productor p ON m.Id_Productor = p.Id_Productor
            WHERE m.Id_Estudiante = %s
            ORDER BY m.Fecha DESC
        """
        cursor.execute(sql, (id_estudiante,))
        monitoreos = cursor.fetchall()
        
        # Convertir fechas a string para evitar problemas de serialización JSON
        for m in monitoreos:
            if m.get('Fecha'):
                m['Fecha'] = m['Fecha'].strftime('%Y-%m-%d %H:%M:%S')
                
        return {"success": True, "monitoreos": monitoreos, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_monitoreos_estudiante: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_productores():
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT Id_Productor, Nombre FROM productor ORDER BY Nombre ASC")
        productores = cursor.fetchall()
        return {"success": True, "productores": productores, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_productores: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_monitoreos_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT m.*, e.Nombre as Nombre_Estudiante
            FROM monitoreo_chinampa m
            JOIN estudiante e ON m.Id_Estudiante = e.Id_Estudiante
            WHERE m.Id_Productor = %s
            ORDER BY m.Fecha DESC
        """
        cursor.execute(sql, (id_productor,))
        monitoreos = cursor.fetchall()
        
        for m in monitoreos:
            m['Escuela'] = "UNRC"
            if m.get('Fecha'):
                m['Fecha'] = m['Fecha'].strftime('%Y-%m-%d %H:%M:%S')
                
        return {"success": True, "monitoreos": monitoreos, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_monitoreos_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def obtener_notificaciones_productor(id_productor):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    try:
        cursor = conexion.cursor(dictionary=True)
        # 1. Obtener monitoreos de los estudiantes
        sql_monitoreos = """
            SELECT m.Fecha, e.Nombre AS Nombre_Estudiante, 'monitoreo' AS Tipo, m.PH, m.Salinidad, m.Humedad, m.Temperatura, m.Observaciones, NULL AS Producto, NULL AS Cantidad, NULL AS Total
            FROM monitoreo_chinampa m
            JOIN estudiante e ON m.Id_Estudiante = e.Id_Estudiante
            WHERE m.Id_Productor = %s
        """
        cursor.execute(sql_monitoreos, (id_productor,))
        list_mon = cursor.fetchall()
        
        # 2. Obtener compras (ventas) asociadas a los productos del productor
        sql_compras = """
            SELECT v.Fecha_Venta AS Fecha, c.Nombre AS Nombre_Cliente, 'compra' AS Tipo, NULL AS PH, NULL AS Salinidad, NULL AS Humedad, NULL AS Temperatura, NULL AS Observaciones, i.Lote AS Producto, dv.Cantidad, (dv.Cantidad * dv.Precio_Unitario) AS Total
            FROM detalle_venta dv
            JOIN venta v ON dv.Id_Venta = v.Id_Venta
            JOIN cliente c ON v.Id_Cliente = c.Id_Cliente
            JOIN inventario i ON dv.Id_Inventario = i.Id_Inventario
            WHERE i.Id_Productor = %s
        """
        cursor.execute(sql_compras, (id_productor,))
        list_comp = cursor.fetchall()
        
        # Combinar ambas listas
        todas = []
        for item in list_mon:
            if item.get('Fecha'):
                item['Fecha'] = item['Fecha'].strftime('%Y-%m-%d %H:%M:%S')
            for col in ['PH', 'Salinidad', 'Humedad', 'Temperatura']:
                if item.get(col) is not None:
                    item[col] = float(item[col])
            todas.append(item)
            
        for item in list_comp:
            if item.get('Fecha'):
                item['Fecha'] = item['Fecha'].strftime('%Y-%m-%d %H:%M:%S')
            for col in ['Cantidad', 'Total']:
                if item.get(col) is not None:
                    item[col] = float(item[col])
            todas.append(item)
            
        # Ordenar por fecha descendente
        todas = sorted(todas, key=lambda x: x['Fecha'], reverse=True)
        
        return {"success": True, "notificaciones": todas, "status": 200}
    except Error as e:
        print(f"Error en bd.obtener_notificaciones_productor: {e}")
        return {"success": False, "error": "Error de base de datos", "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def registrar_siembra(id_productor, id_semilla, metros_cuadrados, temporada=None):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # 1. Buscar la semilla para conseguir temporada si no se proporciona
        cursor.execute("SELECT Temporada FROM semilla WHERE Id_Semilla = %s", (id_semilla,))
        seed = cursor.fetchone()
        if seed and not temporada:
            temporada = seed['Temporada'] or 'Primavera-Verano'
        elif not temporada:
            temporada = 'Primavera-Verano'
            
        # 2. Buscar/crear terreno del productor
        cursor.execute("SELECT Id_Terreno FROM terreno WHERE Id_Productor = %s LIMIT 1", (id_productor,))
        terrain = cursor.fetchone()
        if not terrain:
            # Crear terreno si no existe con un tamaño por defecto
            cursor.execute("INSERT INTO terreno (Id_Productor, Metros_Cuadrados) VALUES (%s, 500.0)", (id_productor,))
            conexion.commit()
            cursor.execute("SELECT Id_Terreno FROM terreno WHERE Id_Productor = %s LIMIT 1", (id_productor,))
            terrain = cursor.fetchone()
                
        id_terreno = terrain['Id_Terreno']
        
        # 3. Insertar la cosecha en proceso
        import datetime
        fecha_inicio = datetime.date.today()
        
        sql = """
            INSERT INTO cosecha (Id_Productor, Id_Terreno, Id_Semilla, Temporada, Estatus, Fecha_Inicio, Metros_Cuadrados)
            VALUES (%s, %s, %s, %s, 'En proceso', %s, %s)
        """
        cursor.execute(sql, (id_productor, id_terreno, id_semilla, temporada, fecha_inicio, float(metros_cuadrados or 0.0)))
        id_cosecha = cursor.lastrowid
        
        conexion.commit()
        return {"success": True, "id_cosecha": id_cosecha, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_siembra: {e}")
        return {"success": False, "error": str(e), "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()

def cosechar_cultivo(id_cosecha, cantidad, unidad_medida, precio_venta=0.0, vender_directamente=False):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # 1. Obtener datos de la cosecha en proceso
        cursor.execute("SELECT * FROM cosecha WHERE Id_Cosecha = %s AND Estatus = 'En proceso'", (id_cosecha,))
        cosecha_row = cursor.fetchone()
        if not cosecha_row:
            return {"success": False, "error": "Cosecha en proceso no encontrada", "status": 404}
            
        # 2. Buscar la semilla asociada
        cursor.execute("SELECT * FROM semilla WHERE Id_Semilla = %s", (cosecha_row['Id_Semilla'],))
        seed = cursor.fetchone()
        nombre_semilla = seed['Nombre_Semilla'] if seed else 'Cultivo Cosechado'
        id_cat = seed['Id_Categoria'] if seed else None
        
        # Determinar si la semilla es por peso o conteo para conversión
        es_peso = True
        if id_cat in [2, 3]: # Hortaliza de hoja, Ornamental / Flor
            es_peso = False
            
        cant_val = float(cantidad)
        uni = (unidad_medida or 'Kg').lower().strip()
        
        if es_peso:
            if uni in ['kg', 'kilo', 'kilogramo', 'kilogramos']:
                factor = 1.0
            elif uni in ['gramos', 'gramo', 'gr', 'g']:
                factor = 0.001
            elif uni in ['libras', 'libra', 'lb', 'lbs']:
                factor = 0.453592
            elif uni in ['costales', 'costal']:
                factor = 55.0
            elif uni in ['bultos', 'bulto']:
                factor = 50.0
            else:
                factor = 1.0
        else:
            if uni in ['unidades', 'unidad', 'pieza', 'piezas', 'manojos', 'manojo', 'tallos', 'tallo', 'esquejes', 'esqueje']:
                factor = 1.0
            elif uni in ['cajas', 'caja']:
                factor = 20.0
            elif uni in ['kg', 'kilo', 'kilogramo', 'kilogramos']:
                factor = 10.0
            else:
                factor = 1.0
                
        cantidad_base = cant_val * factor
        
        # Precio unitario final
        precio_unitario = float(precio_venta) if (vender_directamente and precio_venta and float(precio_venta) > 0) else (float(seed['Precio_Venta']) if (seed and seed.get('Precio_Venta') is not None and seed['Precio_Venta'] > 0) else (float(seed['Valor']) if seed else 10.0))
        valor_neto = cantidad_base * precio_unitario
        
        # 3. Finalizar la cosecha
        import datetime
        fecha_fin = datetime.date.today()
        cursor.execute("""
            UPDATE cosecha 
            SET Estatus = 'Terminada', Fecha_Fin = %s, Valor_Neto = %s
            WHERE Id_Cosecha = %s
        """, (fecha_fin, valor_neto, id_cosecha))
        
        # 4. Insertar lote en inventario
        estado = 'Publicado' if vender_directamente else 'En Bodega'
        precio_inventario = float(precio_venta) if vender_directamente else 0.0
        obs = f"Cosechado desde ciclo activo. Estatus: {estado}"
        
        sql_inv = """
            INSERT INTO inventario 
            (Id_Productor, Id_Cosecha, Lote, Cantidad, Unidad_Medida, Precio_Actual, Observaciones, Estado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_inv, (
            cosecha_row['Id_Productor'], 
            id_cosecha, 
            f"Lote {nombre_semilla}", 
            float(cantidad), 
            unidad_medida, 
            precio_inventario, 
            obs, 
            estado
        ))
        id_inventario = cursor.lastrowid
        
        conexion.commit()
        return {"success": True, "id_inventario": id_inventario, "estado": estado, "status": 201}
    except Error as e:
        print(f"Error en bd.cosechar_cultivo: {e}")
        return {"success": False, "error": str(e), "status": 500}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conexion.is_connected():
            conexion.close()


