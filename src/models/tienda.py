from src.database import get_connection


class Tienda:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tienda ORDER BY provincia, nombre")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_tienda):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tienda WHERE id_tienda = ?", (id_tienda,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_provincia(provincia):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tienda WHERE provincia = ? ORDER BY nombre", (provincia,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_tipo(tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tienda WHERE tipo = ? ORDER BY nombre", (tipo,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def provincias():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT provincia FROM tienda ORDER BY provincia")
        rows = cursor.fetchall()
        conn.close()
        return [row["provincia"] for row in rows]

    @staticmethod
    def tipos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM tienda ORDER BY tipo")
        rows = cursor.fetchall()
        conn.close()
        return [row["tipo"] for row in rows]

    @staticmethod
    def agregar(provincia, tipo, nombre, precio_min, precio_max, especialidad):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tienda (provincia, tipo, nombre, precio_min, precio_max, especialidad) VALUES (?, ?, ?, ?, ?, ?)",
                (provincia, tipo, nombre, precio_min, precio_max, especialidad),
            )
            conn.commit()
            return True, "Tienda agregada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_tienda, provincia, tipo, nombre, precio_min, precio_max, especialidad):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE tienda SET provincia=?, tipo=?, nombre=?, precio_min=?, precio_max=?, especialidad=? WHERE id_tienda=?",
                (provincia, tipo, nombre, precio_min, precio_max, especialidad, id_tienda),
            )
            conn.commit()
            return True, "Tienda actualizada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_tienda):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tienda WHERE id_tienda = ?", (id_tienda,))
            conn.commit()
            return True, "Tienda eliminada exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
