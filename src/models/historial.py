from src.database import get_connection


class Historial:
    def __init__(self):
        pass

    @staticmethod
    def registrar(id_ciudadano, tipo_actividad, descripcion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO historial (id_ciudadano, tipo_actividad, descripcion) VALUES (?, ?, ?)",
            (id_ciudadano, tipo_actividad, descripcion),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_ciudadano(id_ciudadano, tipo=None):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM historial WHERE id_ciudadano = ?"
        params = [id_ciudadano]
        if tipo:
            query += " AND tipo_actividad = ?"
            params.append(tipo)
        query += " ORDER BY fecha DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def tipos_actividad():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo_actividad FROM historial ORDER BY tipo_actividad")
        rows = cursor.fetchall()
        conn.close()
        return [row["tipo_actividad"] for row in rows]
