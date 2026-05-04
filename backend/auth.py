import bcrypt
import sqlite3
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "sistema_laboratorio.db")

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class Auth:

    def validar_login(self, usuario, contrasena):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT contrasena, rol FROM usuarios WHERE usuario = ?", (usuario,))
            row = cursor.fetchone()

            if not row:
                return {"ok": False, "mensaje": "Usuario o contraseña incorrectos"}

            contrasena_hash = row["contrasena"]
            rol = row["rol"]

            if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hash.encode('utf-8')):
                return {"ok": True, "rol": rol}
            else:
                return {"ok": False, "mensaje": "Usuario o contraseña incorrectos"}

        except Exception as e:
            print("Error en login:", e)
            return {"ok": False, "mensaje": "Error del sistema"}
        finally:
            conn.close()

    def hashear_contrasena(self, contrasena):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

    def verificar_contrasena(self, contrasena_ingresada, hash_guardado):
        try:
            return bcrypt.checkpw(
                contrasena_ingresada.encode('utf-8'),
                hash_guardado.encode('utf-8')
            )
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return False