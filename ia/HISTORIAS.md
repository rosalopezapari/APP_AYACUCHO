# Historias de Usuario - Qory Ayacucho

---

# HISTORIA 1: Registro de Ciudadano
COMO usuario nuevo,
QUIERO registrarme con mis datos personales,
PARA acceder a la aplicación y planificar mis viajes
// El sistema debe permitir el registro de ciudadanos con nombre, email, teléfono y contraseña. Los datos se guardarán en SQLite mediante Reflex ORM.

TAREAS
[x] Crear modelo Ciudadano en `src/models/ciudadano.py`
[x] Crear formulario de registro con Tkinter
[x] Validar campos (email, teléfono, contraseña)
[x] Guardar registro en base de datos
[x] Mostrar mensaje de éxito/error
ESTADO: COMPLETADA

---

# HISTORIA 2: Inicio de Sesión
COMO usuario registrado,
QUIERO iniciar sesión con mi email y contraseña,
PARA acceder a mi cuenta de forma segura

TAREAS
[x] Pantalla de inicio con opciones: Iniciar Sesión / Registrarse / Salir
[x] Crear formulario de inicio de sesión con validación de campos
[x] Validar credenciales contra la BD
[x] Redirigir al menú principal tras login exitoso
[x] Mostrar error si las credenciales son incorrectas
[x] Navegación fluida entre inicio → login ↔ registro
[x] Volver a pantalla anterior desde login o registro
ESTADO: COMPLETADA

---

# HISTORIA 3: Gestión de Presupuesto
COMO usuario,
QUIERO ingresar mi presupuesto y días de viaje,
PARA que la app me calcule un plan diario de gastos

TAREAS
[x] Crear modelo Presupuesto en `src/models/presupuesto.py`
[x] Crear formulario de ingreso de presupuesto
[x] Calcular gasto diario sugerido con desglose (40% aloj, 30% comida, 20% transp, 10% extras)
[x] Mostrar resumen del presupuesto
ESTADO: COMPLETADA

---

# HISTORIA 4: Recomendaciones de Viaje
COMO usuario,
QUIERO recibir recomendaciones de hospedaje, comida y turismo según mi presupuesto,
PARA planificar mi viaje de forma económica

TAREAS
[x] Crear tabla destino con 27 lugares turísticos seed
[x] Implementar lógica de recomendación según presupuesto diario
[x] Mostrar lista de lugares recomendados en tabla
[x] Filtrar por provincia (11 provincias)
ESTADO: COMPLETADA

---

# HISTORIA 5: Historial de Actividades
COMO usuario,
QUIERO ver un historial de mis viajes, presupuestos y actividades,
PARA llevar un registro de todo lo que he hecho en la app

TAREAS
[x] Crear modelo Historial en `src/models/historial.py`
[x] Registrar acciones: Registro, Inicio de Sesión, Presupuesto, Recomendación
[x] Mostrar historial ordenado por fecha descendente
[x] Permitir filtrar por tipo de actividad
ESTADO: COMPLETADA

---

# HISTORIA 6: CRUD de Restaurantes
COMO usuario,
QUIERO gestionar restaurantes (agregar, editar, eliminar, listar),
PARA tener información actualizada de dónde comer según mi presupuesto

TAREAS
[x] Crear tabla restaurante con 14 restaurantes seed
[x] Crear modelo Restaurante en `src/models/restaurante.py`
[x] Listar restaurantes con filtro por provincia y tipo de comida
[x] Agregar nuevo restaurante
[x] Editar restaurante existente
[x] Eliminar restaurante
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 7: CRUD de Tiendas y Artesanías
COMO usuario,
QUIERO gestionar tiendas y artesanías (agregar, editar, eliminar, listar),
PARA encontrar lugares donde comprar souvenirs y productos típicos

TAREAS
[x] Crear tabla tienda con 14 tiendas seed
[x] Crear modelo Tienda en `src/models/tienda.py`
[x] Listar tiendas con filtro por provincia y tipo
[x] Agregar nueva tienda
[x] Editar tienda existente
[x] Eliminar tienda
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 8: Sistema de Ahorro
COMO usuario,
QUIERO crear metas de ahorro y registrar mis aportes,
PARA planificar financieramente mis viajes a Ayacucho

TAREAS
[x] Crear tabla ahorro en la base de datos
[x] Crear modelo Ahorro en `src/models/ahorro.py`
[x] Crear nueva meta con monto objetivo y fecha límite
[x] Aportar dinero a una meta y ver progreso
[x] Visualizar progreso con barra de progreso y porcentaje
[x] Editar meta existente
[x] Eliminar meta
[x] Filtrar por estado (En progreso, Completada)
[x] Marcar automáticamente como Completada al alcanzar meta
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 9: CRUD de Transporte
COMO usuario,
QUIERO gestionar opciones de transporte (agregar, editar, eliminar, listar),
PARA planificar cómo llegar a los destinos turísticos

TAREAS
[x] Crear tabla transporte con 14 registros seed
[x] Crear modelo Transporte en `src/models/transporte.py`
[x] Listar transportes con filtro por tipo (Bus, Avión, Taxi, Colectivo)
[x] Agregar nuevo transporte
[x] Editar transporte existente
[x] Eliminar transporte
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 10: CRUD de Hospedajes
COMO usuario,
QUIERO gestionar opciones de hospedaje (agregar, editar, eliminar, listar),
PARA encontrar dónde alojarme durante mi viaje

TAREAS
[x] Crear tabla hospedaje con 14 registros seed
[x] Crear modelo Hospedaje en `src/models/hospedaje.py`
[x] Listar hospedajes con filtro por provincia y tipo
[x] Agregar nuevo hospedaje
[x] Editar hospedaje existente
[x] Eliminar hospedaje
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 11: CRUD de Destinos Turísticos
COMO usuario,
QUIERO gestionar destinos turísticos (agregar, editar, eliminar, listar),
PARA mantener actualizada la información de los lugares a visitar

TAREAS
[x] Crear modelo Destino en `src/models/destino.py`
[x] Listar destinos con filtro por provincia y categoría
[x] Agregar nuevo destino
[x] Editar destino existente
[x] Eliminar destino
[x] Conectar desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 12: Planificador de Viaje Integrado
COMO usuario,
QUIERO seleccionar destino, restaurante, transporte y hospedaje reales al planificar mi presupuesto,
PARA conocer el costo real estimado de mi viaje y ver si se ajusta a mi presupuesto

TAREAS
[x] Rediseñar modelo Presupuesto con cálculo integrado desde datos reales
[x] Agregar comboboxes para seleccionar destino, restaurante, transporte y hospedaje
[x] Calcular costo real total basado en las selecciones (comida × días, alojamiento × noches, etc.)
[x] Mostrar comparación presupuesto vs costo real con indicador visual
[x] Mostrar desglose detallado por categoría
[x] Mantener funcionalidad de guardado de presupuesto existente
[x] Agregar botón Limpiar para reiniciar el formulario
[x] Vincular desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 13: Editar Perfil de Ciudadano
COMO usuario registrado,
QUIERO editar mis datos personales (nombre, email, teléfono, contraseña),
PARA mantener mi información actualizada sin necesidad de crear una nueva cuenta

TAREAS
[x] Agregar método actualizar al modelo Ciudadano
[x] Crear formulario de edición precargado con datos actuales
[x] Validar campos (email, teléfono, contraseña con confirmación)
[x] Actualizar en base de datos con manejo de errores (email duplicado)
[x] Refrescar cabecera del menú principal tras la edición
[x] Registrar cambio en historial
[x] Permitir cambio opcional de contraseña
[x] Vincular desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 14: Exportar Datos
COMO usuario registrado,
QUIERO exportar mi historial, presupuestos y metas de ahorro a CSV o TXT,
PARA tener un respaldo de mi información y analizarla externamente

TAREAS
[x] Crear modelo Exportador con métodos de exportación CSV y TXT
[x] Exportar historial a CSV con columnas Fecha, Tipo, Descripción
[x] Exportar presupuestos a CSV con columnas Fecha, Total, Días, Destino
[x] Exportar metas de ahorro a CSV con columnas Meta, Objetivo, Ahorrado, Progreso, Estado
[x] Exportar reporte completo a TXT con todos los datos formateados
[x] Crear ventana de exportación con selección de datos y formato
[x] Usar cuadro de diálogo Guardar Como para elegir ubicación
[x] Registrar exportación en el historial
[x] Vincular desde el menú principal
ESTADO: COMPLETADA

---

# HISTORIA 15: Reportes y Estadísticas
COMO usuario registrado,
QUIERO ver reportes y estadísticas de mi actividad en la app,
PARA tener una visión general de mis viajes, gastos y ahorros

TAREAS
[x] Crear ventana con pestañas (Notebook) para cada tipo de reporte
[x] Pestaña Resumen General: métricas globales del ciudadano
[x] Pestaña Presupuestos: promedio, totales y gráfico de barras en Canvas
[x] Pestaña Actividades: conteo por tipo con barras horizontales en Canvas
[x] Pestaña Ahorro: progreso global y barras por meta
[x] Mostrar gráficos de barras con tk.Canvas (sin dependencias externas)
[x] Vincular desde el menú principal
ESTADO: COMPLETADA
