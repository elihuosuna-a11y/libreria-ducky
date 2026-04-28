"""
models/libro_model.py
MODELO - Encapsula el acceso a la tabla Libros.

Para la Evidencia 10 unicamente se implementan los metodos necesarios
para el modulo de Catalogo: consulta, filtrado y paginacion.
Los metodos de alta, edicion y eliminacion se desarrollaran en el Proyecto Final.
"""

from models.database import get_connection


class LibroModel:

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