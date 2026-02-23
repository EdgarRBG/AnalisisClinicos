from backend.database import conectar

class Usuarios:
    def crear_usuario(self, usuario, contrasena, rol):
        if not usuario or not contrasena or not rol:
            print("Error: Campos incompletos al crear usuario")
            return False

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, rol)
                VALUES (?, ?, ?)
            """, (usuario, contrasena, rol))
            conn.commit()
            print(f"Usuario creado con éxito: {usuario} (ID: {cursor.lastrowid})")
            return cursor.lastrowid
        except Exception as e:
            print(f"ERROR al crear usuario '{usuario}': {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, usuario, rol FROM usuarios ORDER BY id ASC")
            filas = cursor.fetchall()
            print(f"Usuarios encontrados en la base: {len(filas)}")
            print("Datos:", filas)
            return [dict(row) for row in filas]
        except Exception as e:
            print(f"ERROR en obtener_todos: {str(e)}")
            return []
        finally:
            conn.close()

    def actualizar_rol(self, user_id, nuevo_rol):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, user_id))
            conn.commit()
            print(f"Rol actualizado para ID {user_id}: {nuevo_rol}")
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar rol: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def actualizar_contrasena(self, user_id, nueva_contrasena):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuarios SET contrasena = ? WHERE id = ?", (nueva_contrasena, user_id))
            conn.commit()
            print(f"Contraseña actualizada para ID {user_id}")
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar contraseña: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def eliminar_usuario(self, user_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conn.commit()
            print(f"Usuario ID {user_id} eliminado")
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()