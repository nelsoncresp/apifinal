import mysql.connector
from contextlib import contextmanager

# Configuración de la conexión
mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'BD_PAGINA_WEB',
    'auth_plugin': 'mysql_native_password'
}

@contextmanager
def get_connection():
    connection = mysql.connector.connect(**mysql_config)
    try:
        yield connection
    finally:
        connection.close()
