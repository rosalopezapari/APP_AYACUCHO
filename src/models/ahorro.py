from datetime import date
from src.database import get_connection


class Ahorro:
    @staticmethod
    def listar_por_ciudadano(id_ciudadano):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ahorro WHERE id_ciudadano = ? ORDER BY fecha_inicio DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_activos(id_ciudadano):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ahorro WHERE id_ciudadano = ? AND estado = 'En progreso' ORDER BY fecha_inicio DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_ahorro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ahorro WHERE id_ahorro = ?", (id_ahorro,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def agregar(id_ciudadano, meta, monto_objetivo, fecha_limite):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO ahorro (id_ciudadano, meta, monto_objetivo, monto_actual, fecha_inicio, fecha_limite, estado) VALUES (?, ?, ?, 0, ?, ?, 'En progreso')",
                (id_ciudadano, meta, monto_objetivo, date.today().isoformat(), fecha_limite or None),
            )
            conn.commit()
            return True, "Meta de ahorro creada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def aportar(id_ahorro, monto):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            a = Ahorro.obtener(id_ahorro)
            if not a:
                return False, "Meta no encontrada"
            nuevo_actual = a["monto_actual"] + monto
            nuevo_estado = "Completada" if nuevo_actual >= a["monto_objetivo"] else "En progreso"
            cursor.execute(
                "UPDATE ahorro SET monto_actual = ?, estado = ? WHERE id_ahorro = ?",
                (nuevo_actual, nuevo_estado, id_ahorro),
            )
            conn.commit()
            msg = "¡Meta completada!" if nuevo_estado == "Completada" else f"Ahorro actualizado: S/ {nuevo_actual:.2f}"
            return True, msg
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_ahorro, meta, monto_objetivo, fecha_limite):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            a = Ahorro.obtener(id_ahorro)
            if not a:
                return False, "Meta no encontrada"
            cursor.execute(
                "UPDATE ahorro SET meta=?, monto_objetivo=?, fecha_limite=? WHERE id_ahorro=?",
                (meta, monto_objetivo, fecha_limite or None, id_ahorro),
            )
            conn.commit()
            return True, "Meta actualizada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_ahorro):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM ahorro WHERE id_ahorro = ?", (id_ahorro,))
            conn.commit()
            return True, "Meta eliminada"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
