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
        sql_productor = "INSERT INTO productor (Nombre, Correo, Contrasena, Telefono) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_productor, (nombre, correo, password_hash, telefono))
        id_productor = cursor.lastrowid
        
        # Insertar Terreno
        if hectareas:
            # Convertir m2 a hectáreas (1 ha = 10,000 m2)
            hec = float(hectareas) / 10000
            sql_terreno = "INSERT INTO terreno (Id_Productor, Hectareas, Nombre_Filtro) VALUES (%s, %s, %s)"
            cursor.execute(sql_terreno, (id_productor, hec, filtros or "General"))
            
        # Insertar Semillas en Inventario si existen
        if semillas and isinstance(semillas, list):
            for semilla in semillas:
                id_semilla = semilla.get('id_semilla')
                cantidad = semilla.get('cantidad', 0)
                
                # Buscar nombre de la semilla para el lote
                cursor.execute("SELECT Nombre_Semilla FROM semilla WHERE Id_Semilla = %s", (id_semilla,))
                res_s = cursor.fetchone()
                nombre_semilla = res_s['Nombre_Semilla'] if res_s else f"Semilla ID {id_semilla}"
                
                sql_inv = """
                    INSERT INTO inventario (Id_Productor, Lote, Cantidad, Precio_Actual, Observaciones, Estado) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_inv, (id_productor, f"Stock Inicial: {nombre_semilla}", float(cantidad), 0.0, "Cargado al registrarse", "En Bodega"))

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
        cursor.execute("SELECT SUM(Hectareas) as total FROM terreno WHERE Id_Productor = %s", (id_productor,))
        res_terreno = cursor.fetchone()
        terreno = res_terreno['total'] if res_terreno and res_terreno['total'] else 0
        
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

def registrar_producto_inventario(id_productor, lote, cantidad, precio, observaciones):
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "INSERT INTO inventario (Id_Productor, Lote, Cantidad, Precio_Actual, Observaciones) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_productor, lote, float(cantidad), float(precio), observaciones))
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

def obtener_analiticas_globales():
    conexion = conexion_db()
    if not conexion:
        return {"success": False, "error": "Error de conexión", "status": 500}
    
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # 1. Volumen de Plantación por Producto (Semilla)
        sql_volumen = """
            SELECT s.Nombre_Semilla, SUM(t.Hectareas) as Total_Hectareas
            FROM cosecha c
            JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
            JOIN terreno t ON c.Id_Terreno = t.Id_Terreno
            GROUP BY s.Nombre_Semilla
            ORDER BY Total_Hectareas DESC
        """
        cursor.execute(sql_volumen)
        volumen = cursor.fetchall()
        
        # 2. Inversión por Valor de Semilla
        sql_inversion = """
            SELECT s.Nombre_Semilla, SUM(s.Valor) as Total_Valor
            FROM cosecha c
            JOIN semilla s ON c.Id_Semilla = s.Id_Semilla
            GROUP BY s.Nombre_Semilla
        """
        cursor.execute(sql_inversion)
        inversion = cursor.fetchall()
        
        # 3. Top Productores por Extensión
        sql_top = """
            SELECT p.Nombre, SUM(t.Hectareas) as Extension
            FROM productor p
            JOIN terreno t ON p.Id_Productor = t.Id_Productor
            GROUP BY p.Nombre
            ORDER BY Extension DESC
            LIMIT 5
        """
        cursor.execute(sql_top)
        top_productores = cursor.fetchall()
        
        # 4. Métricas para KPIs (Tarjetas superiores)
        # Producto más plantado
        sql_riesgo = "SELECT s.Nombre_Semilla FROM cosecha c JOIN semilla s ON c.Id_Semilla = s.Id_Semilla GROUP BY s.Nombre_Semilla ORDER BY COUNT(*) DESC LIMIT 1"
        cursor.execute(sql_riesgo)
        riesgo = cursor.fetchone()
        
        # Producto menos plantado (Oportunidad)
        sql_oportunidad = "SELECT s.Nombre_Semilla FROM cosecha c JOIN semilla s ON c.Id_Semilla = s.Id_Semilla GROUP BY s.Nombre_Semilla ORDER BY COUNT(*) ASC LIMIT 1"
        cursor.execute(sql_oportunidad)
        oportunidad = cursor.fetchone()
        
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
                "kpis": {
                    "riesgo": riesgo['Nombre_Semilla'] if riesgo else "N/A",
                    "oportunidad": oportunidad['Nombre_Semilla'] if oportunidad else "N/A",
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

def registrar_publicacion_cosecha(id_productor, lote, cantidad, precio, vender_directamente, id_cosecha=None):
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
            (Id_Productor, Id_Cosecha, Lote, Cantidad, Precio_Actual, Observaciones, Estado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        obs = f"Registro automático desde formulario de cosecha. Estatus: {estado}"
        
        cursor.execute(sql, (id_productor, id_cosecha, lote, float(cantidad), precio_final, obs, estado))
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
