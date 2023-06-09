import mysql.connector

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="sasa",
    database="agency"
)

# Verificar si la conexión fue exitosa
if conexion.is_connected():
    print("Conexión exitosa a la base de datos")

    # Ejecutar consultas
    # Aquí puedes agregar tu código para realizar las consultas y operaciones en la base de datos

    # Cerrar la conexión
    conexion.close()
    print("Conexión cerrada")
else:
    print("Error al conectar a la base de datos")
