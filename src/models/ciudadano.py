import re
import sqlite3
from src.database import get_connection


class Ciudadano:
    def __init__(self, nombre, email, telefono, contrasena):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.contrasena = contrasena

    @staticmethod
    def validar_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @staticmethod
    def validar_telefono(telefono):
        return re.match(r"^\+?\d{7,15}$", telefono) is not None

    @staticmethod
    def validar_contrasena(contrasena):
        return len(contrasena) >= 6

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO ciudadano (nombre, email, telefono, contrasena) VALUES (?, ?, ?, ?)",
                (self.nombre, self.email, self.telefono, self.contrasena),
            )
            conn.commit()
            self.id_ciudadano = cursor.lastrowid
            return True, "Registro exitoso"
        except sqlite3.IntegrityError:
            return False, "El email ya está registrado"
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_ciudadano, nombre, email, telefono, contrasena=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if contrasena:
                cursor.execute(
                    "UPDATE ciudadano SET nombre=?, email=?, telefono=?, contrasena=? WHERE id_ciudadano=?",
                    (nombre, email, telefono, contrasena, id_ciudadano),
                )
            else:
                cursor.execute(
                    "UPDATE ciudadano SET nombre=?, email=?, telefono=? WHERE id_ciudadano=?",
                    (nombre, email, telefono, id_ciudadano),
                )
            conn.commit()
            return True, "Perfil actualizado exitosamente"
        except sqlite3.IntegrityError:
            return False, "El email ya está en uso por otro ciudadano"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def iniciar_sesion(email, contrasena):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ciudadano WHERE email = ? AND contrasena = ?",
            (email, contrasena),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return True, dict(row)
        return False, "Email o contraseña incorrectos"

    @staticmethod
    def obtener_por_email(email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ciudadano WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def cambiar_contrasena(id_ciudadano, nueva_contrasena):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ciudadano SET contrasena = ? WHERE id_ciudadano = ?",
            (nueva_contrasena, id_ciudadano),
        )
        conn.commit()
        conn.close()
        return True, "Contraseña actualizada exitosamente"
