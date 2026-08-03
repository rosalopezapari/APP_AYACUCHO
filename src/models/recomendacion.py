from src.database import get_connection


class Recomendacion:
    CATEGORIAS = ["Cultural", "Natural", "Gastronómico", "Aventura", "Compras"]
    PROVINCIAS = [
        "Huamanga", "Huanta", "La Mar", "Cangallo", "Vilcas Huamán",
        "Víctor Fajardo", "Huanca Sancos", "Sucre", "Lucanas",
        "Parinacochas", "Páucar del Sara Sara",
    ]

    def __init__(self, presupuesto_total, dias):
        self.presupuesto_total = presupuesto_total
        self.dias = dias
        self.presupuesto_diario = presupuesto_total / dias if dias > 0 else 0

    @staticmethod
    def obtener_destinos(provincia=None, categoria=None, precio_max=None):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM destino WHERE 1=1"
        params = []

        if provincia:
            query += " AND provincia = ?"
            params.append(provincia)
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if precio_max:
            query += " AND precio <= ?"
            params.append(precio_max)

        query += " ORDER BY provincia, categoria"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def recomendar(self, provincia=None):
        destinos = self.obtener_destinos(
            provincia=provincia,
            precio_max=self.presupuesto_diario,
        )
        return destinos

    def resumen_recomendacion(self, provincia=None):
        destinos = self.recomendar(provincia)
        total_gasto = sum(d["precio"] for d in destinos)
        return {
            "destinos": destinos,
            "total": total_gasto,
            "presupuesto_diario": self.presupuesto_diario,
            "promedio_por_destino": round(total_gasto / len(destinos), 2) if destinos else 0,
            "dentro_presupuesto": total_gasto <= self.presupuesto_diario,
            "categoria_distribucion": self._distribucion_categorias(destinos),
        }

    @staticmethod
    def _distribucion_categorias(destinos):
        dist = {}
        for d in destinos:
            cat = d["categoria"]
            dist[cat] = dist.get(cat, 0) + 1
        return dist

    @staticmethod
    def obtener_por_provincia(provincia):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destino WHERE provincia = ? ORDER BY precio", (provincia,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
