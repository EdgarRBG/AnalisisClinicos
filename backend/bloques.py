from backend.database import conectar
import json

class Bloques:
    def obtener_estudios_disponibles(self):
        """Lee bloques y parámetros desde la base de datos."""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            # Obtener todos los tipos de estudio únicos
            cursor.execute("""
                SELECT DISTINCT tipo_estudio
                FROM parametros
                WHERE tipo_estudio IS NOT NULL AND tipo_estudio != ''
                ORDER BY tipo_estudio
            """)
            tipos = [row['tipo_estudio'] for row in cursor.fetchall()]

            estudios = []
            for i, tipo in enumerate(tipos):
                cursor.execute("""
                    SELECT nombre, unidades,
                           valor_referencia_min, valor_referencia_max,
                           rango_hombre_min, rango_hombre_max,
                           rango_mujer_min, rango_mujer_max
                    FROM parametros
                    WHERE tipo_estudio = %s
                    ORDER BY nombre
                """, (tipo,))
                params = cursor.fetchall()

                parametros_lista = []
                for p in params:
                    ref_masc = f"{p['rango_hombre_min']} - {p['rango_hombre_max']}" if p['rango_hombre_min'] else f"{p['valor_referencia_min']} - {p['valor_referencia_max']}"
                    ref_fem  = f"{p['rango_mujer_min']} - {p['rango_mujer_max']}" if p['rango_mujer_min'] else f"{p['valor_referencia_min']} - {p['valor_referencia_max']}"
                    parametros_lista.append({
                        "nombre":          p['nombre'],
                        "unidades":        p['unidades'] or '',
                        "referencia_masc": ref_masc or '',
                        "referencia_fem":  ref_fem  or '',
                    })

                estudios.append({
                    "id":         i + 1,
                    "nombre":     tipo,
                    "parametros": parametros_lista
                })

            return estudios
        except Exception as e:
            print("Error en obtener_estudios_disponibles:", e)
            return []
        finally:
            conn.close()

        def guardar_bloques_solicitud(self, solicitud_id, bloques_json):
        """Guarda los bloques seleccionados para una solicitud"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                UPDATE solicitudes_analisis
                SET observaciones_generales = %s
                WHERE id = %s
            """, (bloques_json, solicitud_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error al guardar bloques:", e)
            return False
        finally:
            conn.close()