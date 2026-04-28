"""
models/usuario_model.py
MODELO - Encapsula el acceso a la tabla Usuarios.
Solo se comunica con la base de datos; no contiene logica de presentacion
ni de manejo de peticiones HTTP.
"""

import bcrypt
from models.database import get_connection


class UsuarioModel:

    @staticmethod
    def buscar_por_usuario(usuario):
        """Busca un usuario por su matricula/nomina."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Usuario = ?', (usuario,))
        registro = cursor.fetchone()
        conn.close()
        return registro

    @staticmethod
    def validar_credenciales(usuario, contrasena):
        """
        Valida credenciales de inicio de sesion.
        Compara la contrasena contra el hash almacenado.

        Retorna un dict con datos del usuario si es valido; None en caso contrario.
        """
        registro = UsuarioModel.buscar_por_usuario(usuario)
        if not registro:
            return None

        hash_guardado = registro['Contrasena'].encode('utf-8')
        es_valida = bcrypt.checkpw(contrasena.encode('utf-8'), hash_guardado)
        if not es_valida:
            return None

        # Nunca regresar el hash de la contrasena al controlador
        return {
            'usuario': registro['Usuario'],
            'nombre': registro['Nombre'],
            'email': registro['Email']
        }