from dotenv import load_dotenv
from peewee import *

import os

load_dotenv()

# Conexión a la base de datos MySQL
database = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
)

# Definición del modelo de usuario
class UserModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    age = CharField(max_length=50)
    email = CharField(max_length=50)
    adress = CharField(max_length=50)
    document = CharField(max_length=50)

    class Meta:
        database = database  # Conexión a la base de datos
        table_name = "user"  # Debe coincidir con la tabla en MySQL

# Prueba de conexión
try:
    database.connect()
    print("Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"Error conectando a la base de datos: {e}")
finally:
    database.close()
