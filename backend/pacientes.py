from backend.database import conectar
from backend.auth import Auth
import datetime
import os
import pandas as pd
import numpy as np

auth = Auth()

class Pacientes:

    def guardar(self, nombre, edad, telefono, sexo='', correo='', direccion='',
                observaciones='', fecha_nacimiento=''):
        if not nombre or not edad or not telefono:
            return {"ok": False, "error": "Nombre, edad y teléfono son obligatorios"}

        fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO pacientes (
                    nombre, edad, telefono, sexo, correo, direccion,
                    observaciones, fecha_nacimiento, fecha_registro
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre, edad, telefono, sexo, correo, direccion,
                observaciones, fecha_nacimiento, fecha_registro
            ))

            conn.commit()

            return {
                "ok": True,
                "id": cursor.lastrowid
            }

        except Exception as e:
            print("Error al guardar paciente:", e)
            conn.rollback()

            return {
                "ok": False,
                "error": str(e)
            }

        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nombre, edad, telefono, sexo, correo, direccion,
                   observaciones, fecha_nacimiento, fecha_registro
            FROM pacientes
            ORDER BY nombre ASC
        """)

        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            if fila.get("fecha_registro"):
                fila["fecha_registro"] = fila["fecha_registro"].strftime("%Y-%m-%d %H:%M:%S")

        return filas

    def obtener_para_select(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nombre
            FROM pacientes
            ORDER BY nombre ASC
        """)

        filas = cursor.fetchall()
        conn.close()

        return filas

    def obtener_por_id(self, paciente_id):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM pacientes
            WHERE id = %s
        """, (paciente_id,))

        row = cursor.fetchone()
        conn.close()

        if row and row.get("fecha_registro"):
            row["fecha_registro"] = row["fecha_registro"].strftime("%Y-%m-%d %H:%M:%S")

        return row if row else None

    def editar(self, paciente_id, nombre, edad, telefono, sexo='', correo='',
               direccion='', observaciones='', fecha_nacimiento=''):

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                UPDATE pacientes
                SET nombre=%s,
                    edad=%s,
                    telefono=%s,
                    sexo=%s,
                    correo=%s,
                    direccion=%s,
                    observaciones=%s,
                    fecha_nacimiento=%s
                WHERE id=%s
            """, (
                nombre, edad, telefono, sexo, correo,
                direccion, observaciones, fecha_nacimiento,
                paciente_id
            ))

            conn.commit()

            return True

        except Exception as e:
            print("Error al editar paciente:", e)
            conn.rollback()

            return False

        finally:
            conn.close()

    def eliminar(self, paciente_id, contrasena_admin):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT contrasena
                FROM usuarios
                WHERE usuario = %s
            """, ("admin",))

            row = cursor.fetchone()

            if not row:
                return {
                    "ok": False,
                    "error": "No existe el usuario admin"
                }

            hash_guardado = row["contrasena"]

            if not auth.verificar_contrasena(contrasena_admin, hash_guardado):
                return {
                    "ok": False,
                    "error": "Contraseña de administrador incorrecta"
                }

            cursor.execute("""
                DELETE FROM pacientes
                WHERE id = %s
            """, (paciente_id,))

            conn.commit()

            return {
                "ok": True
            }

        except Exception as e:
            print("Error al eliminar paciente:", e)

            return {
                "ok": False,
                "error": str(e)
            }

        finally:
            conn.close()

    def respaldar_pacientes(self):
        try:
            pacientes = self.obtener_todos()

            if not pacientes:
                return {
                    "ok": False,
                    "error": "No hay pacientes para respaldar"
                }

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

            return {
                "ok": True,
                "archivo": nombre_archivo
            }

        except Exception as e:
            print("Error en respaldo:", e)

            return {
                "ok": False,
                "error": str(e)
            }

    def restaurar_respaldo(self, ruta_archivo):
        try:
            if not ruta_archivo or not os.path.exists(ruta_archivo):
                return {
                    "ok": False,
                    "error": "El archivo no existe"
                }

            df = pd.read_excel(ruta_archivo)
            df = df.replace({np.nan: None})

            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            contador_nuevos = 0

            for _, row in df.iterrows():

                def get_val(keys_list, default=""):
                    for key in keys_list:
                        if key in row:
                            val = row[key]
                            return str(val).strip() if val is not None else default
                    return default

                nombre = get_val(['nombre', 'Nombre', 'Nombre Completo'])
                telefono = get_val(['telefono', 'Teléfono', 'Telefono'])

                if not nombre or nombre == "None" or not telefono or telefono == "None":
                    continue

                cursor.execute("""
                    SELECT id
                    FROM pacientes
                    WHERE nombre = %s AND telefono = %s
                """, (nombre, telefono))

                if cursor.fetchone():
                    continue

                edad = get_val(['edad', 'Edad'], "0")

                try:
                    edad_int = int(float(edad)) if edad else 0
                except:
                    edad_int = 0

                sexo = get_val(['sexo', 'Sexo'])
                correo = get_val(['correo', 'Correo', 'Correo Electrónico'])
                direccion = get_val(['direccion', 'Dirección', 'Direccion'])
                observaciones = get_val(['observaciones', 'Observaciones', 'Notas'])
                fecha_nac = get_val(['fecha_nacimiento', 'Fecha Nacimiento', 'Nacimiento'])

                fecha_reg = get_val(
                    ['fecha_registro', 'Fecha Registro'],
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                cursor.execute("""
                    INSERT INTO pacientes (
                        nombre, edad, telefono, sexo, correo, direccion,
                        observaciones, fecha_nacimiento, fecha_registro
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nombre, edad_int, telefono, sexo, correo,
                    direccion, observaciones, fecha_nac, fecha_reg
                ))

                contador_nuevos += 1

            conn.commit()
            conn.close()

            return {
                "ok": True,
                "mensaje": f"Se agregaron {contador_nuevos} pacientes nuevos."
            }

        except Exception as e:
            print("Error en restauración:", e)

            if 'conn' in locals():
                conn.close()

            return {
                "ok": False,
                "error": str(e)
            }

    def contar_registrados_hoy(self):
        """Retorna cuántos pacientes se registraron hoy"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM pacientes 
                WHERE DATE(fecha_registro) = CURDATE()
            """)
            resultado = cursor.fetchone()
            return resultado['total'] if resultado else 0
        except Exception as e:
            print("Error contando pacientes hoy:", e)
            return 0
        finally:
            conn.close()

    def obtener_recientes(self, limite=10):
        """Retorna los últimos pacientes registrados"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, nombre, edad, telefono, fecha_registro
                FROM pacientes
                ORDER BY fecha_registro DESC
                LIMIT %s
            """, (limite,))
            return cursor.fetchall()
        except Exception as e:
            print("Error obteniendo pacientes recientes:", e)
            return []
        finally:
            conn.close()

    def obtener_registrados_hoy_lista(self):
        """Retorna solo los pacientes registrados el día de hoy"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, nombre, edad, telefono, fecha_registro
                FROM pacientes
                WHERE DATE(fecha_registro) = CURDATE()
                ORDER BY fecha_registro DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print("Error obteniendo pacientes de hoy:", e)
            return []
        finally:
            conn.close()