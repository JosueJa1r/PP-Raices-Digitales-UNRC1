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
        if hectareas:
            sql_terreno = "INSERT INTO terreno (Id_Productor) VALUES (%s)"
            cursor.execute(sql_terreno, (id_productor,))
            
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
        sql = "SELECT * FROM cosecha WHERE Id_Productor = %s"
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
        cursor.execute("SELECT COUNT(*) as total_terrenos FROM terreno WHERE Id_Productor = %s", (id_productor,))
        res_terreno = cursor.fetchone()
        terreno = (res_terreno['total_terrenos'] * 200.0) if res_terreno and res_terreno['total_terrenos'] else 200.0
        
        # 2. Cosechas Activas
        cursor.execute("SELECT COUNT(*) as activas FROM cosecha WHERE Id_Productor = %s AND Estatus = 'Activa'", (id_productor,))
        res_activas = cursor.fetchone()
        activas = res_activas['activas'] if res_activas else 0
        
        # 3. Valor Neto Total (de cosechas activas)
        cursor.execute("SELECT SUM(Valor_Neto) as valor FROM cosecha WHERE Id_Productor = %s AND Estatus = 'Activa'", (id_productor,))
        res_valor = cursor.fetchone()
        valor = res_valor['valor'] if res_valor and res_valor['valor'] else 0
        
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
            sql = "SELECT * FROM inventario WHERE Id_Productor = %s AND (Observaciones NOT LIKE '%pH%' AND Lote NOT LIKE 'Registro Tierra:%')"
        elif tipo == 'insumo':
            # Mostrar todo el inventario de la base de datos tal como el usuario lo solicita
            sql = "SELECT * FROM inventario WHERE Id_Productor = %s"
        else:
            sql = "SELECT * FROM inventario WHERE Id_Productor = %s"
            
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
                    'Valor_Ganado': 0.0
                }
            
            qty = item['Cantidad'] if item['Cantidad'] is not None else 0.0
            price = item['Precio_Actual'] if item['Precio_Actual'] is not None else 0.0
            
            seed_stats[name]['Total_Hectareas'] += qty
            seed_stats[name]['Valor_Ganado'] += qty * price

        volumen = list(seed_stats.values())
        volumen.sort(key=lambda x: x['Total_Hectareas'], reverse=True)
        
        # 2. Inversion (using the same seed stats, mapped to the legacy key Total_Valor for the frontend charts)
        inversion = []
        for v in volumen:
            inversion.append({
                'Nombre_Semilla': v['Nombre_Semilla'],
                'Total_Valor': v['Valor_Ganado']
            })
            
        # 3. Top Productores by Metros Cuadrados & Ganancia
        cursor.execute("SELECT Id_Productor, Nombre FROM productor")
        productores = cursor.fetchall()
        
        producer_list = []
        for prod in productores:
            id_prod = prod['Id_Productor']
            cursor.execute("SELECT * FROM inventario WHERE Id_Productor = %s AND Lote NOT LIKE 'Registro Tierra:%'", (id_prod,))
            prod_inv = cursor.fetchall()
            
            ganancia_total = 0.0
            m2_total = 0.0
            
            for item in prod_inv:
                qty = item['Cantidad'] if item['Cantidad'] is not None else 0.0
                price = item['Precio_Actual'] if item['Precio_Actual'] is not None else 0.0
                
                ganancia_total += qty * price
                m2_total += qty * 10000.0
                
            producer_list.append({
                'Nombre': prod['Nombre'],
                'Metros_Cuadrados': round(m2_total, 2),
                'Ganancia': round(ganancia_total, 2)
            })
            
        # Sort by Ganancia descending and limit to top 5
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

def registrar_publicacion_cosecha(id_productor, lote, cantidad, precio, vender_directamente, id_cosecha=None, unidad_medida='Kg'):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
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

def actualizar_estado_inventario(id_inventario, estado):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión"}
    
    try:
        cursor = conexion.cursor()
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
    """Obtiene todos los productos publicados en la tienda, con nombre del productor."""
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
                i.Precio_Actual,
                i.Estado,
                p.Nombre AS Nombre_Productor,
                p.Id_Productor
            FROM inventario i
            JOIN productor p ON i.Id_Productor = p.Id_Productor
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

def descontar_stock_inventario(id_inventario, cantidad_compra):
    """Descuenta stock de un producto tras una compra. Lo marca Agotado si llega a 0."""
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar stock actual
        cursor.execute("SELECT Cantidad, Lote FROM inventario WHERE Id_Inventario = %s AND Estado = 'Publicado'", (id_inventario,))
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
        sql = "SELECT Nombre, Correo, Telefono, Tipo_Suelo, Filtro_Agua FROM productor WHERE Id_Productor = %s"
        cursor.execute(sql, (id_productor,))
        perfil = cursor.fetchone()
        
        if perfil:
            perfil['Hectareas'] = 10.0
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
            SET Nombre = %s, Correo = %s, Telefono = %s, Tipo_Suelo = %s, Filtro_Agua = %s
            WHERE Id_Productor = %s
        """
        cursor.execute(sql, (
            data.get('Nombre'), 
            data.get('Correo'), 
            data.get('Telefono'), 
            data.get('Tipo_Suelo'), 
            data.get('Filtro_Agua'), 
            id_productor
        ))

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

