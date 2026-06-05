import mysql.connector
import os
import sys
from backend.auth import Auth
 
auth = Auth()
 

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME",     "sistema_laboratorio"),
    "charset":  "utf8mb4",
    "autocommit": False,
}
 
print(f"Usando base de datos MySQL en: {DB_CONFIG['host']}:{DB_CONFIG['port']} / {DB_CONFIG['database']}")
 
 
def conectar():
    """Devuelve una conexión MySQL con row_factory similar a sqlite3.Row."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
 
 
def crear_tablas():
    print("Iniciando creación de tablas en MySQL...")
 
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id              INT PRIMARY KEY AUTO_INCREMENT,
                nombre          TEXT NOT NULL,
                edad            INT NOT NULL,
                telefono        TEXT NOT NULL,
                sexo            TEXT,
                correo          TEXT,
                direccion       TEXT,
                observaciones   TEXT,
                fecha_nacimiento TEXT,
                fecha_registro  DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id              INT PRIMARY KEY AUTO_INCREMENT,
                paciente_id     INT NOT NULL,
                fecha           TEXT NOT NULL,
                hora            TEXT NOT NULL,
                tipo            TEXT NOT NULL,
                estado          VARCHAR(50) DEFAULT 'pendiente',
                observaciones   TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_analisis (
                id                      INT PRIMARY KEY AUTO_INCREMENT,
                paciente_id             INT NOT NULL,
                cita_id                 INT,
                id_muestra              VARCHAR(20) UNIQUE NOT NULL,
                fecha_recepcion         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_reporte           DATETIME,
                medico_solicitante      TEXT,
                tipo_estudio            TEXT NOT NULL,
                estado                  VARCHAR(50) DEFAULT 'pendiente',
                observaciones_generales TEXT,
                creado_por              TEXT,
                fecha_creacion          DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
                FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_parametros (
                id               INT PRIMARY KEY AUTO_INCREMENT,
                solicitud_id     INT NOT NULL,
                parametro        TEXT NOT NULL,
                resultado        TEXT,
                unidades         TEXT,
                valor_referencia TEXT,
                fuera_de_rango   TEXT,
                observacion      TEXT,
                FOREIGN KEY (solicitud_id) REFERENCES solicitudes_analisis(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id             INT PRIMARY KEY AUTO_INCREMENT,
                usuario        VARCHAR(100) NOT NULL UNIQUE,
                contrasena     TEXT NOT NULL,
                rol            TEXT NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS espera (
                id               INT PRIMARY KEY AUTO_INCREMENT,
                nombre           TEXT,
                fecha_nacimiento TEXT,
                edad             INT,
                telefono         TEXT,
                fecha_registro   DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_cita       TEXT,
                hora_cita        TEXT,
                tipo_estudio     TEXT,
                observaciones    TEXT,
                estado           VARCHAR(50) DEFAULT 'en_espera',
                procesado        INT DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parametros (
                id                    INT PRIMARY KEY AUTO_INCREMENT,
                nombre                VARCHAR(150) NOT NULL,
                unidades              VARCHAR(80),
                valor_referencia_min  VARCHAR(50),
                valor_referencia_max  VARCHAR(50),
                tipo_estudio          VARCHAR(150),
                rango_hombre_min      VARCHAR(50),
                rango_hombre_max      VARCHAR(50),
                rango_mujer_min       VARCHAR(50),
                rango_mujer_max       VARCHAR(50),
                observaciones         TEXT,
                fecha_creacion        DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
 
 
        conn.commit()
        print("Tablas creadas correctamente.")
 
     
        cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", ("admin",))
        admin = cursor.fetchone()
 
        if not admin:
            print("Creando usuario admin...")
            contrasena_hash = auth.hashear_contrasena("admin123")

            cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, rol)
                VALUES (%s, %s, %s)
            """, ("admin", contrasena_hash, "admin"))

            conn.commit()
            print("Usuario admin creado correctamente")
        else:
            print("El usuario admin ya existe")
 
    except Exception as e:
        print("ERROR al crear tablas:", str(e))
    finally:
        if conn:
            conn.close()
 
 
if __name__ == "__main__":
    crear_tablas()