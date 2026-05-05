"""
models/libro_model.py
MODELO - Encapsula el acceso a la tabla Libros.

Para el Proyecto Final se implementan todos los metodos CRUD necesarios
para los estados E2 (Catalogo), E3 (Nuevo Libro), E4 (Detalles),
E5 (Editar Libro) y E6 (Eliminar Libro).
"""

from models.database import get_connection


class LibroModel:

    # ============================================================
    # CONSULTA Y FILTRADO  (usado en E2 - T06, T07)
    # ============================================================

    @staticmethod
    def listar(filtro='', campo='todos', pagina=1, por_pagina=5):
        """
        Obtiene una lista paginada y filtrada de libros.
        Soporta T06 (filtro por Titulo / Autor / ISBN) y T07 (paginacion).

        Retorna un dict con:
          - libros:        lista de registros
          - total:         total de coincidencias
          - total_paginas: numero total de paginas
        """
        offset = (pagina - 1) * por_pagina

        # Construccion dinamica del WHERE segun el campo seleccionado
        where = ''
        parametros = []

        if filtro and filtro.strip() != '':
            valor = f'%{filtro.strip()}%'
            if campo == 'titulo':
                where = 'WHERE Titulo LIKE ?'
                parametros = [valor]
            elif campo == 'autor':
                where = 'WHERE Autor LIKE ?'
                parametros = [valor]
            elif campo == 'isbn':
                where = 'WHERE ISBN LIKE ?'
                parametros = [valor]
            else:  # 'todos'
                where = 'WHERE Titulo LIKE ? OR Autor LIKE ? OR ISBN LIKE ?'
                parametros = [valor, valor, valor]

        conn = get_connection()
        cursor = conn.cursor()

        # Conteo total para calcular el numero de paginas
        cursor.execute(f'SELECT COUNT(*) AS n FROM Libros {where}', parametros)
        total = cursor.fetchone()['n']

        # Consulta paginada
        cursor.execute(f"""
            SELECT ISBN, Titulo, Autor, Categoria, NumeroCopias
            FROM Libros
            {where}
            ORDER BY Titulo
            LIMIT ? OFFSET ?
        """, parametros + [por_pagina, offset])

        libros = [dict(row) for row in cursor.fetchall()]
        conn.close()

        total_paginas = max(1, (total + por_pagina - 1) // por_pagina)

        return {
            'libros': libros,
            'total': total,
            'total_paginas': total_paginas
        }

    # ============================================================
    # BUSQUEDA POR ISBN  (usado en E4, E5, E6)
    # ============================================================

    @staticmethod
    def buscar_por_isbn(isbn):
        """
        Busca un libro especifico por su ISBN.
        Retorna un dict con todos los campos del libro o None si no existe.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Libros WHERE ISBN = ?', (isbn,))
        registro = cursor.fetchone()
        conn.close()
        return dict(registro) if registro else None

    @staticmethod
    def isbn_existe(isbn):
        """
        Verifica si un ISBN ya existe en la tabla Libros.
        Usado en E3 para validar duplicados (T12).
        """
        return LibroModel.buscar_por_isbn(isbn) is not None

    # ============================================================
    # ALTA  (usado en E3 - T14)
    # ============================================================

    @staticmethod
    def crear(datos):
        """
        Inserta un nuevo libro en la tabla Libros.
        Recibe un dict con todos los campos del libro.
        Retorna True si se creo correctamente.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Libros
                (ISBN, Titulo, Autor, Editorial, Sinopsis, AnoPublicacion,
                 NumeroPaginas, Precio, Ubicacion, NumeroCopias, Categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos['isbn'],
            datos['titulo'],
            datos['autor'],
            datos['editorial'],
            datos['sinopsis'],
            datos['ano_publicacion'],
            datos['numero_paginas'],
            datos['precio'],
            datos['ubicacion'],
            datos['numero_copias'],
            datos['categoria']
        ))
        conn.commit()
        conn.close()
        return True

    # ============================================================
    # CAMBIO  (usado en E5 - T18)
    # ============================================================

    @staticmethod
    def actualizar(isbn, datos):
        """
        Actualiza los datos de un libro existente.
        El ISBN no se modifica (es la PK).
        Retorna True si se actualizo correctamente.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Libros
            SET Titulo = ?, Autor = ?, Editorial = ?, Sinopsis = ?,
                AnoPublicacion = ?, NumeroPaginas = ?, Precio = ?,
                Ubicacion = ?, NumeroCopias = ?, Categoria = ?
            WHERE ISBN = ?
        """, (
            datos['titulo'],
            datos['autor'],
            datos['editorial'],
            datos['sinopsis'],
            datos['ano_publicacion'],
            datos['numero_paginas'],
            datos['precio'],
            datos['ubicacion'],
            datos['numero_copias'],
            datos['categoria'],
            isbn
        ))
        conn.commit()
        conn.close()
        return True

    # ============================================================
    # BAJA  (usado en E6 - T21)
    # ============================================================

    @staticmethod
    def eliminar(isbn):
        """
        Elimina un libro de la tabla Libros por su ISBN.
        Retorna True si se elimino correctamente.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Libros WHERE ISBN = ?', (isbn,))
        conn.commit()
        conn.close()
        return True