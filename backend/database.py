import sqlite3
import os
import sys
from backend.auth import Auth

auth = Auth()

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "sistema_laboratorio.db")

print("Usando base de datos en:", DB_PATH)

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
        cursor = conn.cursor()

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
                fecha_nacimiento TEXT,
                fecha_registro TEXT DEFAULT (datetime('now'))
            )
        """)

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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS espera (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                fecha_nacimiento TEXT,
                edad INTEGER,
                telefono TEXT,
                fecha_registro TEXT DEFAULT (datetime('now')),
                fecha_cita TEXT,
                hora_cita TEXT,
                tipo_estudio TEXT,
                observaciones TEXT,
                estado TEXT DEFAULT 'en_espera',
                procesado INTEGER DEFAULT 0
            )
        """)

        conn.commit()
        print("Tablas creadas correctamente.")

       
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
        admin = cursor.fetchone()

        if not admin:
            print("Creando usuario admin...")

            contrasena_hash = auth.hashear_contrasena("admin123")

            cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, rol)
                VALUES (?, ?, ?)
            """, ("admin", contrasena_hash, "admin"))

            conn.commit()
            print("✅ Usuario admin creado correctamente")
        else:
            print("ℹ️ El usuario admin ya existe")

    except Exception as e:
        print("ERROR al crear tablas:", str(e))
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_tablas()