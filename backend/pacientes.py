from backend.database import conectar
import datetime


class Pacientes:

    def guardar(self, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones=''):
        """
        Registra un nuevo paciente.
        """
        if not nombre or not edad or not telefono:
            return None

        fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pacientes (
                    nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_registro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_registro))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al guardar paciente:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_registro 
            FROM pacientes
            ORDER BY nombre ASC
        """)
        filas = cursor.fetchall()
        conn.close()

        return [
            {
                "id": f["id"],
                "nombre": f["nombre"],
                "edad": f["edad"],
                "telefono": f["telefono"],
                "sexo": f["sexo"],
                "correo": f["correo"],
                "direccion": f["direccion"],
                "observaciones": f["observaciones"] or "",
                "fecha_registro": f["fecha_registro"]
            }
            for f in filas
        ]

    def obtener_para_select(self):
        """Devuelve lista simple para usar en <select> (id, nombre)"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
        filas = cursor.fetchall()
        conn.close()
        return [(row["id"], row["nombre"]) for row in filas]

    def obtener_por_id(self, paciente_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM pacientes WHERE id = ?
        """, (paciente_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def buscar_por_nombre_o_telefono(self, texto):
        """Búsqueda rápida por nombre o teléfono (LIKE)"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, telefono, edad 
            FROM pacientes 
            WHERE nombre LIKE ? OR telefono LIKE ?
            ORDER BY nombre ASC
            LIMIT 20
        """, (f"%{texto}%", f"%{texto}%"))
        filas = cursor.fetchall()
        conn.close()
        return [dict(row) for row in filas]

    def editar(self, paciente_id, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones=''):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE pacientes 
                SET nombre=?, edad=?, telefono=?, sexo=?, correo=?, direccion=?, observaciones=?
                WHERE id=?
            """, (nombre, edad, telefono, sexo, correo, direccion, observaciones, paciente_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al editar paciente:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    def eliminar(self, paciente_id):
        """
        Elimina paciente y en cascada elimina citas y solicitudes relacionadas (por FK)
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar paciente {paciente_id}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()