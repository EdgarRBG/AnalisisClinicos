
from backend.database import conectar
import json

class Bloques:
    def obtener_estudios_disponibles(self):
        """Devuelve la lista de estudios con sus parámetros y valores de referencia diferenciados por sexo"""
        return [
            {
                "id": 1, 
                "nombre": "Química Sanguínea 35 Elementos", 
                "parametros": [
                    {"nombre": "Glucosa", "unidades": "mg/dL", "referencia_masc": "70.00 - 106.00", "referencia_fem": "70.00 - 106.00"},
                    {"nombre": "Urea", "unidades": "mg/dL", "referencia_masc": "15.00 - 45.00", "referencia_fem": "15.00 - 45.00"},
                    {"nombre": "Nitrógeno Ureico", "unidades": "mg/dL", "referencia_masc": "7.00 - 23.00", "referencia_fem": "7.00 - 23.00"},
                    {"nombre": "Creatinina", "unidades": "mg/dL", "referencia_masc": "0.70 - 1.32", "referencia_fem": "0.60 - 1.13"},
                    {"nombre": "Relación NU/Creatinina", "unidades": "Radio", "referencia_masc": "12.00 - 30.00", "referencia_fem": "12.00 - 30.00"},
                    {"nombre": "Ácido Úrico", "unidades": "mg/dL", "referencia_masc": "3.50 - 7.20", "referencia_fem": "2.60 - 6.00"},
                    {"nombre": "Colesterol Total", "unidades": "mg/dL", "referencia_masc": "< 200.00", "referencia_fem": "< 200.00"},
                    {"nombre": "Colesterol HDL", "unidades": "mg/dL", "referencia_masc": "35.00 - 70.00", "referencia_fem": "45.00 - 85.00"},
                    {"nombre": "Colesterol LDL", "unidades": "mg/dL", "referencia_masc": "< 130.00", "referencia_fem": "< 130.00"},
                    {"nombre": "Colesterol VLDL", "unidades": "mg/dL", "referencia_masc": "7.00 - 40.00", "referencia_fem": "5.00 - 37.00"},
                    {"nombre": "Triglicéridos", "unidades": "mg/dL", "referencia_masc": "40.00 - 160.00", "referencia_fem": "35.00 - 135.00"},
                    {"nombre": "Indice Aterogénico", "unidades": "Radio", "referencia_masc": "< 5.00", "referencia_fem": "< 5.00"},
                    {"nombre": "Bilirrubina Total", "unidades": "mg/dL", "referencia_masc": "0.20 - 1.20", "referencia_fem": "0.20 - 1.20"},
                    {"nombre": "Bilirrubina Directa", "unidades": "mg/dL", "referencia_masc": "< 0.50", "referencia_fem": "< 0.50"},
                    {"nombre": "Bilirrubina Indirecta", "unidades": "mg/dL", "referencia_masc": "0.00 - 1.00", "referencia_fem": "0.00 - 1.00"},
                    {"nombre": "Fosfatasa Alcalina (ALP)", "unidades": "U/L", "referencia_masc": "40.00 - 150.00", "referencia_fem": "40.00 - 150.00"},
                    {"nombre": "AST / TGO", "unidades": "U/L", "referencia_masc": "5.00 - 34.00", "referencia_fem": "5.00 - 34.00"},
                    {"nombre": "ALT / TGP", "unidades": "U/L", "referencia_masc": "0.00 - 55.00", "referencia_fem": "0.00 - 55.00"},
                    {"nombre": "GGT", "unidades": "U/L", "referencia_masc": "Hasta 55.00", "referencia_fem": "Hasta 38.00"},
                    {"nombre": "Deshidrogenasa Láctica (DHL)", "unidades": "U/L", "referencia_masc": "125.00 - 220.00", "referencia_fem": "125.00 - 220.00"},
                    {"nombre": "Proteínas Totales", "unidades": "gr/dL", "referencia_masc": "6.40 - 8.30", "referencia_fem": "6.40 - 8.30"},
                    {"nombre": "Albúmina", "unidades": "gr/dL", "referencia_masc": "3.50 - 5.20", "referencia_fem": "3.50 - 5.20"},
                    {"nombre": "Globulinas", "unidades": "gr/dL", "referencia_masc": "2.30 - 3.40", "referencia_fem": "2.30 - 3.40"},
                    {"nombre": "Relación Albúmina/Globulinas", "unidades": "Radio", "referencia_masc": "1.00 - 2.00", "referencia_fem": "1.00 - 2.00"},
                    {"nombre": "Amilasa en Suero", "unidades": "U/L", "referencia_masc": "25.00 - 125.00", "referencia_fem": "25.00 - 125.00"},
                    {"nombre": "Hierro Sérico", "unidades": "ug/dL", "referencia_masc": "50.00 - 170.00", "referencia_fem": "50.00 - 170.00"},
                    {"nombre": "Capacidad Fijación Hierro", "unidades": "ug/dL", "referencia_masc": "250.00 - 450.00", "referencia_fem": "250.00 - 450.00"},
                    {"nombre": "% de Saturación", "unidades": "%", "referencia_masc": "20.00 - 50.00", "referencia_fem": "20.00 - 50.00"},
                    {"nombre": "Calcio (Ca)", "unidades": "mg/dL", "referencia_masc": "8.50 - 10.50", "referencia_fem": "8.50 - 10.50"},
                    {"nombre": "Cloro (Cl)", "unidades": "mEq/L", "referencia_masc": "95.00 - 115.00", "referencia_fem": "95.00 - 115.00"},
                    {"nombre": "Fósforo (P)", "unidades": "mg/dL", "referencia_masc": "2.50 - 5.00", "referencia_fem": "2.50 - 5.00"},
                    {"nombre": "Magnesio (Mg)", "unidades": "mg/dL", "referencia_masc": "1.60 - 3.00", "referencia_fem": "1.60 - 3.00"},
                    {"nombre": "Potasio (K)", "unidades": "mEq/L", "referencia_masc": "3.40 - 5.30", "referencia_fem": "3.40 - 5.30"},
                    {"nombre": "Sodio (Na)", "unidades": "mEq/L", "referencia_masc": "135.00 - 155.00", "referencia_fem": "135.00 - 155.00"},
                    {"nombre": "Inmunoglobulina G (IgG)", "unidades": "mg/dL", "referencia_masc": "552.00 - 1631.00", "referencia_fem": "552.00 - 1631.00"},
                    {"nombre": "Inmunoglobulina A (IgA)", "unidades": "mg/dL", "referencia_masc": "65.00 - 421.00", "referencia_fem": "65.00 - 421.00"},
                    {"nombre": "Inmunoglobulina M (IgM)", "unidades": "mg/dL", "referencia_masc": "33.00 - 293.00", "referencia_fem": "33.00 - 293.00"},
                    {"nombre": "Proteína C Reactiva", "unidades": "mg/dL", "referencia_masc": "0.00 - 0.50", "referencia_fem": "0.00 - 0.50"}
                ]
            },
            {
                "id": 2, 
                "nombre": "Perfil Lipídico",
                "parametros": [
                    {"nombre": "Colesterol Total", "unidades": "mg/dL", "referencia_masc": "< 200.00", "referencia_fem": "< 200.00"},
                    {"nombre": "Triglicéridos", "unidades": "mg/dL", "referencia_masc": "< 150.00", "referencia_fem": "< 150.00"},
                    {"nombre": "Colesterol HDL", "unidades": "mg/dL", "referencia_masc": "> 40.00", "referencia_fem": "> 50.00"},
                    {"nombre": "Colesterol LDL", "unidades": "mg/dL", "referencia_masc": "< 130.00", "referencia_fem": "< 130.00"}
                ]
            },
            {
                "id": 4, 
                "nombre": "Citometría Hemática Completa",
                "parametros": [
                    {"nombre": "Hemoglobina", "unidades": "g/dL", "referencia_masc": "13.5 - 17.5", "referencia_fem": "12.0 - 15.5"},
                    {"nombre": "Hematocrito", "unidades": "%", "referencia_masc": "41 - 53", "referencia_fem": "36 - 46"},
                    {"nombre": "Leucocitos", "unidades": "10^3/µL", "referencia_masc": "4.5 - 11.0", "referencia_fem": "4.5 - 11.0"},
                    {"nombre": "Plaquetas", "unidades": "10^3/µL", "referencia_masc": "150 - 450", "referencia_fem": "150 - 450"}
                ]
            }
        ]

    def guardar_bloques_solicitud(self, solicitud_id, bloques_json):
        """Guarda los bloques seleccionados para una solicitud"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE solicitudes_analisis 
                SET observaciones_generales = ?
                WHERE id = ?
            """, (bloques_json, solicitud_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error al guardar bloques:", e)
            return False
        finally:
            conn.close()