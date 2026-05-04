from backend.database import conectar
import datetime


class Citas:
    def registrar(self, paciente_id, fecha, hora, tipo, estado='pendiente', observaciones=''):
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

    def actualizar(self, cita_id, tipo=None, estado=None, observaciones=None):
        conn = conectar()
        cursor = conn.cursor()
        try:
            updates = []
            params = []

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

    def contar_citas_hoy(self):
        hoy = datetime.date.today().isoformat()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM citas WHERE fecha = ?
        """, (hoy,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def obtener_citas_hoy(self):
        hoy = datetime.date.today().isoformat()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.id,
                p.nombre AS nombre_paciente,
                c.hora,
                c.tipo,
                c.estado
            FROM citas c
            LEFT JOIN pacientes p ON c.paciente_id = p.id
            WHERE c.fecha = ?
            ORDER BY c.hora ASC
        """, (hoy,))
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]