import mysql.connector
from decouple import config
from mysql.connector import Error

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

def registrar_productor(nombre, correo, password, hectareas, filtros):
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
        sql_productor = "INSERT INTO productor (Nombre, Correo, Contrasena) VALUES (%s, %s, %s)"
        cursor.execute(sql_productor, (nombre, correo, password))
        id_productor = cursor.lastrowid
        
        # Insertar Terreno
        if hectareas and filtros:
            sql_terreno = "INSERT INTO terreno (Id_Productor, Hectareas, Nombre_Filtro) VALUES (%s, %s, %s)"
            cursor.execute(sql_terreno, (id_productor, float(hectareas), filtros))
            
        conexion.commit()
        return {"success": True, "id_productor": id_productor, "status": 201}
    except Error as e:
        print(f"Error en bd.registrar_productor: {e}")
        return {"success": False, "error": "Error interno de base de datos", "status": 500}
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
        sql = "SELECT * FROM productor WHERE Correo = %s AND Contrasena = %s"
        cursor.execute(sql, (correo, password))
        productor = cursor.fetchone()
        
        if productor:
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
