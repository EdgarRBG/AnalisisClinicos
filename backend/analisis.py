
from backend.database import conectar
import datetime
import random
import string

class Analisis:
    def generar_id_muestra(self):
        """Genera un ID único para la muestra (Ej: LAB-A1B2)"""
        letras = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"LAB-{letras}{numeros}"

    def registrar_solicitud(self, paciente_id, cita_id=None, id_muestra=None, medico_solicitante="", tipo_estudio="", observaciones=""):
        if not id_muestra:
            id_muestra = self.generar_id_muestra()
            
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO solicitudes_analisis 
                (paciente_id, cita_id, id_muestra, medico_solicitante, tipo_estudio, observaciones_generales, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'pendiente')
            """, (paciente_id, cita_id, id_muestra, medico_solicitante, tipo_estudio, observaciones))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al registrar solicitud:", e)
            return None
        finally:
            conn.close()

    def obtener_pendientes(self):
        conn = conectar()
        cursor = conn.cursor()
      
        cursor.execute("""
            SELECT s.id, s.id_muestra, s.tipo_estudio, s.fecha_recepcion, p.nombre as paciente_nombre
            FROM solicitudes_analisis s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE s.estado = 'pendiente'
            ORDER BY s.fecha_recepcion DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def obtener_solicitud(self, solicitud_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
           
            cursor.execute("""
                SELECT s.*, p.nombre as paciente_nombre, p.edad as paciente_edad, p.sexo as paciente_sexo
                FROM solicitudes_analisis s
                JOIN pacientes p ON s.paciente_id = p.id
                WHERE s.id = ?
            """, (solicitud_id,))
            solicitud = cursor.fetchone()
            
            if not solicitud:
                return None
                
            cursor.execute("SELECT * FROM resultados_parametros WHERE solicitud_id = ?", (solicitud_id,))
            resultados = cursor.fetchall()
            
            return {
                "solicitud": dict(solicitud),
                "resultados": [dict(r) for r in resultados]
            }
        finally:
            conn.close()

    def agregar_resultado(self, solicitud_id, parametro, resultado, unidades="", valor_referencia="", fuera_de_rango="", observacion=""):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO resultados_parametros 
                (solicitud_id, parametro, resultado, unidades, valor_referencia, fuera_de_rango, observacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (solicitud_id, parametro, resultado, unidades, valor_referencia, fuera_de_rango, observacion))
            conn.commit()
            return True
        except Exception as e:
            print("Error al agregar resultado:", e)
            return False
        finally:
            conn.close()

    def actualizar_estado(self, solicitud_id, estado):
        conn = conectar()
        cursor = conn.cursor()
        try:
            fecha_reporte = None
            if estado == 'finalizado':
                fecha_reporte = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            cursor.execute("""
                UPDATE solicitudes_analisis 
                SET estado = ?, fecha_reporte = ? 
                WHERE id = ?
            """, (estado, fecha_reporte, solicitud_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error al actualizar estado:", e)
            return False
        finally:
            conn.close()

    def obtener_finalizadas(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, p.nombre as paciente_nombre
            FROM solicitudes_analisis s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE s.estado = 'finalizado'
            ORDER BY s.fecha_reporte DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def eliminar_solicitud(self, solicitud_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM solicitudes_analisis WHERE id = ?", (solicitud_id,))
            conn.commit()
            return True
        except Exception as e:
            print("Error al eliminar solicitud:", e)
            return False
        finally:
            conn.close()