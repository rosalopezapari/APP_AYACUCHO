from src.database import get_connection


class Transporte:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transporte ORDER BY tipo, empresa")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener(id_transporte):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transporte WHERE id_transporte = ?", (id_transporte,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def listar_por_tipo(tipo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transporte WHERE tipo = ? ORDER BY precio", (tipo,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_origen(origen):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transporte WHERE origen LIKE ? ORDER BY precio", (f"%{origen}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def listar_por_destino(destino):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transporte WHERE destino LIKE ? ORDER BY precio", (f"%{destino}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def tipos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tipo FROM transporte ORDER BY tipo")
        rows = cursor.fetchall()
        conn.close()
        return [row["tipo"] for row in rows]

    @staticmethod
    def empresas():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT empresa FROM transporte ORDER BY empresa")
        rows = cursor.fetchall()
        conn.close()
        return [row["empresa"] for row in rows]

    @staticmethod
    def destinos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT destino FROM transporte ORDER BY destino")
        rows = cursor.fetchall()
        conn.close()
        return [row["destino"] for row in rows]

    @staticmethod
    def agregar(tipo, empresa, nombre, origen, destino, precio, duracion):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO transporte (tipo, empresa, nombre, origen, destino, precio, duracion) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tipo, empresa, nombre, origen, destino, precio, duracion),
            )
            conn.commit()
            return True, "Transporte agregado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_transporte, tipo, empresa, nombre, origen, destino, precio, duracion):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE transporte SET tipo=?, empresa=?, nombre=?, origen=?, destino=?, precio=?, duracion=? WHERE id_transporte=?",
                (tipo, empresa, nombre, origen, destino, precio, duracion, id_transporte),
            )
            conn.commit()
            return True, "Transporte actualizado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_transporte):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM transporte WHERE id_transporte = ?", (id_transporte,))
            conn.commit()
            return True, "Transporte eliminado exitosamente"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()
