from src.database import get_connection


class Restaurante:
    def __init__(self, id_restaurante=None):
        self.id_restaurante = id_restaurante

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurante ORDER BY provincia, nombre")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_restaurante):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE id_restaurante = ?", (id_restaurante,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_provincia(provincia):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE provincia = ? ORDER BY nombre", (provincia,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_tipo(tipo_comida):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurante WHERE tipo_comida = ? ORDER BY nombre", (tipo_comida,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def provincias():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT provincia FROM restaurante ORDER BY provincia")
        rows = cursor.fetchall()
        conn.close()
        return [row["provincia"] for row in rows]

    @staticmethod
    def tipos_comida():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo_comida FROM restaurante ORDER BY tipo_comida")
        rows = cursor.fetchall()
        conn.close()
        return [row["tipo_comida"] for row in rows]

    @staticmethod
    def agregar(provincia, tipo_comida, nombre, precio_min, precio_max, especialidad):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO restaurante (provincia, tipo_comida, nombre, precio_min, precio_max, especialidad) VALUES (?, ?, ?, ?, ?, ?)",
                (provincia, tipo_comida, nombre, precio_min, precio_max, especialidad),
            )
            conn.commit()
            return True, "Restaurante agregado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_restaurante, provincia, tipo_comida, nombre, precio_min, precio_max, especialidad):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE restaurante SET provincia=?, tipo_comida=?, nombre=?, precio_min=?, precio_max=?, especialidad=? WHERE id_restaurante=?",
                (provincia, tipo_comida, nombre, precio_min, precio_max, especialidad, id_restaurante),
            )
            conn.commit()
            return True, "Restaurante actualizado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_restaurante):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM restaurante WHERE id_restaurante = ?", (id_restaurante,))
            conn.commit()
            return True, "Restaurante eliminado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
