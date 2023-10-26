import pymongo

# Valores de configuración
DATABASE_USER = "BotPacifico_user"
DATABASE_PASSWORD = "BotPacifico_password"
DATABASE_HOST = "BotPacifico_db"
DATABASE_PORT = 27017
DATABASE_NAME = "BotPacifico_db"

# Crear una conexión a la base de datos
client = pymongo.MongoClient(
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
)

# Crear una base de datos
db = client[DATABASE_NAME]

# Verificar si la base de datos se creó correctamente
if DATABASE_NAME in client.list_database_names():
    print(f"Base de datos '{DATABASE_NAME}' creada con éxito.")
else:
    print(f"No se pudo crear la base de datos '{DATABASE_NAME}'.")

# Cerrar la conexión
client.close()
