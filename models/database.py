"""
models/database.py
Maneja la conexion a la base de datos SQLite.
SQLite forma parte de la biblioteca estandar de Python; no requiere instalacion.
"""

import sqlite3
import os

# Ruta absoluta al archivo de la BD
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'libreria.db')


def get_connection():
    """Crea y retorna una conexion a la BD con filas accesibles por nombre."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    conn.execute('PRAGMA foreign_keys = ON')
    return conn