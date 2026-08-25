import sqlite3
from src.database import get_connection


class EventoCultural:
    TIPOS = ("Festival", "Peña", "Desfile", "Concierto", "Feria", "Ceremonia", "Exposición", "Taller")

    PROVINCIAS = (
        "Huamanga", "Huanta", "La Mar", "Cangallo", "Vilcas Huamán",
        "Víctor Fajardo", "Sucre", "Lucanas", "Parinacochas",
        "Páucar del Sara Sara", "Huanca Sancos",
    )

    def __init__(self, nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador=None):
        self.nombre = nombre
        self.tipo = tipo
        self.provincia = provincia
        self.fecha = fecha
        self.lugar = lugar
        self.descripcion = descripcion
        self.precio_entrada = precio_entrada
        self.organizador = organizador

    @staticmethod
    def listar_todos():
        conn = get_connection()
        rows = conn.execute("SELECT * FROM evento_cultural ORDER BY fecha DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def obtener(id_evento):
        conn = get_connection()
        row = conn.execute("SELECT * FROM evento_cultural WHERE id_evento = ?", (id_evento,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_tipo(tipo):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM evento_cultural WHERE tipo = ? ORDER BY fecha DESC", (tipo,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def listar_por_provincia(provincia):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM evento_cultural WHERE provincia = ? ORDER BY fecha DESC", (provincia,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def agregar(nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador=None):
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO evento_cultural (nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador),
            )
            conn.commit()
            return True, "Evento registrado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_evento, nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador=None):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE evento_cultural SET nombre=?, tipo=?, provincia=?, fecha=?, lugar=?, "
                "descripcion=?, precio_entrada=?, organizador=? WHERE id_evento=?",
                (nombre, tipo, provincia, fecha, lugar, descripcion, precio_entrada, organizador, id_evento),
            )
            conn.commit()
            return True, "Evento actualizado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_evento):
        conn = get_connection()
        try:
            conn.execute("DELETE FROM evento_cultural WHERE id_evento = ?", (id_evento,))
            conn.commit()
            return True, "Evento eliminado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
