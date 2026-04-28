"""
app.py
Punto de entrada de la aplicacion Libreria Ducky.
Configura Flask, sesiones y registra los blueprints (controladores).
"""

from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.catalogo_controller import catalogo_bp

app = Flask(__name__)

# Clave secreta requerida para manejar sesiones de usuario
app.secret_key = 'libreria-ducky-secret-key-2026'

# Registro de blueprints (cada uno representa un modulo del sistema)
app.register_blueprint(auth_bp)                              # E1: Autenticacion
app.register_blueprint(catalogo_bp, url_prefix='/catalogo')  # E2: Catalogo


@app.route('/')
def index():
    """Ruta raiz: redirige a la pantalla de login."""
    return redirect(url_for('auth.mostrar_login'))


if __name__ == '__main__':
    print('Servidor Libreria Ducky corriendo en http://localhost:5000')
    app.run(debug=True, port=5000)