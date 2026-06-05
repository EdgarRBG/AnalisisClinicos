from backend.database import conectar
import datetime
import random
import string

class Analisis:

    def generar_id_muestra(self):
        letras = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"LAB-{letras}{numeros}"

    def registrar_solicitud(self, paciente_id, cita_id=None, id_muestra=None,
                            medico_solicitante="", tipo_estudio="", observaciones=""):

        if not id_muestra:
            id_muestra = self.generar_id_muestra()

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO solicitudes_analisis
                (
                    paciente_id,
                    cita_id,
                    id_muestra,
                    medico_solicitante,
                    tipo_estudio,
                    observaciones_generales,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
            """, (
                paciente_id,
                cita_id,
                id_muestra,
                medico_solicitante,
                tipo_estudio,
                observaciones
            ))

            conn.commit()

            return cursor.lastrowid

        except Exception as e:
            print("Error al registrar solicitud:", e)
            return None

        finally:
            conn.close()

    def obtener_pendientes(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT s.id,
                   s.id_muestra,
                   s.tipo_estudio,
                   s.fecha_recepcion,
                   p.nombre as paciente_nombre
            FROM solicitudes_analisis s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE s.estado IN ('pendiente', 'en_proceso')
            ORDER BY s.fecha_recepcion DESC
        """)

        rows = cursor.fetchall()
        conn.close()

       
        for row in rows:
            if row.get("fecha_recepcion"):
                row["fecha_recepcion"] = row["fecha_recepcion"].strftime("%Y-%m-%d %H:%M:%S")

        return rows

    def obtener_solicitud(self, solicitud_id):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT s.*,
                p.nombre           AS paciente_nombre,
                p.edad             AS paciente_edad,
                p.sexo             AS paciente_sexo,
                p.fecha_nacimiento AS paciente_fecha_nacimiento
                FROM solicitudes_analisis s
                JOIN pacientes p ON s.paciente_id = p.id
                WHERE s.id = %s
            """, (solicitud_id,))

            solicitud = cursor.fetchone()

            if not solicitud:
                return None

            cursor.execute("""
                SELECT *
                FROM resultados_parametros
                WHERE solicitud_id = %s
            """, (solicitud_id,))

            resultados = cursor.fetchall()

         
            if solicitud.get("fecha_recepcion"):
                solicitud["fecha_recepcion"] = solicitud["fecha_recepcion"].strftime("%Y-%m-%d %H:%M:%S")

            if solicitud.get("fecha_reporte"):
                solicitud["fecha_reporte"] = solicitud["fecha_reporte"].strftime("%Y-%m-%d %H:%M:%S")

            if solicitud.get("fecha_creacion"):
                solicitud["fecha_creacion"] = solicitud["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")

            return {
                "solicitud": solicitud,
                "resultados": resultados
            }

        finally:
            conn.close()

    def agregar_resultado(self, solicitud_id, parametro, resultado,
                          unidades="", valor_referencia="",
                          fuera_de_rango="", observacion=""):

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO resultados_parametros
                (
                    solicitud_id,
                    parametro,
                    resultado,
                    unidades,
                    valor_referencia,
                    fuera_de_rango,
                    observacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                solicitud_id,
                parametro,
                resultado,
                unidades,
                valor_referencia,
                fuera_de_rango,
                observacion
            ))

            conn.commit()

            return True

        except Exception as e:
            print("Error al agregar resultado:", e)
            return False

        finally:
            conn.close()

    def agregar_resultado_analisis(self, *args, **kwargs):
        return self.agregar_resultado(*args, **kwargs)

    def actualizar_estado(self, solicitud_id, estado):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            fecha_reporte = None

            if estado == 'finalizado':
                fecha_reporte = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                UPDATE solicitudes_analisis
                SET estado = %s,
                    fecha_reporte = %s
                WHERE id = %s
            """, (
                estado,
                fecha_reporte,
                solicitud_id
            ))

            conn.commit()

            return True

        except Exception as e:
            print("Error al actualizar estado:", e)
            return False

        finally:
            conn.close()

    def actualizar_estado_solicitud(self, *args, **kwargs):
        return self.actualizar_estado(*args, **kwargs)

    def actualizar_medico(self, solicitud_id, medico_solicitante):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                UPDATE solicitudes_analisis
                SET medico_solicitante = %s
                WHERE id = %s
            """, (
                medico_solicitante,
                solicitud_id
            ))

            conn.commit()

            return True

        except Exception as e:
            print("Error al actualizar médico:", e)
            return False

        finally:
            conn.close()

    def actualizar_medico_solicitud(self, *args, **kwargs):
        return self.actualizar_medico(*args, **kwargs)

    def marcar_procesado(self, espera_id):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                UPDATE espera
                SET procesado = 1
                WHERE id = %s
            """, (espera_id,))

            conn.commit()

            return True

        except Exception as e:
            print("Error al marcar procesado:", e)
            return False

        finally:
            conn.close()

    def marcar_procesado_js(self, espera_id):
        return self.marcar_procesado(espera_id)

    def eliminar_cita(self, cita_id):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                DELETE FROM citas
                WHERE id = %s
            """, (cita_id,))

            conn.commit()

            return True

        except Exception as e:
            print("Error al eliminar cita:", e)
            return False

        finally:
            conn.close()

    def obtener_finalizadas(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT s.*,
                   p.nombre AS paciente_nombre
            FROM solicitudes_analisis s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE s.estado = 'finalizado'
            ORDER BY s.fecha_reporte DESC
        """)

        rows = cursor.fetchall()
        conn.close()

    
        for row in rows:

            if row.get("fecha_recepcion"):
                row["fecha_recepcion"] = row["fecha_recepcion"].strftime("%Y-%m-%d %H:%M:%S")

            if row.get("fecha_reporte"):
                row["fecha_reporte"] = row["fecha_reporte"].strftime("%Y-%m-%d %H:%M:%S")

            if row.get("fecha_creacion"):
                row["fecha_creacion"] = row["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")

        return rows

    def obtener_solicitudes_finalizadas(self):
        return self.obtener_finalizadas()

    def eliminar_solicitud(self, solicitud_id):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                DELETE FROM resultados_parametros
                WHERE solicitud_id = %s
            """, (solicitud_id,))

            cursor.execute("""
                DELETE FROM solicitudes_analisis
                WHERE id = %s
            """, (solicitud_id,))

            conn.commit()

            return True

        except Exception as e:
            print("Error al eliminar solicitud:", e)
            return False

        finally:
            conn.close()

    def contar_pendientes(self):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM solicitudes_analisis WHERE estado = 'pendiente'")
            return cursor.fetchone()[0]
        except Exception as e:
            print("Error al contar pendientes:", e)
            return 0
        finally:
            conn.close()

    def obtener_finalizadas_hoy(self):
        conn = conectar()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.id, s.id_muestra, s.tipo_estudio, s.estado,
                       p.nombre AS paciente
                FROM solicitudes_analisis s
                JOIN pacientes p ON s.paciente_id = p.id
                WHERE s.estado = 'finalizado'
                  AND DATE(s.fecha_reporte) = CURDATE()
            """)
            return cursor.fetchall()
        except Exception as e:
            print("Error al obtener finalizadas hoy:", e)
            return []
        finally:
            conn.close()