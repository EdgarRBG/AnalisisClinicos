import webview
import screeninfo
import os
import tkinter as tk
from tkinter import filedialog
import datetime
import json

from backend.auth import Auth
from backend.pacientes import Pacientes
from backend.citas import Citas
from backend.analisis import Analisis
from backend.usuarios import Usuarios
from backend.espera import Espera
from backend.bloques import Bloques
from backend.database import crear_tablas
from backend.parametros import Parametros


crear_tablas()

auth = Auth()
pacientes = Pacientes()
citas = Citas()
analisis = Analisis()
usuarios = Usuarios()
bloques = Bloques()
espera_obj = Espera()
parametros_obj = Parametros()
parametros_obj.sembrar_datos_iniciales()


# ==================== FUNCIÓN PARA CONVERTIR FECHAS ====================
def convertir_fechas_a_str(data):
    """Convierte objetos datetime a string para que sea JSON serializable"""
    if isinstance(data, list):
        return [convertir_fechas_a_str(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (datetime.date, datetime.datetime)):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, list) or isinstance(value, dict):
                data[key] = convertir_fechas_a_str(value)
        return data
    return data


class API:

    # ==================== DASHBOARD ====================
    def contarPacientesHoy(self):
        return pacientes.contar_registrados_hoy()

    def obtenerPacientesRecientes(self, limite=10):
        data = pacientes.obtener_recientes(limite)
        return convertir_fechas_a_str(data)

    def obtenerCitasHoy(self):
        data = citas.obtener_citas_hoy_con_nombre()
        return convertir_fechas_a_str(data)

    def login(self, usuario, contrasena):
        return auth.validar_login(usuario, contrasena)

    def guardarPaciente(self, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones='', fecha_nacimiento=''):
        return pacientes.guardar(nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_nacimiento)

    def obtenerTodosLosPacientes(self):
        data = pacientes.obtener_todos()
        return convertir_fechas_a_str(data)

    def obtenerPacientes(self):
        return pacientes.obtener_para_select()

    def obtenerPacientePorId(self, paciente_id):
        data = pacientes.obtener_por_id(paciente_id)
        return convertir_fechas_a_str(data) if data else None

    def eliminarPaciente(self, paciente_id, contrasena_admin):
        return pacientes.eliminar(paciente_id, contrasena_admin)

    def editarPaciente(self, paciente_id, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones='', fecha_nacimiento=''):
        return pacientes.editar(paciente_id, nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_nacimiento)

    def respaldar_pacientes(self):
        return pacientes.respaldar_pacientes()

    def seleccionar_y_restaurar_pacientes(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Seleccionar Respaldo de Pacientes",
                filetypes=[("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
            )
            root.destroy()

            if not file_path:
                return {"ok": False, "error": "No se seleccionó ningún archivo"}

            return pacientes.restaurar_respaldo(file_path)
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def registrarCita(self, paciente_id, fecha, hora, tipo, estado='pendiente', observaciones=''):
        return citas.registrar(paciente_id, fecha, hora, tipo, estado, observaciones)

    def obtenerCitas(self):
        data = citas.obtener_todas()
        return convertir_fechas_a_str(data)

    def eliminarCita(self, cita_id):
        return citas.eliminar(cita_id)

    def contarCitasHoy(self):
        return citas.contar_citas_hoy()

    def registrarEnEspera(self, nombre='', fecha_nacimiento='', edad=None, telefono='', fecha_cita='', hora_cita='', tipo_estudio='', observaciones=''):
        return espera_obj.registrar(nombre, fecha_nacimiento, edad, telefono, fecha_cita, hora_cita, tipo_estudio, observaciones)

    def obtenerPacientesEnEspera(self):
        data = espera_obj.obtener_todos()
        return convertir_fechas_a_str(data)

    def marcarProcesado(self, espera_id):
        return espera_obj.marcar_procesado(espera_id)

    def registrarSolicitudAnalisis(self, paciente_id, cita_id=None, id_muestra=None, medico_solicitante="", tipo_estudio="", observaciones=""):
        return analisis.registrar_solicitud(paciente_id, cita_id, id_muestra, medico_solicitante, tipo_estudio, observaciones)

    def obtenerSolicitudesPendientes(self):
        data = analisis.obtener_pendientes()
        return convertir_fechas_a_str(data)

    def obtenerSolicitud(self, solicitud_id):
        data = analisis.obtener_solicitud(solicitud_id)
        return convertir_fechas_a_str(data) if data else None

    def agregarResultadoAnalisis(self, solicitud_id, parametro, resultado, unidades="", valor_referencia="", fuera_de_rango="", observacion=""):
        return analisis.agregar_resultado(solicitud_id, parametro, resultado, unidades, valor_referencia, fuera_de_rango, observacion)

    def actualizarEstadoSolicitud(self, solicitud_id, estado):
        return analisis.actualizar_estado(solicitud_id, estado)

    def actualizarMedicoSolicitud(self, solicitud_id, medico_solicitante):
        return analisis.actualizar_medico(solicitud_id, medico_solicitante)

    def obtenerSolicitudesFinalizadas(self):
        data = analisis.obtener_finalizadas()
        return convertir_fechas_a_str(data)

    def obtenerFinalizadasHoy(self):
        try:
            data = analisis.obtener_finalizadas_hoy()
            return convertir_fechas_a_str(data)
        except AttributeError:
            return []

    def contarPendientes(self):
        return analisis.contar_pendientes()

    def eliminarSolicitud(self, solicitud_id):
        return analisis.eliminar_solicitud(solicitud_id)

    def obtenerEstudiosDisponibles(self):
        return bloques.obtener_estudios_disponibles()

    def guardarBloquesSolicitud(self, solicitud_id, bloques_json):
        return bloques.guardar_bloques_solicitud(solicitud_id, bloques_json)

    def seleccionarYLeerCSV(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo de resultados (CSV)",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            root.destroy()

            if not file_path:
                return {"ok": False, "error": "No se seleccionó archivo"}

            import csv

            muestras = {}
            orden_muestras = []

            encodings = ['utf-8-sig', 'latin-1', 'cp1252']
            f_obj = None
            for enc in encodings:
                try:
                    f_obj = open(file_path, mode='r', encoding=enc, errors='strict')
                    f_obj.read(512)
                    f_obj.seek(0)
                    break
                except Exception:
                    if f_obj:
                        f_obj.close()
                    f_obj = None

            if not f_obj:
                f_obj = open(file_path, mode='r', encoding='utf-8', errors='replace')

            with f_obj as f:
                reader = csv.DictReader(f)
                for row in reader:
                    prueba     = (row.get('Prueba')            or row.get('parametro') or '').strip()
                    resultado  = (row.get('Resultado')         or row.get('valor')     or '').strip()
                    no_muestra = str(row.get('No. de muestra') or row.get('No. muestra') or '1').strip()
                    nombre     = (row.get('Nombre')            or '').strip()

                    if not prueba:
                        continue

                    if no_muestra not in muestras:
                        muestras[no_muestra] = {"no": no_muestra, "nombre": nombre, "datos": {}}
                        orden_muestras.append(no_muestra)

                    muestras[no_muestra]["datos"][prueba] = resultado
                    if not muestras[no_muestra]["nombre"] and nombre:
                        muestras[no_muestra]["nombre"] = nombre

            lista = [muestras[k] for k in orden_muestras]
            if not lista:
                return {"ok": False, "error": "No se encontraron datos válidos en el archivo"}
            return {"ok": True, "muestras": lista}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    def crearUsuario(self, usuario, contrasena, rol):
        return usuarios.crear_usuario(usuario, contrasena, rol)

    def obtenerUsuarios(self):
        return usuarios.obtener_todos()

    def actualizarRolUsuario(self, user_id, nuevo_rol):
        return usuarios.actualizar_rol(user_id, nuevo_rol)

    def actualizarContrasenaUsuario(self, user_id, nueva_contrasena):
        return usuarios.actualizar_contrasena(user_id, nueva_contrasena)

    def eliminarUsuario(self, user_id):
        return usuarios.eliminar_usuario(user_id)

    def verificarContrasenaAdmin(self, contrasena):
        return usuarios.verificar_contrasena_admin(contrasena)

    # ==================== PARÁMETROS ====================
    def obtenerParametros(self):
        return convertir_fechas_a_str(parametros_obj.obtener_todos())

    def agregarParametro(self, nombre, unidades, valor_referencia_min, valor_referencia_max,
                         tipo_estudio, rango_hombre_min='', rango_hombre_max='',
                         rango_mujer_min='', rango_mujer_max='', observaciones=''):
        return parametros_obj.agregar(nombre, unidades, valor_referencia_min, valor_referencia_max,
                                      tipo_estudio, rango_hombre_min, rango_hombre_max,
                                      rango_mujer_min, rango_mujer_max, observaciones)

    def editarParametro(self, parametro_id, nombre, unidades, valor_referencia_min, valor_referencia_max,
                        tipo_estudio, rango_hombre_min='', rango_hombre_max='',
                        rango_mujer_min='', rango_mujer_max='', observaciones=''):
        return parametros_obj.editar(parametro_id, nombre, unidades, valor_referencia_min, valor_referencia_max,
                                     tipo_estudio, rango_hombre_min, rango_hombre_max,
                                     rango_mujer_min, rango_mujer_max, observaciones)

    def eliminarParametro(self, parametro_id):
        return parametros_obj.eliminar(parametro_id)

    def obtenerParametrosPorTipo(self, tipo_estudio):
        return parametros_obj.obtener_por_tipo(tipo_estudio)


if __name__ == "__main__":
    try:
        monitor = screeninfo.get_monitors()[0]
        ancho, alto = monitor.width, monitor.height
    except:
        ancho, alto = 1400, 900

    base_dir = os.path.dirname(os.path.abspath(__file__))
    login_html_path = os.path.join(base_dir, 'frontend', 'login.html')

    webview.create_window(
        title="Analitic - Laboratorio Clínico",
        url=login_html_path,
        js_api=API(),
        width=ancho,
        height=alto,
        maximized=True,
        resizable=True,
        text_select=True
    )

    webview.start(debug=True, http_server=True)