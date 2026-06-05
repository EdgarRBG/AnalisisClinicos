import bcrypt

class Auth:

    def validar_login(self, usuario, contrasena):
        from backend.database import conectar  
        conn = conectar()
        cursor = conn.cursor(dictionary=True)   
        try:
            cursor.execute(
                "SELECT contrasena, rol FROM usuarios WHERE usuario = %s",
                (usuario,)
            )
            row = cursor.fetchone()

            if not row:
                return {"ok": False, "mensaje": "Usuario o contraseña incorrectos"}

            contrasena_hash = row["contrasena"]
            rol = row["rol"]

            if bcrypt.checkpw(contrasena.encode("utf-8"), contrasena_hash.encode("utf-8")):
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
        return bcrypt.hashpw(contrasena.encode("utf-8"), salt).decode("utf-8")

    def verificar_contrasena(self, contrasena_ingresada, hash_guardado):
        try:
            return bcrypt.checkpw(
                contrasena_ingresada.encode("utf-8"),
                hash_guardado.encode("utf-8"),
            )
        except Exception as e:
            print("Error al verificar contraseña:", e)
            return False