
from backend.database import conectar
from backend.auth import Auth

auth = Auth()

class Usuarios:
    def crear_usuario(self, usuario, contrasena, rol):
        conn = conectar()
        cursor = conn.cursor()
        try:
            contrasena_hash = auth.hashear_contrasena(contrasena)
            cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, rol)
                VALUES (?, ?, ?)
            """, (usuario, contrasena_hash, rol))
            conn.commit()
            return True
        except Exception as e:
            print("Error al crear usuario:", e)
            return False
        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, rol FROM usuarios ORDER BY usuario ASC")
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]

    def actualizar_rol(self, user_id, nuevo_rol):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar rol:", e)
            return False
        finally:
            conn.close()

    def actualizar_contrasena(self, user_id, nueva_contrasena):
        conn = conectar()
        cursor = conn.cursor()
        try:
            contrasena_hash = auth.hashear_contrasena(nueva_contrasena)
            cursor.execute("UPDATE usuarios SET contrasena = ? WHERE id = ?", (contrasena_hash, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar contraseña:", e)
            return False
        finally:
            conn.close()

    def eliminar_usuario(self, user_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al eliminar usuario:", e)
            return False
        finally:
            conn.close()

    def verificar_contrasena_admin(self, contrasena):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = 'admin' AND rol = 'admin'")
            row = cursor.fetchone()
            if not row:
                return False
            return bcrypt.checkpw(contrasena.encode('utf-8'), row["contrasena"].encode('utf-8'))
        except Exception as e:
            print("Error al verificar admin:", e)
            return False
        finally:
            conn.close()