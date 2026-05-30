# Sistema Académico - Gestión de Estudiantes y Profesores

-- Sistema en Python para la gestión integral de estudiantes y profesores mediante una interfaz de consola (CLI).

-- Características

* Gestión de estudiantes
* Gestión de profesores
* Estadísticas generales
* Persistencia de datos en archivos JSON
* Arquitectura modular y escalable

# Estructura del Proyecto

```
src/
├── main.py              # Punto de entrada
├── models/              # Entidades del dominio (Student, Teacher)
├── services/            # Lógica de negocio
├── storage/             # Persistencia (JSON)
├── ui/                  # Interfaces de usuario (menús CLI)
└── data/                # Archivos de datos
```

# Instalación

1. Clona el repositorio:

```
git clone <tu-repositorio>
cd Maestro-edu
```

2. (Opcional) Crear entorno virtual:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

# Uso

Ejecuta el sistema con:

```
python -m src.main
```

# Arquitectura

El proyecto sigue una separación por capas:

* Models → Representan las entidades del sistema
* Services → Contienen la lógica de negocio
* Storage → Manejo de persistencia (JSON)
* ui → Interfaz de usuario basada en consola

# Funcionalidades principales

# Estudiantes

* Crear, listar, actualizar y eliminar estudiantes
* Gestión de información académica

# Profesores

* Registro y administración de profesores
* Organización de datos docentes

# Sistema

* Menú interactivo
* Estadísticas generales
* Persistencia automática

# Tecnologías

* Python 3.x
* JSON (para almacenamiento)

## 👨‍💻 Autor

Proyecto académico


