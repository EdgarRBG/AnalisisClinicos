from backend.database import conectar
import datetime


class Citas:
    """
    Manejo de citas / órdenes de toma de muestra.
    En un laboratorio, estas suelen ser las citas para extracción de sangre u otras muestras.
    """

    def registrar(self, paciente_id, fecha, hora, tipo, estado='pendiente', observaciones=''):
        """
        Registra una nueva cita/orden para toma de muestra.
        """
        if not paciente_id or not fecha or not hora or not tipo:
            return False

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO citas (
                    paciente_id, fecha, hora, tipo, estado, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente_id, fecha, hora, tipo, estado, observaciones))
            conn.commit()
            return cursor.lastrowid  
        except Exception as e:
            print("Error al registrar cita/orden:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    def obtener_todas(self):
        """
        Obtiene todas las citas con información del paciente.
        """
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.id,
                c.paciente_id,
                c.fecha,
                c.hora,
                c.tipo,
                c.estado,
                c.observaciones,
                p.nombre AS nombre_paciente
            FROM citas c
            LEFT JOIN pacientes p ON c.paciente_id = p.id
            ORDER BY c.fecha DESC, c.hora ASC
        """)
        filas = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row["id"],
                "paciente_id": row["paciente_id"],
                "fecha": row["fecha"],
                "hora": row["hora"],
                "tipo": row["tipo"],
                "estado": row["estado"],
                "observaciones": row["observaciones"] or "",
                "nombre_paciente": row["nombre_paciente"] or "Paciente desconocido"
            }
            for row in filas
        ]

    def obtener_por_id(self, cita_id):
        """
        Obtiene una cita específica por su ID.
        """
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.id,
                c.paciente_id,
                c.fecha,
                c.hora,
                c.tipo,
                c.estado,
                c.observaciones,
                p.nombre AS nombre_paciente
            FROM citas c
            LEFT JOIN pacientes p ON c.paciente_id = p.id
            WHERE c.id = ?
        """, (cita_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row["id"],
                "paciente_id": row["paciente_id"],
                "fecha": row["fecha"],
                "hora": row["hora"],
                "tipo": row["tipo"],
                "estado": row["estado"],
                "observaciones": row["observaciones"] or "",
                "nombre_paciente": row["nombre_paciente"] or "Paciente desconocido"
            }
        return None

    def obtener_por_paciente(self, paciente_id):
        """
        Obtiene todas las citas de un paciente específico.
        """
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.id, c.fecha, c.hora, c.tipo, c.estado, c.observaciones
            FROM citas c
            WHERE c.paciente_id = ?
            ORDER BY c.fecha DESC, c.hora ASC
        """, (paciente_id,))
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]

    def actualizar(self, cita_id, fecha=None, hora=None, tipo=None, estado=None, observaciones=None):
        """
        Actualiza una cita existente.
        Solo actualiza los campos que se envíen (no nulos).
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            updates = []
            params = []

            if fecha is not None:
                updates.append("fecha = ?")
                params.append(fecha)
            if hora is not None:
                updates.append("hora = ?")
                params.append(hora)
            if tipo is not None:
                updates.append("tipo = ?")
                params.append(tipo)
            if estado is not None:
                updates.append("estado = ?")
                params.append(estado)
            if observaciones is not None:
                updates.append("observaciones = ?")
                params.append(observaciones)

            if not updates:
                return False

            params.append(cita_id)
            query = f"UPDATE citas SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar cita:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def eliminar(self, cita_id):
        """
        Elimina una cita por su ID.
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al eliminar cita:", e)
            conn.rollback()
            return False
        finally:
            conn.close()