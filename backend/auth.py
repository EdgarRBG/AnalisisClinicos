from backend.database import conectar

class Auth:
    def validar_login(self, usuario, contrasena):
        print("LOGIN LLAMADO DESDE FRONTEND")
        print(f"Usuario: '{usuario}' (tipo: {type(usuario)}, len: {len(usuario)})")
        print(f"Contrasena: '{contrasena}' (tipo: {type(contrasena)}, len: {len(contrasena)})")

        try:
            conn = conectar()
            print("Conexión a BD abierta OK")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rol FROM usuarios 
                WHERE usuario = ? AND contrasena = ?
            """, (usuario, contrasena))
            row = cursor.fetchone()
            print(f"Resultado de consulta: {row}")
            conn.close()
            print("Conexión cerrada")

            if row:
                print("LOGIN EXITOSO")
                return {
                    "ok": True,
                    "usuario": usuario,
                    "rol": row["rol"],
                    "nombre": usuario.capitalize()
                }
            else:
                print("No coincidencia en BD")
                return {"ok": False, "mensaje": "Usuario o contraseña incorrectos"}
        except Exception as e:
            print("ERROR EN LOGIN:", str(e))
            return {"ok": False, "mensaje": "Error interno en el servidor"}