from src.database import get_connection


class Hospedaje:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospedaje ORDER BY provincia, nombre")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_hospedaje):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospedaje WHERE id_hospedaje = ?", (id_hospedaje,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_provincia(provincia):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospedaje WHERE provincia = ? ORDER BY nombre", (provincia,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_tipo(tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospedaje WHERE tipo = ? ORDER BY nombre", (tipo,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def provincias():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT provincia FROM hospedaje ORDER BY provincia")
        rows = cursor.fetchall()
        conn.close()
        return [row["provincia"] for row in rows]

    @staticmethod
    def tipos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM hospedaje ORDER BY tipo")
        rows = cursor.fetchall()
        conn.close()
        return [row["tipo"] for row in rows]

    @staticmethod
    def agregar(provincia, tipo, nombre, precio_min, precio_max, servicios, telefono):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO hospedaje (provincia, tipo, nombre, precio_min, precio_max, servicios, telefono) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (provincia, tipo, nombre, precio_min, precio_max, servicios, telefono),
            )
            conn.commit()
            return True, "Hospedaje agregado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_hospedaje, provincia, tipo, nombre, precio_min, precio_max, servicios, telefono):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE hospedaje SET provincia=?, tipo=?, nombre=?, precio_min=?, precio_max=?, servicios=?, telefono=? WHERE id_hospedaje=?",
                (provincia, tipo, nombre, precio_min, precio_max, servicios, telefono, id_hospedaje),
            )
            conn.commit()
            return True, "Hospedaje actualizado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_hospedaje):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM hospedaje WHERE id_hospedaje = ?", (id_hospedaje,))
            conn.commit()
            return True, "Hospedaje eliminado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
