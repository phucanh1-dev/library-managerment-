import pyodbc
from config import DATABASE_CONFIG

def get_connection():
    connection_string = (
    f"DRIVER={DATABASE_CONFIG['driver']};"
    f"SERVER={DATABASE_CONFIG['server']};"
    f"DATABASE={DATABASE_CONFIG['database']};"
    f"Trusted_Connection={DATABASE_CONFIG['trusted_connection']};"
    f"charset=utf8;"
    )
    return pyodbc.connect(connection_string)
