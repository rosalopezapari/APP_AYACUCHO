# Base de Datos - Qory Ayacucho

## Importante
- Los modelos van en `src/models/`
- Cada modelo en su propio archivo
- Se usa SQLite3 con Python estándar (módulo `sqlite3`)
- La conexión se maneja desde `src/database.py`

## Tablas Implementadas

### TABLA: CIUDADANO

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_ciudadano | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| nombre | TEXT | NOT NULL | Nombre completo del ciudadano |
| email | TEXT | NOT NULL UNIQUE | Correo electrónico |
| telefono | TEXT | NOT NULL | Número de teléfono |
| contrasena | TEXT | NOT NULL | Contraseña de acceso |
| fecha_registro | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS ciudadano (
    id_ciudadano INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL,
    contrasena TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### TABLA: PRESUPUESTO

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_presupuesto | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| id_ciudadano | INTEGER | NOT NULL FK → ciudadano | Ciudadano asociado |
| total | REAL | NOT NULL | Presupuesto total en soles |
| dias | INTEGER | NOT NULL | Días de viaje |
| destino_principal | TEXT | | Destino principal del viaje |
| fecha_viaje | TEXT | | Fecha del viaje |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS presupuesto (
    id_presupuesto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ciudadano INTEGER NOT NULL,
    total REAL NOT NULL,
    dias INTEGER NOT NULL,
    destino_principal TEXT,
    fecha_viaje TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
);
```

### TABLA: DESTINO

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_destino | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| provincia | TEXT | NOT NULL | Provincia de Ayacucho |
| categoria | TEXT | NOT NULL | Cultural, Natural, Gastronómico, Aventura, Compras |
| nombre | TEXT | NOT NULL | Nombre del lugar turístico |
| precio | REAL | NOT NULL | Precio de entrada/actividad |
| descripcion | TEXT | | Descripción del lugar |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS destino (
    id_destino INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT NOT NULL,
    categoria TEXT NOT NULL,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    descripcion TEXT
);
```

**Datos semilla:** 27 lugares turísticos precargados en las 11 provincias de Ayacucho.

### TABLA: HISTORIAL

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_historial | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| id_ciudadano | INTEGER | NOT NULL FK → ciudadano | Ciudadano asociado |
| tipo_actividad | TEXT | NOT NULL | Tipo: Registro, Inicio de Sesión, Presupuesto, Recomendación |
| descripcion | TEXT | NOT NULL | Detalle de la actividad |
| fecha | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha y hora del registro |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS historial (
    id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ciudadano INTEGER NOT NULL,
    tipo_actividad TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
);
```

### TABLA: RESTAURANTE

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_restaurante | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| provincia | TEXT | NOT NULL | Provincia de Ayacucho |
| tipo_comida | TEXT | NOT NULL | Tipo de comida (Tradicional, Criolla, Parrilla, etc.) |
| nombre | TEXT | NOT NULL | Nombre del restaurante |
| precio_min | REAL | NOT NULL | Precio mínimo por persona |
| precio_max | REAL | NOT NULL | Precio máximo por persona |
| especialidad | TEXT | | Plato o especialidad destacada |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS restaurante (
    id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT NOT NULL,
    tipo_comida TEXT NOT NULL,
    nombre TEXT NOT NULL,
    precio_min REAL NOT NULL,
    precio_max REAL NOT NULL,
    especialidad TEXT
);
```

**Datos semilla:** 14 restaurantes precargados en 6 provincias (Huamanga, Huanta, Vilcashuamán, Cangallo, Parinacochas, Lucanas) con 5 tipos de comida.

---

### TABLA: TIENDA

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_tienda | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| provincia | TEXT | NOT NULL | Provincia de Ayacucho |
| tipo | TEXT | NOT NULL | Tipo (Artesanía, Textiles, Cerámica, Retablos, etc.) |
| nombre | TEXT | NOT NULL | Nombre de la tienda o taller |
| precio_min | REAL | NOT NULL | Precio mínimo del producto |
| precio_max | REAL | NOT NULL | Precio máximo del producto |
| especialidad | TEXT | | Producto o especialidad destacada |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS tienda (
    id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT NOT NULL,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    precio_min REAL NOT NULL,
    precio_max REAL NOT NULL,
    especialidad TEXT
);
```

**Datos semilla:** 14 tiendas precargadas en 7 provincias con 7 tipos (Artesanía, Retablos, Piedra de Huamanga, Textiles, Cerámica, Ropa, Instrumentos).

---

### TABLA: AHORRO

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_ahorro | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| id_ciudadano | INTEGER | NOT NULL FK → ciudadano | Ciudadano asociado |
| meta | TEXT | NOT NULL | Nombre de la meta (ej: "Viaje a Wari") |
| monto_objetivo | REAL | NOT NULL | Monto total a alcanzar |
| monto_actual | REAL | NOT NULL DEFAULT 0 | Monto ahorrado hasta ahora |
| fecha_inicio | TEXT | NOT NULL | Fecha de creación de la meta |
| fecha_limite | TEXT | | Fecha objetivo para completar |
| estado | TEXT | NOT NULL DEFAULT 'En progreso' | En progreso, Completada, Cancelada |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS ahorro (
    id_ahorro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ciudadano INTEGER NOT NULL,
    meta TEXT NOT NULL,
    monto_objetivo REAL NOT NULL,
    monto_actual REAL NOT NULL DEFAULT 0,
    fecha_inicio TEXT NOT NULL,
    fecha_limite TEXT,
    estado TEXT NOT NULL DEFAULT 'En progreso',
    FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
);
```

**Nota:** Sin datos semilla (cada ciudadano crea sus propias metas).

---

### TABLA: TRANSPORTE

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_transporte | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| tipo | TEXT | NOT NULL | Tipo (Bus, Avión, Taxi, Colectivo) |
| empresa | TEXT | NOT NULL | Empresa transportista |
| nombre | TEXT | NOT NULL | Nombre del servicio o ruta |
| origen | TEXT | NOT NULL | Ciudad o lugar de origen |
| destino | TEXT | NOT NULL | Ciudad o lugar de destino |
| precio | REAL | NOT NULL | Precio del pasaje |
| duracion | TEXT | | Duración estimada del viaje |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS transporte (
    id_transporte INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    empresa TEXT NOT NULL,
    nombre TEXT NOT NULL,
    origen TEXT NOT NULL,
    destino TEXT NOT NULL,
    precio REAL NOT NULL,
    duracion TEXT
);
```

**Datos semilla:** 14 transportes precargados: 4 tipos (Bus, Avión, Colectivo, Taxi) conectando Lima, Ayacucho y provincias.

---

### TABLA: HOSPEDAJE

| Campo | Tipo de Dato | Restricción | Descripción |
|-------|-------------|-------------|-------------|
| id_hospedaje | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único |
| provincia | TEXT | NOT NULL | Provincia de Ayacucho |
| tipo | TEXT | NOT NULL | Tipo (Hotel, Hostal, Hospedaje, Lodge) |
| nombre | TEXT | NOT NULL | Nombre del hospedaje |
| precio_min | REAL | NOT NULL | Precio mínimo por noche |
| precio_max | REAL | NOT NULL | Precio máximo por noche |
| servicios | TEXT | | Servicios ofrecidos (WiFi, Desayuno, etc.) |
| telefono | TEXT | | Teléfono de contacto |

**SQL de creación:**
```sql
CREATE TABLE IF NOT EXISTS hospedaje (
    id_hospedaje INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT NOT NULL,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    precio_min REAL NOT NULL,
    precio_max REAL NOT NULL,
    servicios TEXT,
    telefono TEXT
);
```

**Datos semilla:** 14 hospedajes precargados en 7 provincias con 4 tipos (Hotel, Hostal, Hospedaje, Lodge).

---

## Tablas Planificadas

(No hay tablas planificadas — todas las funcionalidades actuales están implementadas.)

## Notas de Integración

### Módulo Presupuesto (H12)
El modelo `Presupuesto` ahora incluye `calcular_integrado()` que obtiene datos reales desde las tablas `destino`, `restaurante`, `transporte` y `hospedaje` para calcular el costo estimado del viaje. No requiere cambios en el esquema de la base de datos; la integración es una capa de cálculo sobre los datos existentes.
