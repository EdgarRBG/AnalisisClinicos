from backend.database import conectar
from backend.auth import Auth
import datetime
import os
import pandas as pd

auth = Auth()

class Pacientes:

    def guardar(self, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones='', fecha_nacimiento=''):
        if not nombre or not edad or not telefono:
            return {"ok": False, "error": "Nombre, edad y teléfono son obligatorios"}

        fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pacientes (nombre, edad, telefono, sexo, correo, direccion, 
                                     observaciones, fecha_nacimiento, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_nacimiento, fecha_registro))
            conn.commit()
            return {"ok": True, "id": cursor.lastrowid}
        except Exception as e:
            print("Error al guardar paciente:", e)
            conn.rollback()
            return {"ok": False, "error": str(e)}
        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, edad, telefono, sexo, correo, direccion, 
                   observaciones, fecha_nacimiento, fecha_registro 
            FROM pacientes 
            ORDER BY nombre ASC
        """)
        filas = cursor.fetchall()
        conn.close()
        return [dict(f) for f in filas]

    def obtener_para_select(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]

    def obtener_por_id(self, paciente_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def editar(self, paciente_id, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones='', fecha_nacimiento=''):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE pacientes 
                SET nombre=?, edad=?, telefono=?, sexo=?, correo=?, direccion=?, 
                    observaciones=?, fecha_nacimiento=? 
                WHERE id=?
            """, (nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_nacimiento, paciente_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error al editar paciente:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    # 🔥 AQUÍ ESTÁ LA PARTE IMPORTANTE
    def eliminar(self, paciente_id, contrasena_admin):
        conn = conectar()
        cursor = conn.cursor()
        try:
            # Verificar contraseña del admin
            cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", ("admin",))
            row = cursor.fetchone()

            if not row:
                return {"ok": False, "error": "No existe el usuario admin"}

            hash_guardado = row["contrasena"]

            if not auth.verificar_contrasena(contrasena_admin, hash_guardado):
                return {"ok": False, "error": "Contraseña de administrador incorrecta"}

            # Si la contraseña es correcta, eliminar
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
            conn.commit()

            return {"ok": True}

        except Exception as e:
            print("Error al eliminar paciente:", e)
            return {"ok": False, "error": str(e)}
        finally:
            conn.close()

    def respaldar_pacientes(self):
        try:
            pacientes = self.obtener_todos()
            if not pacientes:
                return {"ok": False, "error": "No hay pacientes para respaldar"}

            ruta_respaldos = os.path.join(os.getcwd(), "Respaldos")
            os.makedirs(ruta_respaldos, exist_ok=True)

            df = pd.DataFrame(pacientes)
            fecha_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_archivo = f"Respaldo_Pacientes_{fecha_str}.xlsx"
            ruta_final = os.path.join(ruta_respaldos, nombre_archivo)

            df.to_excel(ruta_final, index=False)

            try:
                os.startfile(ruta_respaldos)
            except:
                pass

            return {"ok": True, "archivo": nombre_archivo}
        except Exception as e:
            print("Error en respaldo:", e)
            return {"ok": False, "error": str(e)}

    def restaurar_respaldo(self, ruta_archivo):
        try:
            if not ruta_archivo or not os.path.exists(ruta_archivo):
                return {"ok": False, "error": "El archivo no existe"}

            df = pd.read_excel(ruta_archivo)
            conn = conectar()
            cursor = conn.cursor()
            contador_nuevos = 0

            for _, row in df.iterrows():
                nombre = str(row.get('Nombre Completo', row.get('nombre', ''))).strip()
                telefono = str(row.get('Teléfono', row.get('telefono', ''))).strip()

                if not nombre or not telefono:
                    continue

                cursor.execute("SELECT id FROM pacientes WHERE nombre = ? AND telefono = ?", (nombre, telefono))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO pacientes (nombre, edad, telefono, sexo, correo, direccion, 
                                         observaciones, fecha_nacimiento, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nombre,
                    int(row.get('Edad', row.get('edad', 0))),
                    telefono,
                    str(row.get('Sexo', '')),
                    str(row.get('Correo', '')),
                    str(row.get('Dirección', '')),
                    str(row.get('Observaciones', '')),
                    str(row.get('Fecha Nacimiento', '')),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                contador_nuevos += 1

            conn.commit()
            conn.close()
            return {"ok": True, "mensaje": f"Se agregaron {contador_nuevos} pacientes nuevos."}
        except Exception as e:
            print("Error en restauración:", e)
            return {"ok": False, "error": str(e)}