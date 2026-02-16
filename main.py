import webview

from backend.auth import Auth
from backend.pacientes import Pacientes
from backend.citas import Citas
from backend.analisis import Analisis
from backend.usuarios import Usuarios           
from backend.database import crear_tablas

# Crea/verifica tablas al iniciar
crear_tablas()

auth = Auth()
pacientes = Pacientes()
citas = Citas()
analisis = Analisis()
usuarios = Usuarios()                           


class API:
  
    def login(self, usuario, contraseña):
        return auth.validar_login(usuario, contraseña)

   
    def guardarPaciente(self, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones=''):
        return pacientes.guardar(nombre, edad, telefono, sexo, correo, direccion, observaciones)

    def obtenerTodosLosPacientes(self):
        return pacientes.obtener_todos()

    def obtenerPacientes(self):
        return pacientes.obtener_para_select()

    def eliminarPaciente(self, paciente_id):
        return pacientes.eliminar(paciente_id)

    def editarPaciente(self, paciente_id, nombre, edad, telefono, sexo='', correo='', direccion='', observaciones=''):
        return pacientes.editar(paciente_id, nombre, edad, telefono, sexo, correo, direccion, observaciones)

    def obtenerPacientePorId(self, paciente_id):
        return pacientes.obtener_por_id(paciente_id)

    
    def registrarCita(self, paciente_id, fecha, hora, tipo, estado='pendiente', observaciones=''):
        return citas.registrar(paciente_id, fecha, hora, tipo, estado, observaciones)

    def obtenerCitas(self):
        return citas.obtener_todas()

    def obtenerCitaPorId(self, cita_id):
        return citas.obtener_por_id(cita_id)

    def actualizarCita(self, cita_id, tipo, estado, observaciones):
        return citas.actualizar(cita_id, tipo, estado, observaciones)

    def eliminarCita(self, cita_id):
        return citas.eliminar(cita_id)

   
    def registrarSolicitudAnalisis(self, paciente_id, cita_id=None, id_muestra=None, medico_solicitante="", tipo_estudio="", observaciones=""):
        return analisis.registrar_solicitud(paciente_id, cita_id, id_muestra, medico_solicitante, tipo_estudio, observaciones)

    def agregarResultadoAnalisis(self, solicitud_id, parametro, resultado=None, unidades="", valor_referencia="", fuera_de_rango="", observacion=""):
        return analisis.agregar_resultado(solicitud_id, parametro, resultado, unidades, valor_referencia, fuera_de_rango, observacion)

    def obtenerSolicitudesPendientes(self):
        return analisis.obtener_pendientes()

    def obtenerSolicitud(self, solicitud_id):
        return analisis.obtener_solicitud(solicitud_id)

    def actualizarEstadoSolicitud(self, solicitud_id, nuevo_estado):
        return analisis.actualizar_estado(solicitud_id, nuevo_estado)
    
    def obtenerSolicitudesFinalizadas(self):
        return analisis.obtener_finalizadas()

    def generarReporte(self, solicitud_id):
        return analisis.generar_reporte(solicitud_id)

    def importarDesdeCSV(self, solicitud_id, csv_content):
        return analisis.importarDesdeCSV(solicitud_id, csv_content)

    # ←——— FUNCIÓN NUEVA AGREGADA AQUÍ ↓↓↓
    def eliminarSolicitud(self, solicitud_id):
        return analisis.eliminar_solicitud(solicitud_id)
   
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
   
    def eliminarParametro(self, solicitud_id, parametro):
        return analisis.eliminar_parametro(solicitud_id, parametro)


if __name__ == "__main__":
    webview.create_window(
        title="Laboratorio de Análisis Clínicos",
        url="frontend/login.html",
        js_api=API(),
        width=1400,
        height=900,
        min_size=(1200, 800),
        maximized=True,
        resizable=True
    )

    webview.start(debug=True, http_server=True)