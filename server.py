"""
server.py — Analitic Web Server
Convierte la app pywebview a Flask con autenticación JWT (5 min sliding window).
"""

import os
import datetime
from functools import wraps

from flask import (
    Flask, request, jsonify, send_from_directory,
    redirect, make_response
)
import jwt as pyjwt

from backend.auth import Auth
from backend.pacientes import Pacientes
from backend.citas import Citas
from backend.analisis import Analisis
from backend.usuarios import Usuarios
from backend.espera import Espera
from backend.bloques import Bloques
from backend.database import crear_tablas
from backend.parametros import Parametros

app = Flask(__name__, static_folder="frontend", static_url_path="/static")

SECRET_KEY = os.getenv("SECRET_KEY", "analitic-secret-2024-xK9q")
TOKEN_MINUTOS = int(os.getenv("TOKEN_MINUTOS", 5))

crear_tablas()

_auth       = Auth()
_pacientes  = Pacientes()
_citas      = Citas()
_analisis   = Analisis()
_usuarios   = Usuarios()
_espera     = Espera()
_bloques    = Bloques()
_parametros = Parametros()
_parametros.sembrar_datos_iniciales()


def crear_token(usuario: str, rol: str) -> str:
    payload = {
        "usuario": usuario,
        "rol": rol,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_MINUTOS)
    }
    return pyjwt.encode(payload, SECRET_KEY, algorithm="HS256")


def _set_cookie(response, token: str):
    """Agrega el JWT como cookie httpOnly con expiración deslizante."""
    response.set_cookie(
        "token", token,
        httponly=True,
        samesite="Lax",
        max_age=TOKEN_MINUTOS * 60,
        secure=os.getenv("FLASK_ENV") == "production"
    )
    return response


def requiere_token(f):
    """Decorador: valida JWT y renueva la cookie en cada llamada exitosa."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"error": "No autorizado", "expired": True}), 401
        try:
            data = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.usuario_actual = data.get("usuario", "")
            request.rol_actual = data.get("rol", "")
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Sesión expirada", "expired": True}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"error": "Token inválido", "expired": True}), 401

        result = f(*args, **kwargs)

        nuevo_token = crear_token(request.usuario_actual, request.rol_actual)
        if isinstance(result, tuple):
            resp, status = result
        else:
            resp, status = result, 200

        _set_cookie(resp, nuevo_token)
        return resp, status

    return decorated


def _json_dates(data):
    if isinstance(data, list):
        return [_json_dates(i) for i in data]
    if isinstance(data, dict):
        return {k: (v.strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(v, (datetime.date, datetime.datetime))
                    else _json_dates(v))
                for k, v in data.items()}
    return data


PAGINAS = {
    "/":            "login.html",
    "/login":       "login.html",
    "/dashboard":   "dashboard.html",
    "/pacientes":   "pacientes.html",
    "/citas":       "citas.html",
    "/analisis":    "analisis.html",
    "/espera":      "espera.html",
    "/usuarios":    "usuarios.html",
    "/parametros":  "Parametros.html",
    "/resultados":  "resultados.html",
    "/bloques":     "bloques.html",
}

for ruta, archivo in PAGINAS.items():
    endpoint = "page_" + ruta.strip("/").replace("/", "_") or "page_root"
    def _make_view(nombre_archivo):
        def view():
            return send_from_directory("frontend", nombre_archivo)
        return view
    app.add_url_rule(ruta, endpoint=endpoint, view_func=_make_view(archivo))


@app.route("/api/login", methods=["POST"])
def api_login():
    body = request.json or {}
    args = body.get("args", [])
    usuario = args[0] if len(args) > 0 else ""
    contrasena = args[1] if len(args) > 1 else ""

    resultado = _auth.validar_login(usuario, contrasena)

    if resultado.get("ok"):
        token = crear_token(usuario, resultado.get("rol", ""))
        resp = make_response(jsonify(resultado))
        _set_cookie(resp, token)
        return resp

    return jsonify(resultado)


@app.route("/api/logout", methods=["POST"])
def api_logout():
    resp = make_response(jsonify({"ok": True}))
    resp.delete_cookie("token")
    return resp


@app.route("/api/check_auth", methods=["GET"])
def api_check_auth():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"ok": False}), 401
    try:
        data = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"ok": True, "usuario": data["usuario"], "rol": data["rol"]})
    except pyjwt.PyJWTError:
        return jsonify({"ok": False}), 401


METODOS = {
    "contarPacientesHoy":         lambda args: _pacientes.contar_registrados_hoy(),
    "obtenerPacientesRecientes":  lambda args: _json_dates(_pacientes.obtener_recientes(args[0] if args else 10)),
    "obtenerPacientesDeHoy":      lambda args: _json_dates(_pacientes.obtener_recientes(50)),
    "obtenerCitasHoy":            lambda args: _json_dates(_citas.obtener_citas_hoy_con_nombre()),
    "obtenerFinalizadasHoy":      lambda args: _json_dates(_analisis.obtener_finalizadas_hoy()),
    "contarPendientes":           lambda args: _analisis.contar_pendientes(),
    "contarCitasHoy":             lambda args: _citas.contar_citas_hoy(),

    "guardarPaciente":            lambda args: _pacientes.guardar(*args),
    "obtenerTodosLosPacientes":   lambda args: _json_dates(_pacientes.obtener_todos()),
    "obtenerPacientes":           lambda args: _pacientes.obtener_para_select(),
    "obtenerPacientePorId":       lambda args: _json_dates(_pacientes.obtener_por_id(args[0])),
    "eliminarPaciente":           lambda args: _pacientes.eliminar(*args),
    "editarPaciente":             lambda args: _pacientes.editar(*args),
    "respaldar_pacientes":        lambda args: {"ok": False, "error": "Usa el botón de exportar en la web"},
    "seleccionar_y_restaurar_pacientes": lambda args: {"ok": False, "error": "Usa el formulario de importar"},

    "registrarCita":              lambda args: _citas.registrar(*args),
    "obtenerCitas":               lambda args: _json_dates(_citas.obtener_todas()),
    "eliminarCita":               lambda args: _citas.eliminar(args[0]),

    "registrarSolicitudAnalisis": lambda args: _analisis.registrar_solicitud(*args),
    "obtenerSolicitudesPendientes": lambda args: _json_dates(_analisis.obtener_pendientes()),
    "obtenerSolicitud":           lambda args: _json_dates(_analisis.obtener_solicitud(args[0])),
    "agregarResultadoAnalisis":   lambda args: _analisis.agregar_resultado(*args),
    "actualizarEstadoSolicitud":  lambda args: _analisis.actualizar_estado(*args),
    "actualizarMedicoSolicitud":  lambda args: _analisis.actualizar_medico(*args),
    "obtenerSolicitudesFinalizadas": lambda args: _json_dates(_analisis.obtener_finalizadas()),
    "eliminarSolicitud":          lambda args: _analisis.eliminar_solicitud(args[0]),

    "obtenerEstudiosDisponibles": lambda args: _bloques.obtener_estudios_disponibles(),
    "guardarBloquesSolicitud":    lambda args: _bloques.guardar_bloques_solicitud(*args),

    "registrarEnEspera":          lambda args: _espera.registrar(*args),
    "obtenerPacientesEnEspera":   lambda args: _json_dates(_espera.obtener_todos()),
    "marcarProcesado":            lambda args: _espera.marcar_procesado(args[0]),

    "crearUsuario":               lambda args: _usuarios.crear_usuario(*args),
    "obtenerUsuarios":            lambda args: _usuarios.obtener_todos(),
    "actualizarRolUsuario":       lambda args: _usuarios.actualizar_rol(*args),
    "actualizarContrasenaUsuario":lambda args: _usuarios.actualizar_contrasena(*args),
    "eliminarUsuario":            lambda args: _usuarios.eliminar_usuario(args[0]),
    "verificarContrasenaAdmin":   lambda args: _usuarios.verificar_contrasena_admin(args[0]),

    "obtenerParametros":          lambda args: _json_dates(_parametros.obtener_todos()),
    "agregarParametro":           lambda args: _parametros.agregar(*args),
    "editarParametro":            lambda args: _parametros.editar(*args),
    "eliminarParametro":          lambda args: _parametros.eliminar(args[0]),
    "obtenerParametrosPorTipo":   lambda args: _parametros.obtener_por_tipo(args[0]),

    "seleccionarYLeerCSV":        lambda args: {"ok": False, "error": "Usa el formulario de carga de archivo"},
}


@app.route("/api/<metodo>", methods=["POST"])
@requiere_token
def api_dispatch(metodo):
    body = request.json or {}
    args = body.get("args", [])

    handler = METODOS.get(metodo)
    if handler is None:
        return jsonify({"error": f"Método '{metodo}' no encontrado"}), 404

    try:
        resultado = handler(args)
        return jsonify(resultado)
    except Exception as e:
        print(f"[ERROR] {metodo}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/descargar_respaldo", methods=["GET"])
@requiere_token
def descargar_respaldo():
    import io
    import pandas as pd

    pacientes = _pacientes.obtener_todos()
    if not pacientes:
        return jsonify({"error": "No hay pacientes para respaldar"}), 400

    df = pd.DataFrame(pacientes)

    for col in df.columns:
        df[col] = df[col].apply(
            lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(v, (datetime.date, datetime.datetime)) else v
        )

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Pacientes")
    buffer.seek(0)

    fecha_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre = f"Respaldo_Pacientes_{fecha_str}.xlsx"

    from flask import send_file
    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=nombre
    )


@app.route("/api/restaurar_pacientes", methods=["POST"])
@requiere_token
def restaurar_pacientes():
    import tempfile, os
    archivo = request.files.get("archivo")
    if not archivo:
        return jsonify({"ok": False, "error": "No se recibió archivo"})

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        archivo.save(tmp.name)
        ruta_tmp = tmp.name

    try:
        resultado = _pacientes.restaurar_respaldo(ruta_tmp)
    finally:
        os.unlink(ruta_tmp)

    return jsonify(resultado)


@app.route("/api/upload_csv", methods=["POST"])
@requiere_token
def upload_csv():
    import csv, io
    f = request.files.get("archivo")
    if not f:
        return jsonify({"ok": False, "error": "No se recibió archivo"})

    muestras = {}
    orden = []
    content = f.read().decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        prueba     = (row.get("Prueba") or row.get("parametro") or "").strip()
        resultado  = (row.get("Resultado") or row.get("valor") or "").strip()
        no_muestra = str(row.get("No. de muestra") or row.get("No. muestra") or "1").strip()
        nombre     = (row.get("Nombre") or "").strip()
        if not prueba:
            continue
        if no_muestra not in muestras:
            muestras[no_muestra] = {"no": no_muestra, "nombre": nombre, "datos": {}}
            orden.append(no_muestra)
        muestras[no_muestra]["datos"][prueba] = resultado

    lista = [muestras[k] for k in orden]
    return jsonify({"ok": True, "muestras": lista} if lista else {"ok": False, "error": "Sin datos"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") != "production")
