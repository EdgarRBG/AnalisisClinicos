import sqlite3
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "sistema_laboratorio.db")

print("Usando base de datos en:", DB_PATH)
print("Directorio actual:", os.getcwd())

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def crear_tablas():
    print("Iniciando creación de tablas...")

    conn = None
    try:
        conn = conectar()
        print("Conexión a BD abierta exitosamente.")
        cursor = conn.cursor()

        print("Creando tabla pacientes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                telefono TEXT NOT NULL,
                sexo TEXT,
                correo TEXT,
                direccion TEXT,
                observaciones TEXT,
                fecha_registro TEXT DEFAULT (datetime('now'))
            )
        """)
        print("Tabla pacientes OK")

        print("Creando tabla citas...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT DEFAULT '',
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            )
        """)
        print("Tabla citas OK")

        print("Creando tabla solicitudes_analisis...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_analisis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                cita_id INTEGER,
                id_muestra TEXT UNIQUE NOT NULL,
                fecha_recepcion TEXT NOT NULL DEFAULT (datetime('now')),
                fecha_reporte TEXT,
                medico_solicitante TEXT,
                tipo_estudio TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                observaciones_generales TEXT,
                creado_por TEXT,
                fecha_creacion TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
                FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE SET NULL
            )
        """)
        print("Tabla solicitudes_analisis OK")

        print("Creando tabla resultados_parametros...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_parametros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitud_id INTEGER NOT NULL,
                parametro TEXT NOT NULL,
                resultado REAL,
                unidades TEXT,
                valor_referencia TEXT,
                fuera_de_rango TEXT,
                observacion TEXT,
                FOREIGN KEY (solicitud_id) REFERENCES solicitudes_analisis(id) ON DELETE CASCADE
            )
        """)
        print("Tabla resultados_parametros OK")

        print("Creando tabla usuarios...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabla usuarios OK")

        print("Creando índices...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_paciente_nombre ON pacientes(nombre)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_solicitudes_paciente ON solicitudes_analisis(paciente_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_solicitudes_estado ON solicitudes_analisis(estado)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_resultados_solicitud ON resultados_parametros(solicitud_id)")
        print("Índices OK")

        conn.commit()
        print("Base de datos creada/actualizada correctamente.")

    except Exception as e:
        print("ERROR al crear tablas:", str(e))
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

    print("Fin de crear_tablas()")


if __name__ == "__main__":
    crear_tablas()