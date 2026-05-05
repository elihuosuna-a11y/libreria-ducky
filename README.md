# Librería de la Universidad Ducky

Sistema de gestión de biblioteca desarrollado como **Evidencia 10** de la materia **Arquitectura de Software**.

Este proyecto implementa los módulos de **Autenticación** y **Catálogo de Libros** del sistema, siguiendo el patrón arquitectónico **Modelo-Vista-Controlador (MVC)** y respetando el comportamiento definido en el Diagrama Estado-Transición de la Evidencia 9.

---

## 📋 Tecnologías utilizadas

- **Lenguaje:** Python 3.11
- **Framework web:** Flask 3.0.3
- **Base de datos:** SQLite
- **Frontend:** HTML5 + Bootstrap 5 + Jinja2
- **Seguridad:** bcrypt (hash de contraseñas)

---

## 🏗️ Arquitectura MVC

```
libreria_ducky/
├── models/                    # MODELO — Acceso a la base de datos
│   ├── database.py
│   ├── usuario_model.py
│   └── libro_model.py
│
├── controllers/               # CONTROLADOR — Lógica y flujo
│   ├── auth_controller.py
│   └── catalogo_controller.py
│
├── templates/                 # VISTA — Interfaz de usuario
│   ├── auth/login.html
│   ├── catalogo/index.html
│   └── partials/
│
├── static/css/                # Recursos estáticos
├── app.py                     # Punto de entrada
├── init_db.py                 # Inicializa la base de datos
└── requirements.txt           # Dependencias
```

---

## 🎯 Estados y transiciones implementados

| Estado | Pantalla | Transiciones |
|---|---|---|
| **E1** | Autenticación | T01, T02, T03, T04, T05 |
| **E2** | Catálogo de Libros | T06, T07, T19 |

Los estados **E3 a E6** (Nuevo Libro, Detalles, Editar y Eliminar) se desarrollarán como parte del **Proyecto Final**.

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio
```
git clone https://github.com/elihuosuna-a11y/libreria-ducky.git
cd libreria-ducky
```

### 2. Instalar dependencias
```
pip install -r requirements.txt
```

### 3. Inicializar la base de datos
```
python init_db.py
```

### 4. Ejecutar el servidor
```
python app.py
```

### 5. Abrir en el navegador
```
http://localhost:5000
```

---

## 🔐 Credenciales de prueba

| Campo | Valor |
|---|---|
| Usuario | `A01234567` |
| Contraseña | `admin123` |

---

## 👤 Autor

**Elihu Osuna** — Estudiante de 6° Semestre, Universidad Ducky

Materia: Arquitectura de Software
