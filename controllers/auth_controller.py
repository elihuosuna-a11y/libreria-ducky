"""
controllers/auth_controller.py
CONTROLADOR - Maneja las transiciones del Estado E1 (Autenticacion).

Transiciones implementadas:
  T01 - Conexion al componente (mostrar pantalla de login)
  T02 - Login invalido (usuario/contrasena incorrectos)
  T03 - Login invalido (campos vacios)
  T04 - Login exitoso -> ir a E2 (Catalogo)
  T05 - Salir del sistema desde E1
  T19 - Cerrar sesion desde E2 -> regresa a E1
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario_model import UsuarioModel

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET'])
def mostrar_login():
    """
    T01 - Conexion al componente.
    Presenta la pantalla de login con campos en blanco.
    """
    # Si ya hay sesion activa, ir directo al catalogo
    if session.get('usuario'):
        return redirect(url_for('catalogo.mostrar_catalogo'))

    return render_template('auth/login.html', error=None, datos={})


@auth_bp.route('/login', methods=['POST'])
def procesar_login():
    """
    Procesa el formulario de login.
    Implementa T02, T03 y T04 segun el resultado de la validacion.
    """
    usuario = request.form.get('usuario', '').strip()
    contrasena = request.form.get('contrasena', '')

    # --- T03: Login invalido (campos vacios) ---
    if not usuario or not contrasena:
        return render_template(
            'auth/login.html',
            error='Datos requeridos. Por favor completa todos los campos.',
            datos={'usuario': usuario}
        )

    # --- T02: Login invalido (credenciales incorrectas) ---
    usuario_valido = UsuarioModel.validar_credenciales(usuario, contrasena)
    if not usuario_valido:
        return render_template(
            'auth/login.html',
            error='Credenciales incorrectas.',
            datos={'usuario': usuario}
        )

    # --- T04: Login exitoso -> ir a E2 ---
    session['usuario'] = usuario_valido
    return redirect(url_for('catalogo.mostrar_catalogo'))


@auth_bp.route('/logout')
def cerrar_sesion():
    """
    T05 / T19 - Cerrar sesion.
    Destruye la sesion y regresa a la pantalla de Autenticacion.
    """
    session.clear()
    return redirect(url_for('auth.mostrar_login'))