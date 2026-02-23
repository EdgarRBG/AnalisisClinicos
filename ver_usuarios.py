import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sistema_laboratorio.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id, usuario, contraseña, rol FROM usuarios")
usuarios = cursor.fetchall()

if usuarios:
    print("Usuarios encontrados (detalle exacto):")
    for u in usuarios:
        print(f"ID: {u[0]}")
        print(f"Usuario crudo: '{u[1]}' | Longitud: {len(u[1])} | Representación: {repr(u[1])}")
        print(f"Contraseña cruda: '{u[2]}' | Longitud: {len(u[2])} | Representación: {repr(u[2])}")
        print(f"Rol: {u[3]}")
        print("-" * 40)
else:
    print("No hay usuarios.")

conn.close()