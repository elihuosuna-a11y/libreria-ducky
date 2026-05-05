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
# ================================================================
# E4 - DETALLES DEL LIBRO
# ================================================================

@catalogo_bp.route('/detalles/<isbn>')
@requiere_sesion
def mostrar_detalles(isbn):
    """
    T09 - Clic en "Ver detalles" desde E2 -> E4.
    Presenta la informacion completa del libro seleccionado.

    T16 - Volver desde E4 -> E2 se maneja con un enlace en la vista
    que regresa al catalogo.
    """
    libro = LibroModel.buscar_por_isbn(isbn)

    # Si el ISBN no existe, regresar al catalogo
    if not libro:
        return redirect(url_for('catalogo.mostrar_catalogo'))

    return render_template('catalogo/detalles.html', libro=libro)
# ================================================================
# E3 - INGRESAR NUEVO LIBRO
# ================================================================

@catalogo_bp.route('/nuevo', methods=['GET'])
@requiere_sesion
def mostrar_nuevo():
    """
    T08 - Clic en "Nuevo Libro +" desde E2 -> E3.
    Presenta el formulario con todos los campos en blanco.
    """
    return render_template('catalogo/nuevo.html', error=None, datos={})


@catalogo_bp.route('/nuevo', methods=['POST'])
@requiere_sesion
def procesar_nuevo():
    """
    Procesa el alta de un nuevo libro.
    Implementa T12, T13 y T14 segun el resultado de la validacion.
    """
    # Recopilar datos del formulario
    datos = {
        'isbn':            request.form.get('isbn', '').strip(),
        'titulo':          request.form.get('titulo', '').strip(),
        'autor':           request.form.get('autor', '').strip(),
        'editorial':       request.form.get('editorial', '').strip(),
        'sinopsis':        request.form.get('sinopsis', '').strip(),
        'ano_publicacion': request.form.get('ano_publicacion', '').strip(),
        'numero_paginas':  request.form.get('numero_paginas', '').strip(),
        'precio':          request.form.get('precio', '').strip(),
        'ubicacion':       request.form.get('ubicacion', '').strip(),
        'numero_copias':   request.form.get('numero_copias', '').strip(),
        'categoria':       request.form.get('categoria', '').strip()
    }

    # --- T13: Alta invalida (datos requeridos) ---
    campos_requeridos = ['isbn', 'titulo', 'autor', 'editorial', 'sinopsis',
                         'ano_publicacion', 'numero_paginas', 'precio',
                         'ubicacion', 'numero_copias', 'categoria']
    campos_vacios = [c for c in campos_requeridos if not datos[c]]

    if campos_vacios:
        return render_template(
            'catalogo/nuevo.html',
            error='Datos requeridos. Por favor completa todos los campos.',
            datos=datos,
            campos_error=campos_vacios
        )

    # --- T12: Alta invalida (ISBN ya existe) ---
    if LibroModel.isbn_existe(datos['isbn']):
        return render_template(
            'catalogo/nuevo.html',
            error='Libro ya existe. El ISBN ingresado ya está registrado.',
            datos=datos,
            campos_error=['isbn']
        )

    # Conversion de tipos numericos
    try:
        datos['ano_publicacion'] = int(datos['ano_publicacion'])
        datos['numero_paginas']  = int(datos['numero_paginas'])
        datos['numero_copias']   = int(datos['numero_copias'])
        datos['precio']          = float(datos['precio'])
    except ValueError:
        return render_template(
            'catalogo/nuevo.html',
            error='Datos invalidos. Verifica los campos numericos.',
            datos=datos,
            campos_error=['ano_publicacion', 'numero_paginas',
                          'numero_copias', 'precio']
        )

    # --- T14: Alta exitosa -> regresar a E2 ---
    LibroModel.crear(datos)
    return redirect(url_for('catalogo.mostrar_catalogo'))
# ================================================================
# E5 - EDITAR LIBRO
# ================================================================

@catalogo_bp.route('/editar/<isbn>', methods=['GET'])
@requiere_sesion
def mostrar_editar(isbn):
    """
    T10 - Clic en "Editar" desde E2 -> E5.
    Presenta el formulario con la informacion del libro a editar.
    El campo ISBN se muestra pero no se puede modificar (es la PK).
    """
    libro = LibroModel.buscar_por_isbn(isbn)

    if not libro:
        return redirect(url_for('catalogo.mostrar_catalogo'))

    # Mapear nombres de columnas a nombres de campos del formulario
    datos = {
        'isbn':            libro['ISBN'],
        'titulo':          libro['Titulo'],
        'autor':           libro['Autor'],
        'editorial':       libro['Editorial'],
        'sinopsis':        libro['Sinopsis'],
        'ano_publicacion': libro['AnoPublicacion'],
        'numero_paginas':  libro['NumeroPaginas'],
        'precio':          libro['Precio'],
        'ubicacion':       libro['Ubicacion'],
        'numero_copias':   libro['NumeroCopias'],
        'categoria':       libro['Categoria']
    }

    return render_template('catalogo/editar.html',
                           error=None, datos=datos, campos_error=None)


@catalogo_bp.route('/editar/<isbn>', methods=['POST'])
@requiere_sesion
def procesar_editar(isbn):
    """
    Procesa la edicion de un libro existente.
    Implementa T17 (datos requeridos) y T18 (cambio exitoso).
    El ISBN no se modifica.
    """
    # Recopilar datos del formulario (sin ISBN, ya que no se modifica)
    datos = {
        'isbn':            isbn,  # se conserva el original
        'titulo':          request.form.get('titulo', '').strip(),
        'autor':           request.form.get('autor', '').strip(),
        'editorial':       request.form.get('editorial', '').strip(),
        'sinopsis':        request.form.get('sinopsis', '').strip(),
        'ano_publicacion': request.form.get('ano_publicacion', '').strip(),
        'numero_paginas':  request.form.get('numero_paginas', '').strip(),
        'precio':          request.form.get('precio', '').strip(),
        'ubicacion':       request.form.get('ubicacion', '').strip(),
        'numero_copias':   request.form.get('numero_copias', '').strip(),
        'categoria':       request.form.get('categoria', '').strip()
    }

    # --- T17: Cambio invalido (datos requeridos) ---
    campos_requeridos = ['titulo', 'autor', 'editorial', 'sinopsis',
                         'ano_publicacion', 'numero_paginas', 'precio',
                         'ubicacion', 'numero_copias', 'categoria']
    campos_vacios = [c for c in campos_requeridos if not datos[c]]

    if campos_vacios:
        return render_template(
            'catalogo/editar.html',
            error='Datos requeridos. Por favor completa todos los campos.',
            datos=datos,
            campos_error=campos_vacios
        )

    # Conversion de tipos numericos
    try:
        datos['ano_publicacion'] = int(datos['ano_publicacion'])
        datos['numero_paginas']  = int(datos['numero_paginas'])
        datos['numero_copias']   = int(datos['numero_copias'])
        datos['precio']          = float(datos['precio'])
    except ValueError:
        return render_template(
            'catalogo/editar.html',
            error='Datos invalidos. Verifica los campos numericos.',
            datos=datos,
            campos_error=['ano_publicacion', 'numero_paginas',
                          'numero_copias', 'precio']
        )

    # --- T18: Cambio exitoso -> regresar a E2 ---
    LibroModel.actualizar(isbn, datos)
    return redirect(url_for('catalogo.mostrar_catalogo'))
# ================================================================
# E6 - ELIMINAR LIBRO (modal de confirmacion)
# ================================================================

@catalogo_bp.route('/eliminar/<isbn>', methods=['GET'])
@requiere_sesion
def mostrar_eliminar(isbn):
    """
    T11 - Clic en "Eliminar" desde E2 -> E6.
    Presenta el modal de confirmacion con el nombre del libro.
    """
    libro = LibroModel.buscar_por_isbn(isbn)

    if not libro:
        return redirect(url_for('catalogo.mostrar_catalogo'))

    return render_template('catalogo/eliminar.html', libro=libro)


@catalogo_bp.route('/eliminar/<isbn>', methods=['POST'])
@requiere_sesion
def procesar_eliminar(isbn):
    """
    T21 - Baja exitosa (usuario confirmo "Eliminar") -> regresar a E2.
    Elimina el libro de la tabla Libros y regresa al catalogo.

    Nota: T22 (Cancelar eliminacion) se maneja con un enlace en la vista
    que regresa al catalogo sin tocar la BD.
    """
    libro = LibroModel.buscar_por_isbn(isbn)

    if libro:
        LibroModel.eliminar(isbn)

    return redirect(url_for('catalogo.mostrar_catalogo'))
