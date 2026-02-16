from backend.database import conectar


class Auth:
    def validar_login(self, usuario, contraseña):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rol FROM usuarios 
            WHERE usuario = ? AND contraseña = ?
        """, (usuario, contraseña))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "ok": True,
                "usuario": usuario,
                "rol": row["rol"],
                "nombre": usuario.capitalize()
            }
        else:
            return {"ok": False, "mensaje": "Usuario o contraseña incorrectos"}