"""
controllers/catalogo_controller.py
CONTROLADOR - Maneja las transiciones del Estado E2 (Catalogo de Libros).

Transiciones implementadas en esta evidencia:
  T04 - (entrada) Login exitoso -> mostrar catalogo
  T06 - Filtro aplicado (Titulo / Autor / ISBN)
  T07 - Paginacion (avanzar/retroceder)
  T19 - Cerrar sesion desde E2 (delegado a auth.cerrar_sesion)

Transiciones pendientes para Proyecto Final:
  T08 - Clic en "Nuevo Libro"  -> E3
  T09 - Clic en "Ver detalles" -> E4
  T10 - Clic en "Editar"       -> E5
  T11 - Clic en "Eliminar"     -> E6
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.libro_model import LibroModel

catalogo_bp = Blueprint('catalogo', __name__)


def requiere_sesion(f):
    """Decorador que protege rutas exigiendo sesion activa."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('usuario'):
            return redirect(url_for('auth.mostrar_login'))
        return f(*args, **kwargs)
    return wrapper


@catalogo_bp.route('/')
@requiere_sesion
def mostrar_catalogo():
    """
    Muestra la pantalla de catalogo con filtros y paginacion.
    Implementa T06 y T07.
    """
    filtro = request.args.get('filtro', '')
    campo = request.args.get('campo', 'todos')

    try:
        pagina = int(request.args.get('pagina', 1))
    except ValueError:
        pagina = 1

    por_pagina = 5
    resultado = LibroModel.listar(
        filtro=filtro,
        campo=campo,
        pagina=pagina,
        por_pagina=por_pagina
    )

    return render_template(
        'catalogo/index.html',
        libros=resultado['libros'],
        total=resultado['total'],
        pagina_actual=pagina,
        total_paginas=resultado['total_paginas'],
        filtro=filtro,
        campo=campo
    )