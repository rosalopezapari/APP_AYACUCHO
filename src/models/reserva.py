from src.database import get_connection


class Reserva:
    @staticmethod
    def listar_por_ciudadano(id_ciudadano):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reserva WHERE id_ciudadano = ? ORDER BY created_at DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_estado(id_ciudadano, estado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reserva WHERE id_ciudadano = ? AND estado = ? ORDER BY created_at DESC",
            (id_ciudadano, estado),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def agregar(id_ciudadano, tipo_servicio, id_servicio, nombre_servicio, fecha_reserva):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO reserva (id_ciudadano, tipo_servicio, id_servicio, nombre_servicio, fecha_reserva) VALUES (?, ?, ?, ?, ?)",
                (id_ciudadano, tipo_servicio, id_servicio, nombre_servicio, fecha_reserva),
            )
            conn.commit()
            return True, "Reserva creada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(id_reserva, nuevo_estado):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE reserva SET estado = ? WHERE id_reserva = ?",
                (nuevo_estado, id_reserva),
            )
            conn.commit()
            return True, f"Reserva {nuevo_estado.lower()}"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_reserva):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM reserva WHERE id_reserva = ?", (id_reserva,))
            conn.commit()
            return True, "Reserva eliminada"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def tipos_servicio():
        return ["Restaurante", "Hospedaje", "Transporte", "Destino"]

    @staticmethod
    def estados():
        return ["Pendiente", "Confirmada", "Cancelada"]

    @staticmethod
    def obtener_servicios_por_tipo(tipo):
        conn = get_connection()
        cursor = conn.cursor()
        tabla = {
            "Restaurante": "restaurante",
            "Hospedaje": "hospedaje",
            "Transporte": "transporte",
            "Destino": "destino",
        }
        t = tabla.get(tipo)
        if not t:
            conn.close()
            return []
        cursor.execute(f"SELECT * FROM {t} ORDER BY nombre")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
