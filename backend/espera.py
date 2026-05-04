from backend.database import conectar
import datetime

class Espera:
    def registrar(self, nombre='', fecha_nacimiento='', edad=None, telefono='', fecha_cita='', hora_cita='', tipo_estudio='', observaciones=''):
        if not fecha_cita or not hora_cita:
            return None

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO espera (
                    nombre, fecha_nacimiento, edad, telefono, fecha_cita, hora_cita, 
                    tipo_estudio, observaciones, fecha_registro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, fecha_nacimiento, edad, telefono, fecha_cita, hora_cita, 
                  tipo_estudio or "Pendiente", observaciones, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al registrar en espera:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM espera 
            WHERE procesado = 0 
            ORDER BY fecha_registro DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]

    def actualizar(self, espera_id, nombre, fecha_nacimiento, edad, telefono, observaciones):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE espera 
                SET nombre=?, fecha_nacimiento=?, edad=?, telefono=?, observaciones=?
                WHERE id=?
            """, (nombre, fecha_nacimiento, edad, telefono, observaciones, espera_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar espera:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def marcar_procesado(self, espera_id):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE espera SET procesado = 1, estado = 'procesado' WHERE id = ?", (espera_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al marcar como procesado:", e)
            conn.rollback()
            return False
        finally:
            conn.close()