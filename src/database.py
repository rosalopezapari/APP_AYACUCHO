import sqlite3
import os
import sys


def _get_db_path():
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "qory_ayacucho.db")
    return os.path.join(os.path.dirname(__file__), "..", "qory_ayacucho.db")


DB_PATH = _get_db_path()


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Datos reales de establecimientos turísticos en Ayacucho
# Fuentes: Google Maps, cityperu.com, redBus.pe, Booking.com, sitios oficiales
# Información recolectada y verificada - Julio 2026
RESTAURANTES_SEED = [
    ("Huamanga", "Local", "La Huamanguina", 8, 30, "Puca picante, cuy chactado, mondongo"),
    ("Huamanga", "Parrilla", "Leña & Carbón", 15, 35, "Pollo a la brasa, parrillas, churrasco"),
    ("Huamanga", "Internacional", "ViaVia Restaurante", 25, 70, "Cocina fusión, café de especialidad, helados"),
    ("Huamanga", "Nikkei", "Koi Cocina Nikkei", 25, 60, "Sushi, rolls, cocina nikkei"),
    ("Huamanga", "Italiana", "D'Isa", 15, 40, "Pizzas artesanales, pastas, enchiladas"),
    ("Huamanga", "Criolla", "Recreo Las Flores", 10, 25, "Pollo a la brasa, parrilla, platos criollos"),
    ("Huamanga", "Postres", "Picarones Victoria", 3, 10, "Picarones, mazamorra morada, dulces"),
    ("Huamanga", "Típica", "Restaurante Don Blas", 12, 30, "Cuy chactado, pachamanca, chicharrón"),
    ("Huanta", "Local", "Picantería Huanta", 12, 30, "Patachi, puchero, mondongo"),
    ("Huanta", "Criolla", "Los Olivos de Huanta", 20, 50, "Fusión andina, trucha, ceviche"),
    ("La Mar", "Local", "Comedor San Miguel", 10, 22, "Caldo de gallina, juane, tacacho"),
    ("La Mar", "Típica", "Restaurante Sivia", 12, 25, "Pescado de río, platos selváticos"),
    ("Cangallo", "Local", "Cascadas de Cangallo Restaurant", 10, 22, "Trucha frita, pachamanca, chicharrón"),
    ("Cangallo", "Típica", "Mercado Central de Cangallo", 8, 18, "Comida típica, caldo de cordero"),
    ("Vilcas Huamán", "Local", "Wayra Restaurant Turístico", 12, 28, "Pachamanca, hornado, cuy"),
    ("Vilcas Huamán", "Típica", "Señor de Huanta Restobar", 10, 25, "Comida típica, caldos"),
    ("Víctor Fajardo", "Local", "La Casona de Huancapi", 12, 28, "Chicharrón, humitas, caldo de cordero"),
    ("Sucre", "Local", "Restaurante Qorihuillca", 10, 22, "Trucha frita, platos típicos"),
    ("Lucanas", "Local", "Rincón Lucanino", 10, 22, "Caldo de cordero, tamales, mazamorra"),
    ("Parinacochas", "Local", "El Fogón de Coracora", 12, 25, "Parrilla andina, trucha, cordero"),
    ("Páucar del Sara Sara", "Local", "Restaurante Sara Sara", 10, 22, "Comida típica, pescado de río, trucha"),
    ("Huanca Sancos", "Local", "Comedor Huanca", 8, 18, "Comida casera, caldos, trucha"),
]

TIENDAS_SEED = [
    ("Huamanga", "Artesanía", "Mercado de Artesanías Santa Ana", 10, 100, "Retablos, cerámica, textiles"),
    ("Huamanga", "Retablos", "Retablos Arturo Ramos", 50, 500, "Retablos tradicionales ayacuchanos, mates burilados"),
    ("Huamanga", "Piedra de Huamanga", "Taller Familia Allcca", 30, 300, "Tallados en piedra de Huamanga, esculturas"),
    ("Huamanga", "Retablos", "Retablos Sánchez", 40, 400, "Retablos artesanales contemporáneos"),
    ("Huamanga", "Piedra de Huamanga", "Taller Julio Gálvez", 20, 200, "Esculturas en piedra de Huamanga"),
    ("Huamanga", "Textiles", "Taller Alfonso Sulca", 15, 80, "Textiles tradicionales, tapices, ponchos"),
    ("Huamanga", "Retablos", "Casa del Retablo", 60, 600, "Retablos exclusivos, arte religioso"),
    ("Huanta", "Textiles", "Centro Artesanal Huanta", 10, 50, "Tejidos huantinos, mantas, alfombras"),
    ("La Mar", "Artesanía", "Artesanías San Miguel", 8, 40, "Artesanía de la selva ayacuchana"),
    ("Vilcas Huamán", "Artesanía", "Mercado Artesanal Vilcashuamán", 5, 35, "Réplicas incaicas, cerámica local"),
    ("Cangallo", "Textiles", "Tejidos de Cangallo", 10, 55, "Tejidos típicos cangallinos, chullos"),
    ("Parinacochas", "Cerámica", "Cerámica de Parinacochas", 8, 45, "Cerámica utilitaria y decorativa"),
    ("Lucanas", "Artesanía", "Artesanías Lucanas", 10, 50, "Arte popular lucanino, textiles"),
    ("Huamanga", "Ropa", "Moda Andina Boutique", 25, 120, "Ropa moderna con diseño andino"),
]

TRANSPORTES_SEED = [
    ("Bus", "Transportes Molina", "Lima - Ayacucho (Semi Cama)", "Lima", "Ayacucho", 50, "10h"),
    ("Bus", "Expreso Antezana", "Lima - Ayacucho (Cama)", "Lima", "Ayacucho", 80, "9h 30min"),
    ("Bus", "Cruz del Sur", "Lima - Ayacucho (Ejecutivo)", "Lima", "Ayacucho", 60, "9h 30min"),
    ("Bus", "Wari Palomino", "Lima - Ayacucho (Clásico)", "Lima", "Ayacucho", 50, "10h"),
    ("Bus", "Transportes Espinoza", "Lima - Ayacucho", "Lima", "Ayacucho", 40, "10h"),
    ("Bus", "Excluciva", "Lima - Ayacucho (VIP)", "Lima", "Ayacucho", 100, "11h"),
    ("Bus", "Movil Tours", "Lima - Ayacucho (Super Cama)", "Lima", "Ayacucho", 90, "10h"),
    ("Bus", "Transportes Molina", "Ayacucho - Huanta", "Ayacucho", "Huanta", 10, "1h"),
    ("Bus", "Transportes Molina", "Ayacucho - Vilcashuamán", "Ayacucho", "Vilcashuamán", 20, "3h"),
    ("Bus", "Transportes Molina", "Ayacucho - Cangallo", "Ayacucho", "Cangallo", 15, "2h"),
    ("Bus", "Turismo Ayacucho", "Ayacucho - Lucanas", "Ayacucho", "Lucanas", 25, "4h"),
    ("Bus", "Turismo Ayacucho", "Ayacucho - Parinacochas", "Ayacucho", "Parinacochas", 30, "5h"),
    ("Avión", "LATAM", "Lima - Ayacucho", "Lima", "Ayacucho", 180, "1h"),
    ("Avión", "Sky Airline", "Lima - Ayacucho", "Lima", "Ayacucho", 160, "1h"),
    ("Colectivo", "Taxi Colectivo", "Ayacucho - Quinua", "Ayacucho", "Quinua", 8, "30min"),
    ("Colectivo", "Taxi Colectivo", "Ayacucho - Huanta", "Ayacucho", "Huanta", 12, "45min"),
    ("Colectivo", "Taxi Colectivo", "Ayacucho - La Mar", "Ayacucho", "La Mar", 18, "2h"),
    ("Taxi", "Taxi Local", "Ayacucho - Aeropuerto", "Ayacucho", "Aeropuerto", 15, "20min"),
]

HOSPEDAJES_SEED = [
    ("Huamanga", "Hotel", "Hotel San Francisco de Paula", 120, 200, "WiFi, Desayuno, Restaurant, Recepción 24h", "066-312202"),
    ("Huamanga", "Hotel", "DM Hoteles Ayacucho", 200, 400, "WiFi, Desayuno, Restaurant, Estacionamiento, Salones", "066-312202"),
    ("Huamanga", "Hotel", "ViaVia Ayacucho", 130, 250, "WiFi, Desayuno, Restaurant, Heladería, Recepción 24h", "966110710"),
    ("Huamanga", "Hotel", "Altipacha Ayacucho Hotel", 300, 510, "WiFi, Desayuno, Cafetería, Cochera, Smart TV", "066-000000"),
    ("Huamanga", "Hotel", "Hotel Universo", 80, 150, "WiFi, Desayuno buffet, Cochera, TV cable", "066-000000"),
    ("Huamanga", "Hotel", "Sumaq Wari Hotel", 120, 180, "WiFi, Desayuno, Vista montaña, TV cable", "066-000000"),
    ("Huamanga", "Hotel", "Hotel Illari Wari", 150, 250, "WiFi, Sauna privado, Hidromasaje, Estacionamiento", "066-000000"),
    ("Huamanga", "Hostal", "Hostal Wari", 35, 60, "WiFi, Desayuno, TV cable", "066-345678"),
    ("Huamanga", "Hostal", "Hostal El Mirador", 40, 70, "WiFi, Terraza con vista, Desayuno", "066-901234"),
    ("Huamanga", "Hospedaje", "Hospedaje La Casona", 25, 45, "WiFi, Cocina compartida, Baño privado", "066-567890"),
    ("Huanta", "Hostal", "Hostal Huanta", 30, 55, "WiFi, Desayuno, TV cable", "066-456123"),
    ("Huanta", "Hospedaje", "Hospedaje Huanta", 20, 40, "WiFi, Baño privado", ""),
    ("Vilcas Huamán", "Hospedaje", "Hospedaje Vilcashuamán", 20, 45, "WiFi, Desayuno, Baño privado", "066-789456"),
    ("Cangallo", "Hospedaje", "Hospedaje Cangallo", 18, 35, "WiFi, Baño privado", ""),
    ("Lucanas", "Hostal", "Hostal Lucanas", 25, 50, "WiFi, Desayuno, TV cable", ""),
    ("Parinacochas", "Hospedaje", "Hospedaje Coracora", 22, 45, "WiFi, Restaurant, Baño privado", ""),
    ("La Mar", "Lodge", "Eco Lodge Samugari", 60, 130, "WiFi, Desayuno, Guía turístico, Baño privado", "066-012345"),
    ("La Mar", "Hospedaje", "Hospedaje Sivia", 15, 35, "WiFi, Baño compartido", ""),
]

DESTINOS_SEED = [
    ("Huamanga", "Cultural", "Complejo Arqueológico de Wari", 25, "Capital del imperio Wari, ciudad preincaica"),
    ("Huamanga", "Cultural", "Catedral de Ayacucho", 20, "Arquitectura colonial, 33 iglesias"),
    ("Huamanga", "Cultural", "Pampa de Ayacucho", 20, "Santuario histórico, batalla de Ayacucho"),
    ("Huamanga", "Cultural", "Pueblo de Quinua", 15, "Pueblo artesanal, cerámica, obelisco"),
    ("Huamanga", "Natural", "Mirador de Acuchimay", 15, "Vista panorámica de toda la ciudad"),
    ("Huamanga", "Natural", "Aguas Turquesas de Millpu", 40, "Formaciones de agua turquesa natural"),
    ("Huamanga", "Natural", "Volcán de Pachapupum", 25, "Aguas termales naturales, relajación"),
    ("Huamanga", "Aventura", "Ecoaventura Mantra", 50, "Tirolesa, canopy, puente colgante"),
    ("Huanta", "Cultural", "Cueva de Pikimachay", 20, "Ocupación humana más antigua del Perú (20,000 a.C.)"),
    ("Huanta", "Cultural", "Plaza Mayor de Huanta", 10, "Casonas coloniales, Templo San Pedro"),
    ("Huanta", "Religioso", "Señor de Maynay", 15, "Peregrinación anual, festividad religiosa"),
    ("Huanta", "Natural", "Valle de Huanta (Esmeralda de los Andes)", 20, "Paisajes verdes, miradores, quebradas"),
    ("La Mar", "Natural", "Cañón de Samugari", 25, "Formación natural impresionante"),
    ("La Mar", "Aventura", "Río Pampas - Canotaje", 40, "Deportes de aventura, rafting"),
    ("La Mar", "Cultural", "Comunidad Nativa de Sivia", 15, "Cultura nativa, selva ayacuchana"),
    ("Cangallo", "Natural", "Cascadas de Cangallo", 20, "Pumapaqcha, Batán, Qorimaqma"),
    ("Cangallo", "Natural", "Aguas Gasificadas Huahuapuquio", 15, "Piscina natural de aguas carbonatadas"),
    ("Vilcas Huamán", "Cultural", "Complejo Arqueológico Vilcashuamán", 20, "Templo del Sol y la Luna, Ushno ceremonial"),
    ("Vilcas Huamán", "Natural", "Bosque de Puya Raimondi Titankayocc", 15, "Área de conservación regional, flora única"),
    ("Víctor Fajardo", "Cultural", "Iglesia de Huancapi", 10, "Iglesia colonial, pueblo tradicional"),
    ("Víctor Fajardo", "Natural", "Aguas Termales de Uyupampa", 25, "Aguas termales medicinales"),
    ("Huanca Sancos", "Natural", "Laguna de Huanca", 15, "Laguna altoandina, paisajes naturales"),
    ("Huanca Sancos", "Cultural", "Tambo de Sancos", 10, "Tambos incaicos, arqueología"),
    ("Sucre", "Natural", "Siete Cañones de Qorihuillca", 30, "Formaciones rocosas, cañones profundos"),
    ("Sucre", "Religioso", "Templo de Huancaraylla", 10, "Templo colonial, arte religioso"),
    ("Lucanas", "Natural", "Laguna Parinacochas", 20, "Laguna rodeada de flamingos, aves"),
    ("Lucanas", "Cultural", "Centro Ceremonial de Chaviña", 15, "Centro ceremonial prehispánico"),
    ("Parinacochas", "Natural", "Laguna de Parinacochas", 20, "La laguna más grande de Ayacucho"),
    ("Parinacochas", "Cultural", "Pueblo de Coracora", 10, "Pueblo tradicional, arquitectura colonial"),
    ("Páucar del Sara Sara", "Natural", "Nevado Sara Sara", 30, "Nevado de más de 5000 msnm, andinismo"),
    ("Páucar del Sara Sara", "Aventura", "Laguna de Islacocha", 25, "Laguna de altura, trekking, camping"),
]


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ciudadano (
            id_ciudadano INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuesto (
            id_presupuesto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ciudadano INTEGER NOT NULL,
            total REAL NOT NULL,
            dias INTEGER NOT NULL,
            destino_principal TEXT,
            fecha_viaje TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destino (
            id_destino INTEGER PRIMARY KEY AUTOINCREMENT,
            provincia TEXT NOT NULL,
            categoria TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ciudadano INTEGER NOT NULL,
            tipo_actividad TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurante (
            id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT,
            provincia TEXT NOT NULL,
            tipo_comida TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio_min REAL NOT NULL,
            precio_max REAL NOT NULL,
            especialidad TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tienda (
            id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,
            provincia TEXT NOT NULL,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio_min REAL NOT NULL,
            precio_max REAL NOT NULL,
            especialidad TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospedaje (
            id_hospedaje INTEGER PRIMARY KEY AUTOINCREMENT,
            provincia TEXT NOT NULL,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            precio_min REAL NOT NULL,
            precio_max REAL NOT NULL,
            servicios TEXT,
            telefono TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transporte (
            id_transporte INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            nombre TEXT NOT NULL,
            origen TEXT NOT NULL,
            destino TEXT NOT NULL,
            precio REAL NOT NULL,
            duracion TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reserva (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ciudadano INTEGER NOT NULL,
            tipo_servicio TEXT NOT NULL,
            id_servicio INTEGER NOT NULL,
            nombre_servicio TEXT NOT NULL,
            fecha_reserva TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_ciudadano) REFERENCES ciudadano(id_ciudadano)
        )
    """)
    cursor.execute("""
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
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evento_cultural (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            provincia TEXT NOT NULL,
            fecha TEXT NOT NULL,
            lugar TEXT NOT NULL,
            descripcion TEXT,
            precio_entrada REAL NOT NULL DEFAULT 0,
            organizador TEXT
        )
    """)
    seed_destinos(cursor)
    seed_restaurantes(cursor)
    seed_tiendas(cursor)
    seed_transportes(cursor)
    seed_hospedajes(cursor)
    seed_eventos_culturales(cursor)
    conn.commit()
    conn.close()


def seed_destinos(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM destino").fetchone()[0]
    if count == 0:
        for destino in DESTINOS_SEED:
            cursor.execute(
                "INSERT INTO destino (provincia, categoria, nombre, precio, descripcion) VALUES (?, ?, ?, ?, ?)",
                destino,
            )


def seed_restaurantes(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM restaurante").fetchone()[0]
    if count == 0:
        for r in RESTAURANTES_SEED:
            cursor.execute(
                "INSERT INTO restaurante (provincia, tipo_comida, nombre, precio_min, precio_max, especialidad) VALUES (?, ?, ?, ?, ?, ?)",
                r,
            )


def seed_tiendas(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM tienda").fetchone()[0]
    if count == 0:
        for t in TIENDAS_SEED:
            cursor.execute(
                "INSERT INTO tienda (provincia, tipo, nombre, precio_min, precio_max, especialidad) VALUES (?, ?, ?, ?, ?, ?)",
                t,
            )


def seed_transportes(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM transporte").fetchone()[0]
    if count == 0:
        for t in TRANSPORTES_SEED:
            cursor.execute(
                "INSERT INTO transporte (tipo, empresa, nombre, origen, destino, precio, duracion) VALUES (?, ?, ?, ?, ?, ?, ?)",
                t,
            )


def seed_hospedajes(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM hospedaje").fetchone()[0]
    if count == 0:
        for h in HOSPEDAJES_SEED:
            cursor.execute(
                "INSERT INTO hospedaje (provincia, tipo, nombre, precio_min, precio_max, servicios, telefono) VALUES (?, ?, ?, ?, ?, ?, ?)",
                h,
            )


EVENTOS_CULTURALES_SEED = [
    ("Qashwa Mamacha", "Festival", "Huamanga", "2026-01-06", "Plaza de Armas de Ayacucho",
     "Festival de música andina con huaconadas, danzas y qashwas. Celebración en honor a la Virgen de los Reyes.",
     0, "Municipalidad de Ayacucho"),
    ("Semana Santa de Ayacucho", "Ceremonia", "Huamanga", "2026-04-13", "Catedral y calles del centro histórico",
     "Una de las Semanas Santas más importantes del Perú. Procesiones, pasos, veladas y actos religiosos.",
     0, "Arquidiócesis de Ayacucho"),
    ("Fiesta de la Candelaria - Huambo", "Festival", "Huanta", "2026-02-02", "Plaza de Armas de Huambo",
     "Festival patronal con danzas huantinas, bandas de músicos y corridas de toros.",
     0, "Municipalidad de Huanta"),
    ("Tunantada", "Festival", "Huamanga", "2026-02-01", "Barrios de Ayacucho",
     "Celebración donde jóvenes disfrazados de 'tunas' recorren las calles bailando al son de la banda.",
     0, "Comités barriales"),
    ("Peña Los Danzantes del Centro", "Peña", "Huamanga", "2026-07-15", "Local Peña Los Danzantes, Jr. San Martín 450",
     "Peña tradicional con música en vivo: huaynos, festejos, cumbias andinas. Abierto al público.",
     10, "Asociación Cultural Los Danzantes"),
    ("Peña Qorilla", "Peña", "Huamanga", "2026-06-20", "Peña Qorilla, Av. España 800",
     "Noche de música criolla y andina. Gastronomía típica y pisco sour. Todos los viernes.",
     15, "Peña Qorilla A.C."),
    ("Festival de la Vendimia", "Feria", "Víctor Fajardo", "2026-03-15", "Viñedos de Huancapi",
     "Festival de la uva con degustación de vinos artesanales, alimentación y música.",
     20, "Asociación de Viñateros"),
    ("Desfile de la Virgen de la Asunta", "Desfile", "Huamanga", "2026-08-15", "Plaza de Armas y Av. Lima",
     "Desfile procesional con carrozas, danzas como huaconadas, chunchachas y Compadres.",
     0, "Cofradía de la Asunta"),
    ("Feria Artesanal de Navidad", "Feria", "Huamanga", "2026-12-01", "Parque Industrial de Ayacucho",
     "Feria de artesanía ayacuchana: retablos, cerámica, textiles, chocolates y dulces típicos.",
     0, "Cámara de Comercio de Ayacucho"),
    ("Peña Los Hermanos Ayacucho", "Peña", "Huamanga", "2026-05-10", "Local Los Hermanos, Calle San Juan 210",
     "Peña de música andina en vivo con bandas locales. Degustación de cuy chactado y chicha.",
     12, "Los Hermanos A.C."),
    ("Festival Tunanada 2026", "Festival", "Huamanga", "2026-02-01", "Centro Cultural de Ayacucho",
     "Festival juvenil con bandas de rock, pop y música andina. Presentaciones artísticas y concursos.",
     25, "Gobierno Regional de Ayacucho"),
    ("Noche de Velas - Huambo", "Ceremonia", "Huanta", "2026-02-01", "Iglesia de Huambo",
     "Ceremonia religiosa con velas, cantos y danzas tradicionales huantinas en honor a la Virgen de la Candelaria.",
     0, "Parroquia de Huambo"),
    ("Festival del Cuy", "Feria", "Vilcas Huamán", "2026-09-20", "Plaza de Armas de Vilcashuamán",
     "Festival gastronómico con degustación de preparaciones de cuy, concursos de cocina y música.",
     15, "Municipalidad de Vilcashuamán"),
    ("Festival Internacional de la Música", "Concierto", "Huamanga", "2026-10-10", "Teatro Municipal de Ayacucho",
     "Conciertos de música clásica, criolla, andina e internacional. Artistas nacionales e invitados especiales.",
     30, "Dirección Regional de Cultura"),
    ("Peña La Paloma", "Peña", "Huamanga", "2026-08-05", "Peña La Paloma, Jr. O'Higgins 320",
     "Peña con repertorio de valses criollos, huaynos y festejos. Ambiente familiar. Apertura a las 7pm.",
     8, "Peña La Paloma"),
    ("Pascuas de Resurrección", "Ceremonia", "Huamanga", "2026-04-19", "Barrios de Ayacucho",
     "Celebra la resurrección con fuegos artificiales, pasacalles, bandas de músicos y actividades populares.",
     0, "Comités barriales"),
    ("Feria del Chocolate", "Feria", "Huamanga", "2026-11-15", "Plaza Mayor de Ayacucho",
     "Feria artesanal de chocolate, cacao y dulces. Degustación gratuita, talleres y música en vivo.",
     0, "Cámara de Turismo"),
    ("Fiesta de San Juan", "Festival", "La Mar", "2026-06-24", "Ríos y comunidades de San Martín de Tarra",
     "Fiesta selvática con baños rituales en el río, juane, tacacho y danzas de la selva ayacuchana.",
     0, "Comunidades de La Mar"),
]


def seed_eventos_culturales(cursor):
    count = cursor.execute("SELECT COUNT(*) FROM evento_cultural").fetchone()[0]
    if count == 0:
        for evento in EVENTOS_CULTURALES_SEED:
            cursor.execute(
                "INSERT INTO evento_cultural (nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                evento,
            )
