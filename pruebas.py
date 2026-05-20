import pandas as pd
import mysql.connector
from mysql.connector import Error
from decouple import config

def conexion_db():
    try:
        conn = mysql.connector.connect(
            host=config('MYSQL_HOST', default='localhost'),
            port=config('MYSQL_PORT', default='3306', cast=int),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DATABASE')
        )
        return conn if conn.is_connected() else None
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return None

def actualizador_universal_csv():
    print("\n" + "="*40)
    print("🚀 ACTUALIZADOR UNIVERSAL DE BASE DE DATOS")
    print("="*40)
    
    ruta_csv = input("📂 1. Ruta del archivo CSV: ")
    
    try:
        # Cargar CSV y mostrar columnas
        df = pd.read_csv(ruta_csv)
        print(f"\n✅ CSV cargado. Columnas encontradas: {list(df.columns)}")
        
        # 1. Configuración de la Tabla
        tabla = input("\n📊 2. Nombre de la tabla en MySQL (ej: semilla): ")
        
        # 2. Configuración de las columnas de vinculación (El "ID" o Nombre)
        print("\n--- Vincular por (Ej: Nombre_Semilla) ---")
        col_csv_key = input("🔑 Nombre de la columna en el CSV que es la llave: ")
        col_db_key = input("🔑 Nombre de la columna en la Base de Datos que es la llave: ")
        
        # 3. Configuración de los datos a actualizar
        print("\n--- Dato a actualizar (Ej: Tiempo_Produccion) ---")
        col_csv_val = input("📝 Nombre de la columna en el CSV con el nuevo dato: ")
        col_db_val = input("📝 Nombre de la columna en la Base de Datos a modificar: ")

        conexion = conexion_db()
        if conexion:
            cursor = conexion.cursor()
            actualizados = 0
            errores = 0

            print("\n⏳ Procesando...")
            
            for index, row in df.iterrows():
                val_key = row[col_csv_key]
                val_nuevo = row[col_csv_val]

                # SQL Dinámico: UPDATE {tabla} SET {col_datos} = %s WHERE {col_llave} = %s
                sql = f"UPDATE {tabla} SET {col_db_val} = %s WHERE {col_db_key} = %s"
                
                try:
                    cursor.execute(sql, (val_nuevo, val_key))
                    if cursor.rowcount > 0:
                        actualizados += 1
                except Exception:
                    errores += 1

            conexion.commit()
            print(f"\n" + "-"*40)
            print(f"✅ PROCESO TERMINADO")
            print(f"🔹 Registros actualizados: {actualizados}")
            if errores > 0:
                print(f"🔸 Errores encontrados: {errores}")
            print("-"*40)
            
            cursor.close()
            conexion.close()

    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo CSV.")
    except KeyError as e:
        print(f"❌ Error: La columna {e} no existe en tu archivo CSV.")
    except Exception as e:
        print(f"❌ Ocurrió un problema: {e}")

if __name__ == '__main__':
    actualizador_universal_csv()
