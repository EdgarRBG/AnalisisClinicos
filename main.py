
import webview
import screeninfo
import os
import tkinter as tk
from tkinter import filedialog


from backend.auth import Auth
from backend.pacientes import Pacientes
from backend.citas import Citas
from backend.analisis import Analisis
from backend.usuarios import Usuarios
from backend.espera import Espera
from backend.bloques import Bloques   
from backend.database import crear_tablas


crear_tablas()


auth = Auth()
pacientes = Pacientes()
citas = Citas()
analisis = Analisis()
usuarios = Usuarios()
bloques = Bloques()
espera_obj = Espera()

class API:
  
    def login(self, usuario, contrasena):
        return auth.validar_login(usuario, contrasena)

  
    def guardarPaciente(self, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones='', fecha_nacimiento=''):
        return pacientes.guardar(nombre, edad, telefono, sexo, correo, direccion, observaciones, fecha_nacimiento)

    def obtenerTodosLosPacientes(self):
        return pacientes.obtener_todos()

    def obtenerPacientes(self):
        return pacientes.obtener_para_select()

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
        return citas.obtener_todas()

    def eliminarCita(self, cita_id):
        return citas.eliminar(cita_id)

    def contarCitasHoy(self):
        return citas.contar_citas_hoy()

   
    def registrarEnEspera(self, nombre='', fecha_nacimiento='', edad=None, telefono='', fecha_cita='', hora_cita='', tipo_estudio='', observaciones=''):
        return espera_obj.registrar(nombre, fecha_nacimiento, edad, telefono, fecha_cita, hora_cita, tipo_estudio, observaciones)

    def obtenerPacientesEnEspera(self):
        return espera_obj.obtener_todos()

    def marcarProcesado(self, espera_id):
        return espera_obj.marcar_procesado(espera_id)

  
    def registrarSolicitudAnalisis(self, paciente_id, cita_id=None, id_muestra=None, medico_solicitante="", tipo_estudio="", observaciones=""):
        return analisis.registrar_solicitud(paciente_id, cita_id, id_muestra, medico_solicitante, tipo_estudio, observaciones)

    def obtenerSolicitudesPendientes(self):
        return analisis.obtener_pendientes()

    def obtenerSolicitud(self, solicitud_id):
        return analisis.obtener_solicitud(solicitud_id)

    def agregarResultadoAnalisis(self, solicitud_id, parametro, resultado, unidades="", valor_referencia="", fuera_de_rango="", observacion=""):
        return analisis.agregar_resultado(solicitud_id, parametro, resultado, unidades, valor_referencia, fuera_de_rango, observacion)

    def actualizarEstadoSolicitud(self, solicitud_id, estado):
        return analisis.actualizar_estado(solicitud_id, estado)

    def obtenerSolicitudesFinalizadas(self):
        return analisis.obtener_finalizadas()

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
            resultados = {}
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                  
                    param = row.get('parametro', '').strip()
                    val = row.get('valor', '').strip()
                    if param:
                        resultados[param] = val
            return {"ok": True, "datos": resultados}
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