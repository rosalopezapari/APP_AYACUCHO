from src.database import get_connection


class Destino:
    CATEGORIAS = ["Cultural", "Natural", "Gastronómico", "Aventura", "Compras"]
    PROVINCIAS = [
        "Huamanga", "Huanta", "La Mar", "Cangallo", "Vilcas Huamán",
        "Víctor Fajardo", "Huanca Sancos", "Sucre", "Lucanas",
        "Parinacochas", "Páucar del Sara Sara",
    ]

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destino ORDER BY provincia, nombre")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_destino):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destino WHERE id_destino = ?", (id_destino,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_provincia(provincia):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destino WHERE provincia = ? ORDER BY nombre", (provincia,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_categoria(categoria):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destino WHERE categoria = ? ORDER BY nombre", (categoria,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def agregar(provincia, categoria, nombre, precio, descripcion):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO destino (provincia, categoria, nombre, precio, descripcion) VALUES (?, ?, ?, ?, ?)",
                (provincia, categoria, nombre, precio, descripcion),
            )
            conn.commit()
            return True, "Destino agregado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_destino, provincia, categoria, nombre, precio, descripcion):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE destino SET provincia=?, categoria=?, nombre=?, precio=?, descripcion=? WHERE id_destino=?",
                (provincia, categoria, nombre, precio, descripcion, id_destino),
            )
            conn.commit()
            return True, "Destino actualizado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_destino):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM destino WHERE id_destino = ?", (id_destino,))
            conn.commit()
            return True, "Destino eliminado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
