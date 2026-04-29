from decouple import config

#  Notocar JOSUE
def conexion_db():
    database = config('MYSQL_DATABASE')
    print("Conectando a la base de datos:", database)   

conexion_db()
##########################################

conexion = conexion_db()
cursor = conexion.cursor()
cursor.execute("SELECT * FROM ")

