from backend.database import conectar
 

PARAMETROS_INICIALES = [
    # ── Química Sanguínea 35 Elementos ──────────────────────────────
    ("Glucosa",                      "mg/dL",   "70.00",  "106.00", "Química Sanguínea 35 Elementos", "70.00", "106.00", "70.00", "106.00", ""),
    ("Urea",                         "mg/dL",   "15.00",  "45.00",  "Química Sanguínea 35 Elementos", "15.00", "45.00",  "15.00", "45.00",  ""),
    ("Nitrógeno Ureico",             "mg/dL",   "7.00",   "23.00",  "Química Sanguínea 35 Elementos", "7.00",  "23.00",  "7.00",  "23.00",  ""),
    ("Creatinina",                   "mg/dL",   "0.60",   "1.32",   "Química Sanguínea 35 Elementos", "0.70",  "1.32",   "0.60",  "1.13",   ""),
    ("Relación NU/Creatinina",       "Radio",   "12.00",  "30.00",  "Química Sanguínea 35 Elementos", "12.00", "30.00",  "12.00", "30.00",  ""),
    ("Ácido Úrico",                  "mg/dL",   "2.60",   "7.20",   "Química Sanguínea 35 Elementos", "3.50",  "7.20",   "2.60",  "6.00",   ""),
    ("Colesterol Total",             "mg/dL",   "",       "200.00", "Química Sanguínea 35 Elementos", "",      "200.00", "",      "200.00", "< 200.00"),
    ("Colesterol HDL",               "mg/dL",   "35.00",  "85.00",  "Química Sanguínea 35 Elementos", "35.00", "70.00",  "45.00", "85.00",  ""),
    ("Colesterol LDL",               "mg/dL",   "",       "130.00", "Química Sanguínea 35 Elementos", "",      "130.00", "",      "130.00", "< 130.00"),
    ("Colesterol VLDL",              "mg/dL",   "5.00",   "40.00",  "Química Sanguínea 35 Elementos", "7.00",  "40.00",  "5.00",  "37.00",  ""),
    ("Triglicéridos",                "mg/dL",   "35.00",  "160.00", "Química Sanguínea 35 Elementos", "40.00", "160.00", "35.00", "135.00", ""),
    ("Indice Aterogénico",           "Radio",   "",       "5.00",   "Química Sanguínea 35 Elementos", "",      "5.00",   "",      "5.00",   "< 5.00"),
    ("Bilirrubina Total",            "mg/dL",   "0.20",   "1.20",   "Química Sanguínea 35 Elementos", "0.20",  "1.20",   "0.20",  "1.20",   ""),
    ("Bilirrubina Directa",          "mg/dL",   "",       "0.50",   "Química Sanguínea 35 Elementos", "",      "0.50",   "",      "0.50",   "< 0.50"),
    ("Bilirrubina Indirecta",        "mg/dL",   "0.00",   "1.00",   "Química Sanguínea 35 Elementos", "0.00",  "1.00",   "0.00",  "1.00",   ""),
    ("Fosfatasa Alcalina (ALP)",     "U/L",     "40.00",  "150.00", "Química Sanguínea 35 Elementos", "40.00", "150.00", "40.00", "150.00", ""),
    ("AST / TGO",                    "U/L",     "5.00",   "34.00",  "Química Sanguínea 35 Elementos", "5.00",  "34.00",  "5.00",  "34.00",  ""),
    ("ALT / TGP",                    "U/L",     "0.00",   "55.00",  "Química Sanguínea 35 Elementos", "0.00",  "55.00",  "0.00",  "55.00",  ""),
    ("GGT",                          "U/L",     "",       "",       "Química Sanguínea 35 Elementos", "",      "55.00",  "",      "38.00",  "Hasta 55 masc / Hasta 38 fem"),
    ("Deshidrogenasa Láctica (DHL)", "U/L",     "125.00", "220.00", "Química Sanguínea 35 Elementos", "125.00","220.00", "125.00","220.00", ""),
    ("Proteínas Totales",            "gr/dL",   "6.40",   "8.30",   "Química Sanguínea 35 Elementos", "6.40",  "8.30",   "6.40",  "8.30",   ""),
    ("Albúmina",                     "gr/dL",   "3.50",   "5.20",   "Química Sanguínea 35 Elementos", "3.50",  "5.20",   "3.50",  "5.20",   ""),
    ("Globulinas",                   "gr/dL",   "2.30",   "3.40",   "Química Sanguínea 35 Elementos", "2.30",  "3.40",   "2.30",  "3.40",   ""),
    ("Relación Albúmina/Globulinas", "Radio",   "1.00",   "2.00",   "Química Sanguínea 35 Elementos", "1.00",  "2.00",   "1.00",  "2.00",   ""),
    ("Amilasa en Suero",             "U/L",     "25.00",  "125.00", "Química Sanguínea 35 Elementos", "25.00", "125.00", "25.00", "125.00", ""),
    ("Hierro Sérico",                "ug/dL",   "50.00",  "170.00", "Química Sanguínea 35 Elementos", "50.00", "170.00", "50.00", "170.00", ""),
    ("Capacidad Fijación Hierro",    "ug/dL",   "250.00", "450.00", "Química Sanguínea 35 Elementos", "250.00","450.00", "250.00","450.00", ""),
    ("% de Saturación",              "%",       "20.00",  "50.00",  "Química Sanguínea 35 Elementos", "20.00", "50.00",  "20.00", "50.00",  ""),
    ("Calcio (Ca)",                  "mg/dL",   "8.50",   "10.50",  "Química Sanguínea 35 Elementos", "8.50",  "10.50",  "8.50",  "10.50",  ""),
    ("Cloro (Cl)",                   "mEq/L",   "95.00",  "115.00", "Química Sanguínea 35 Elementos", "95.00", "115.00", "95.00", "115.00", ""),
    ("Fósforo (P)",                  "mg/dL",   "2.50",   "5.00",   "Química Sanguínea 35 Elementos", "2.50",  "5.00",   "2.50",  "5.00",   ""),
    ("Magnesio (Mg)",                "mg/dL",   "1.60",   "3.00",   "Química Sanguínea 35 Elementos", "1.60",  "3.00",   "1.60",  "3.00",   ""),
    ("Potasio (K)",                  "mEq/L",   "3.40",   "5.30",   "Química Sanguínea 35 Elementos", "3.40",  "5.30",   "3.40",  "5.30",   ""),
    ("Sodio (Na)",                   "mEq/L",   "135.00", "155.00", "Química Sanguínea 35 Elementos", "135.00","155.00", "135.00","155.00", ""),
    ("Inmunoglobulina G (IgG)",      "mg/dL",   "552.00", "1631.00","Química Sanguínea 35 Elementos", "552.00","1631.00","552.00","1631.00",""),
    ("Inmunoglobulina A (IgA)",      "mg/dL",   "65.00",  "421.00", "Química Sanguínea 35 Elementos", "65.00", "421.00", "65.00", "421.00", ""),
    ("Inmunoglobulina M (IgM)",      "mg/dL",   "33.00",  "293.00", "Química Sanguínea 35 Elementos", "33.00", "293.00", "33.00", "293.00", ""),
    ("Proteína C Reactiva",          "mg/dL",   "0.00",   "0.50",   "Química Sanguínea 35 Elementos", "0.00",  "0.50",   "0.00",  "0.50",   ""),
 
    # ── Perfil Lipídico ─────────────────────────────────────────────
    ("Colesterol Total",             "mg/dL",   "",       "200.00", "Perfil Lipídico",  "",      "200.00", "",      "200.00", "< 200.00"),
    ("Triglicéridos",                "mg/dL",   "",       "150.00", "Perfil Lipídico",  "",      "150.00", "",      "150.00", "< 150.00"),
    ("Colesterol HDL",               "mg/dL",   "40.00",  "85.00",  "Perfil Lipídico",  "40.00", "",       "50.00", "",       "> 40 masc / > 50 fem"),
    ("Colesterol LDL",               "mg/dL",   "",       "130.00", "Perfil Lipídico",  "",      "130.00", "",      "130.00", "< 130.00"),
 
    # ── Citometría Hemática Completa ────────────────────────────────
    ("Hemoglobina",                  "g/dL",    "12.0",   "17.5",   "Citometría Hemática Completa", "13.5", "17.5", "12.0", "15.5", ""),
    ("Hematocrito",                  "%",       "36",     "53",     "Citometría Hemática Completa", "41",   "53",   "36",   "46",   ""),
    ("Leucocitos",                   "10^3/µL", "4.5",    "11.0",   "Citometría Hemática Completa", "4.5",  "11.0", "4.5",  "11.0", ""),
    ("Plaquetas",                    "10^3/µL", "150",    "450",    "Citometría Hemática Completa", "150",  "450",  "150",  "450",  ""),
]
 
 
class Parametros:
 
    def sembrar_datos_iniciales(self):
        """Inserta los parámetros predefinidos si la tabla está vacía."""
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM parametros")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.executemany("""
                    INSERT INTO parametros
                        (nombre, unidades, valor_referencia_min, valor_referencia_max,
                         tipo_estudio, rango_hombre_min, rango_hombre_max,
                         rango_mujer_min, rango_mujer_max, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, PARAMETROS_INICIALES)
                conn.commit()
                print(f" {len(PARAMETROS_INICIALES)} parámetros iniciales insertados.")
            else:
                print(f"ℹ  Tabla parametros ya tiene {count} registros, no se sembraron datos.")
        except Exception as e:
            conn.rollback()
            print("Error al sembrar parámetros:", e)
        finally:
            conn.close()
 
    def obtener_todos(self):
        conn = conectar()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM parametros ORDER BY tipo_estudio, nombre")
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            conn.close()
 
    def agregar(self, nombre, unidades, valor_referencia_min, valor_referencia_max,
                tipo_estudio, rango_hombre_min='', rango_hombre_max='',
                rango_mujer_min='', rango_mujer_max='', observaciones=''):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parametros
                    (nombre, unidades, valor_referencia_min, valor_referencia_max,
                     tipo_estudio, rango_hombre_min, rango_hombre_max,
                     rango_mujer_min, rango_mujer_max, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, unidades, valor_referencia_min, valor_referencia_max,
                  tipo_estudio, rango_hombre_min, rango_hombre_max,
                  rango_mujer_min, rango_mujer_max, observaciones))
            conn.commit()
            return {"ok": True, "id": cursor.lastrowid}
        except Exception as e:
            conn.rollback()
            return {"ok": False, "error": str(e)}
        finally:
            conn.close()
 
    def editar(self, parametro_id, nombre, unidades, valor_referencia_min, valor_referencia_max,
               tipo_estudio, rango_hombre_min='', rango_hombre_max='',
               rango_mujer_min='', rango_mujer_max='', observaciones=''):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE parametros SET
                    nombre = %s, unidades = %s,
                    valor_referencia_min = %s, valor_referencia_max = %s,
                    tipo_estudio = %s,
                    rango_hombre_min = %s, rango_hombre_max = %s,
                    rango_mujer_min = %s, rango_mujer_max = %s,
                    observaciones = %s
                WHERE id = %s
            """, (nombre, unidades, valor_referencia_min, valor_referencia_max,
                  tipo_estudio, rango_hombre_min, rango_hombre_max,
                  rango_mujer_min, rango_mujer_max, observaciones, parametro_id))
            conn.commit()
            return {"ok": True}
        except Exception as e:
            conn.rollback()
            return {"ok": False, "error": str(e)}
        finally:
            conn.close()
 
    def eliminar(self, parametro_id):
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM parametros WHERE id = %s", (parametro_id,))
            conn.commit()
            return {"ok": True}
        except Exception as e:
            conn.rollback()
            return {"ok": False, "error": str(e)}
        finally:
            conn.close()
 
    def obtener_por_tipo(self, tipo_estudio):
        conn = conectar()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM parametros WHERE tipo_estudio = %s ORDER BY nombre", (tipo_estudio,))
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            conn.close()
 