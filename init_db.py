"""
init_db.py
Crea las tablas Usuarios y Libros e inserta datos de prueba.
Ejecutar una sola vez:  python init_db.py
"""

import bcrypt
from models.database import get_connection

print('Inicializando base de datos...')

conn = get_connection()
cursor = conn.cursor()

# ----- Tabla Usuarios -----
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        Usuario     VARCHAR(50)  PRIMARY KEY,
        Contrasena  VARCHAR(255) NOT NULL,
        Nombre      VARCHAR(50)  UNIQUE NOT NULL,
        Email       VARCHAR(150) UNIQUE NOT NULL
    )
""")

# ----- Tabla Libros -----
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Libros (
        ISBN            VARCHAR(20)  PRIMARY KEY,
        Titulo          VARCHAR(255) NOT NULL,
        Autor           VARCHAR(255) NOT NULL,
        Editorial       VARCHAR(150),
        Sinopsis        TEXT,
        AnoPublicacion  INTEGER,
        NumeroPaginas   INTEGER,
        Precio          DECIMAL(10,2),
        Ubicacion       VARCHAR(100),
        NumeroCopias    INTEGER DEFAULT 1,
        Categoria       VARCHAR(100),
        FechaRegistro   DATETIME DEFAULT CURRENT_TIMESTAMP,
        Estado          TEXT CHECK(Estado IN ('disponible','prestado','mantenimiento','perdido'))
                        DEFAULT 'disponible'
    )
""")

# Indices para busqueda rapida (usados en T06)
cursor.execute('CREATE INDEX IF NOT EXISTS idx_titulo ON Libros(Titulo)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_autor  ON Libros(Autor)')

# ----- Datos de prueba -----

# Usuario admin con contrasena cifrada
password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())

cursor.execute("""
    INSERT OR IGNORE INTO Usuarios (Usuario, Contrasena, Nombre, Email)
    VALUES (?, ?, ?, ?)
""", ('A01234567', password_hash.decode('utf-8'),
      'Administrador Ducky', 'admin@ducky.edu'))

# Libros de ejemplo
libros_ejemplo = [
    ('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott',
     'Clasico sobre justicia racial en el sur de Estados Unidos.',
     1960, 281, 350.00, 'Seccion: Literatura - Pasillo 3A', 2, 'Ficcion'),
    ('978-84-16408-23-9', 'El Eco de los Relojes de Arena', 'Elena Villarreal Solis',
     'Nexo Arcano Editores',
     'En un pueblo donde el tiempo no transcurre de forma lineal, Julian descubre que sus recuerdos pertenecen a un hombre que aun no ha nacido.',
     2024, 342, 400.00, 'Seccion: Narrativa Hispanoamericana - Pasillo 12-B', 4, 'Ciencia Ficcion'),
    ('978-0-452-28423-4', '1984', 'George Orwell', 'Secker & Warburg',
     'Distopia sobre vigilancia estatal y manipulacion de la verdad.',
     1949, 328, 320.00, 'Seccion: Literatura - Pasillo 3B', 3, 'Ficcion'),
    ('978-84-376-0494-7', 'Cien anos de soledad', 'Gabriel Garcia Marquez',
     'Editorial Sudamericana',
     'La saga de la familia Buendia en Macondo a lo largo de varias generaciones.',
     1967, 471, 380.00, 'Seccion: Literatura Hispanoamericana - Pasillo 5A', 5, 'Ficcion'),
    ('978-0-7432-7356-5', 'The Great Gatsby', 'F. Scott Fitzgerald',
     'Charles Scribner Sons',
     'Retrato de la era del jazz y el sueno americano.',
     1925, 180, 290.00, 'Seccion: Literatura - Pasillo 3C', 2, 'Ficcion'),
    ('978-84-08-04364-5', 'La sombra del viento', 'Carlos Ruiz Zafon',
     'Editorial Planeta',
     'Un joven descubre un misterioso libro en el Cementerio de los Libros Olvidados.',
     2001, 565, 420.00, 'Seccion: Misterio - Pasillo 8B', 3, 'Misterio'),
]

cursor.executemany("""
    INSERT OR IGNORE INTO Libros
        (ISBN, Titulo, Autor, Editorial, Sinopsis, AnoPublicacion,
         NumeroPaginas, Precio, Ubicacion, NumeroCopias, Categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", libros_ejemplo)

conn.commit()
conn.close()

print('Base de datos inicializada correctamente.')
print('Usuario de prueba:  A01234567')
print('Contrasena:         admin123')