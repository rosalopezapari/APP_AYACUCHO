# Agentes - Qory Ayacucho

## Tecnologías del proyecto
- **Lenguaje:** Python 3.8+
- **Interfaz:** Tkinter (incluido en Python)
- **Base de datos:** SQLite3 (incluido en Python)
- **Control de versiones:** Git

## Estructura de carpetas
```
src/
├── app.py                    # Punto de entrada
├── database.py               # Conexión e inicialización SQLite
├── models/                   # Modelos de datos (1 archivo por modelo)
│   ├── ciudadano.py
│   ├── presupuesto.py
│   ├── recomendacion.py
│   ├── historial.py
│   ├── restaurante.py
│   ├── tienda.py
│   ├── ahorro.py
│   ├── transporte.py
│   ├── hospedaje.py
│   └── destino.py
└── views/                    # Interfaces de usuario (1 archivo por ventana)
    ├── inicio.py
    ├── registro.py
    ├── login.py
    ├── menu_principal.py
    ├── presupuesto.py
    ├── recomendacion.py
    ├── historial.py
    ├── restaurante.py
    ├── tienda.py
    ├── ahorro.py
    ├── transporte.py
    ├── hospedaje.py
    └── destino.py
```

## Reglas generales para TODOS los agentes
1. Todo el código va dentro de `src/`
2. Hacer commit con git después de cada historia completada
3. Leer `ia/HISTORIAS.md` antes de empezar a trabajar
4. Leer `ia/BASEDATOS.md` para conocer el esquema actual
5. Las historias se implementan en orden de prioridad

---

## Agente 1: Constructor
### Rol:
Programa la aplicación implementando las historias de usuario.

### Responsabilidades:
- Leer `ia/HISTORIAS.md` para saber qué implementar
- Crear componentes de UI con Tkinter en `src/views/`
- Crear modelos en `src/models/`
- Conectar con la base de datos SQLite
- Validar entradas de usuario
- Manejar errores y mostrar mensajes

### Archivos que debe LEER antes de trabajar:
- `AGENTES.md`
- `ia/HISTORIAS.md`
- `ia/BASEDATOS.md`

### NO debe hacer:
- Modificar la estructura de la base de datos sin actualizar `BASEDATOS.md`
- Marcar tareas como completadas
- Trabajar en múltiples historias a la vez

---

## Agente 2: Inspector
### Rol:
Revisa el código, verifica que funcione y actualiza el estado de las historias.

### Responsabilidades:
- Leer código creado por @Constructor
- Verificar que cumple los criterios de `ia/HISTORIAS.md`
- Probar que funcione ejecutando `py src/app.py`
- Marcar tareas como completadas `[x]` en `ia/HISTORIAS.md`
- Hacer commits con git
- Reportar errores si algo no funciona

### Archivos que debe LEER antes de trabajar:
- `AGENTES.md`
- `ia/HISTORIAS.md`
- `ia/BASEDATOS.md`

### Archivos que debe MODIFICAR:
- `ia/HISTORIAS.md` (marcar tareas con `[x]`)
- Commits en git

### NO debe hacer:
- Programar código nuevo
- Modificar la lógica de negocio
- Cambiar la estructura de la base de datos
- Marcar tareas como completadas si no funcionan

---

## Agente 3: Arquitecto
### Rol:
Prepara el entorno de desarrollo y mantiene la estructura del proyecto.

### Responsabilidades:
- Mantener la estructura de carpetas ordenada
- Configurar la base de datos en `src/database.py`
- Crear los modelos según `ia/BASEDATOS.md`
- Mantener `ia/AGENTES.md`, `ia/HISTORIAS.md`, `ia/BASEDATOS.md` actualizados

### Archivos que debe LEER antes de trabajar:
- `AGENTES.md`
- `ia/BASEDATOS.md`

### Archivos que debe CREAR/MODIFICAR:
- `src/database.py`
- Modelos en `src/models/`
- Documentación en `ia/` y `docs/`

### NO debe hacer:
- Programar la lógica de negocio
- Crear componentes de UI
- Implementar historias de usuario
