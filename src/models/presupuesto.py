from src.database import get_connection
from src.models.destino import Destino
from src.models.restaurante import Restaurante
from src.models.transporte import Transporte
from src.models.hospedaje import Hospedaje


class Presupuesto:
    def __init__(self, id_ciudadano, total, dias, destino_principal="", fecha_viaje=""):
        self.id_ciudadano = id_ciudadano
        self.total = total
        self.dias = dias
        self.destino_principal = destino_principal
        self.fecha_viaje = fecha_viaje

    def gasto_diario(self):
        return round(self.total / self.dias, 2)

    def desglose(self):
        diario = self.gasto_diario()
        return {
            "total": self.total,
            "dias": self.dias,
            "diario": diario,
            "alojamiento": round(diario * 0.40, 2),
            "comida": round(diario * 0.30, 2),
            "transporte": round(diario * 0.20, 2),
            "extras": round(diario * 0.10, 2),
        }

    @staticmethod
    def calcular_integrado(total, dias, id_destino, id_restaurante, id_transporte, id_hospedaje):
        destino = Destino.obtener(id_destino)
        restaurante = Restaurante.obtener(id_restaurante)
        transporte = Transporte.obtener(id_transporte)
        hospedaje = Hospedaje.obtener(id_hospedaje)

        if not all([destino, restaurante, transporte, hospedaje]):
            return None

        costo_destino = destino["precio"]
        costo_comida = restaurante["precio_max"] * dias
        costo_transporte = transporte["precio"]
        costo_alojamiento = hospedaje["precio_max"] * dias
        costo_total = costo_destino + costo_comida + costo_transporte + costo_alojamiento
        diferencia = total - costo_total

        return {
            "destino": destino["nombre"],
            "restaurante": restaurante["nombre"],
            "transporte": transporte["nombre"],
            "hospedaje": hospedaje["nombre"],
            "costo_destino": costo_destino,
            "costo_comida": costo_comida,
            "costo_transporte": costo_transporte,
            "costo_alojamiento": costo_alojamiento,
            "costo_total": costo_total,
            "presupuesto": total,
            "dias": dias,
            "diferencia": diferencia,
            "dentro_presupuesto": diferencia >= 0,
        }

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO presupuesto
                (id_ciudadano, total, dias, destino_principal, fecha_viaje)
                VALUES (?, ?, ?, ?, ?)""",
                (self.id_ciudadano, self.total, self.dias, self.destino_principal, self.fecha_viaje),
            )
            conn.commit()
            return True, "Presupuesto guardado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def obtener_por_ciudadano(id_ciudadano):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM presupuesto WHERE id_ciudadano = ? ORDER BY created_at DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
