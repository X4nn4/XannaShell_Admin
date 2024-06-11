from tkinter import *
import tkinter as tk
import os
from tkinter import scrolledtext
from tkinter import Menu
from io import open
from tkinter import PanedWindow
from tkinter import ttk
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget
import sys

#--------FUNCTIONS AND CLASS---------#
class MonitorRendimiento(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monitor de Rendimiento')

        # Configurar el layout principal
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        # Configurar el gráfico de líneas para la CPU
        self.cpu_plot = PlotWidget()
        layout.addWidget(self.cpu_plot)
        self.cpu_plot.setYRange(0, 100)
        self.cpu_plot.setLabel('left', 'Uso de CPU (%)')
        self.cpu_plot.setLabel('bottom', 'Tiempo (s)')
        self.cpu_curve = self.cpu_plot.plot(pen='r')

        # Configurar el gráfico de líneas para la memoria
        self.memory_plot = PlotWidget()
        layout.addWidget(self.memory_plot)
        self.memory_plot.setYRange(0, 100)
        self.memory_plot.setLabel('left', 'Uso de Memoria (%)')
        self.memory_plot.setLabel('bottom', 'Tiempo (s)')
        self.memory_curve = self.memory_plot.plot(pen='b')

        # Configurar el gráfico de líneas para el disco
        self.disk_plot = PlotWidget()
        layout.addWidget(self.disk_plot)
        self.disk_plot.setYRange(0, 100)
        self.disk_plot.setLabel('left', 'Uso de Disco (%)')
        self.disk_plot.setLabel('bottom', 'Tiempo (s)')
        self.disk_curve = self.disk_plot.plot(pen='g')

        # Inicializar los datos y el temporizador
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def update_plot(self):
        # Obtener el uso de la CPU y la memoria
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Obtener el uso del disco
        disk_usage = psutil.disk_usage('/').percent

        # Agregar datos al historial
        self.cpu_history.append(cpu_usage)
        self.memory_history.append(memory_usage)
        self.disk_history.append(disk_usage)

        # Actualizar los datos en los gráficos de líneas
        self.cpu_curve.setData(self.cpu_history)
        self.memory_curve.setData(self.memory_history)
        self.disk_curve.setData(self.disk_history)

def rendimiento():
    app = QApplication(sys.argv)
    window = MonitorRendimiento()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    app.exec_()

def ocultar_paneles():
    pw_red.pack_forget()
    pw_puertos.pack_forget()
    pw_procesos.pack_forget()
    pw_información_general_del_sistema.pack_forget()
    pw_usuarios_active_directory.pack_forget()
    pw_grupos_active_directory.pack_forget()
    pw_formatear.pack_forget()
    pw_filtrado.pack_forget()
    pw_servicios.pack_forget()
    pw_administrar_grupos.pack_forget()
    pw_formateo_realizado.pack_forget()
    pw_eventos.pack_forget()
    pw_eventos_activos.pack_forget()

def get_storage_devices():
    # Obtener todos los dispositivos de almacenamiento disponibles en el sistema
    partitions = psutil.disk_partitions(all=True)
    devices = []
    for partition in partitions:
        device = partition.device
        if device not in devices:
            devices.append(device)
    return devices

def get_event_type():
    lista = ["Application","Active Directory Web Services","DFS Replication","Directory Service","DNS Server","HardwareEvents","Internet Explorer","Key Management Service","Security","System","Windows Powershell"]
    return lista

def formateo():
    ocultar_paneles()
    pw_formateo_realizado.pack()
    seleccion=str(combo_dispositivos.get()).replace(':', ' ')
    modificada=seleccion.replace('\\', ' ')
    t12.delete("1.0",END)
    t12.update()
    t12.insert(END, "Loading...")
    t12.update()
    info = os.popen(f'powershell.exe -command "Format-Volume -DriveLetter {modificada}"').read()
    t12.delete("1.0",END)
    t12.insert(1.0, info)

def formatear():
    ocultar_paneles()
    pw_formatear.pack()
    t11.delete("1.0",END)
    t11.update()
    t11.insert(END, "Loading...")
    t11.update()
    info = os.popen(f'powershell.exe -File "informacion_de_almacenamiento.ps1"').read()
    t11.delete("1.0",END)
    t11.insert(1.0, info)


def informacion_general_del_sistema():
    ocultar_paneles()
    pw_información_general_del_sistema.pack()
    t1.delete("1.0",END)
    t1.update()
    t1.insert(END, "Loading...")
    t1.update()
    info = os.popen(f'powershell.exe "Get-computerinfo"').read()
    t1.delete("1.0",END)
    t1.insert(1.0, info)

def finalizar_proceso():
    pid=int(entrada.get())
    os.system(f'powershell.exe "Stop-process -Id {pid}"')
    entrada.delete(0, END)
    procesos()

def procesos():
    ocultar_paneles()
    pw_procesos.pack()
    t4.pack(expand=True, fill='both')
    t4.delete("1.0", END)
    t4.update()
    t4.insert(END, "Loading...")
    t4.update()
    info = os.popen(f'powershell.exe "Get-Process"').read()
    t4.delete("1.0",END)
    t4.insert(1.0, info)

def red():
    ocultar_paneles()
    pw_red.pack()
    t2.delete("1.0",END)
    t2.update()
    t2.insert(END, "Loading...")
    t2.update()
    info = os.popen(f'powershell.exe "Get-NetIPAddress"').read()
    t2.delete("1.0",END)
    t2.insert(1.0, info)


def puertos_abiertos():
    ocultar_paneles()
    pw_puertos.pack()
    t3.delete("1.0",END)
    t3.update()
    t3.insert(END, "Loading...")
    t3.update()
    info = os.popen(f'powershell.exe "Get-NetTCPConnection | Select-Object -Property LocalPort, State"').read()
    t3.delete("1.0",END)
    t3.insert(1.0, info)

def servicios():
    ocultar_paneles()
    pw_servicios.pack()
    t9.delete("1.0",END)
    t9.update()
    t9.insert(END, "Loading...")
    t9.update()
    info = os.popen(f'powershell.exe "Get-Service"').read()
    t9.delete("1.0",END)
    t9.insert(1.0, info)

def eventlog():
    ocultar_paneles()
    pw_eventos.pack()
    t13.delete("1.0",END)
    t13.update()
    t13.insert(END, "Loading...")
    t13.update()
    info = os.popen(f'powershell.exe "Get-EventLog -LogName *"').read()
    t13.delete("1.0",END)
    t13.insert(1.0, info)

def eventos_activos():
    ocultar_paneles()
    dia=str(entrada_de_dia.get())
    evento=str(combo_eventos.get())
    pw_eventos_activos.pack()
    t14.delete("1.0",END)
    t14.update()
    t14.insert(END, "Loading...")
    t14.update()
    info = os.popen(f'powershell.exe "Get-EventLog -LogName {evento} -After (Get-Date).AddDays(-{dia}) | Select-Object TimeGenerated, Source, Message"').read()
    t14.delete("1.0",END)
    t14.insert(1.0, info)
    entrada_de_dia.delete(0, END)


def detener_servicio():
    servicio=str(entrada_de_servicio.get())
    os.system(f'powershell.exe "Stop-Service -Name {servicio}"')
    entrada_de_servicio.delete(0, END)
    servicios()

def iniciar_servicio():
    servicio=str(entrada_iniciar_Servicio.get())
    os.system(f'powershell.exe "Start-Service -Name {servicio}"')
    entrada_iniciar_Servicio.delete(0, END)
    servicios()


#------Active Directory--------#

def usuarios_de_Active_directory():
    ocultar_paneles()
    pw_usuarios_active_directory.pack()
    t6.delete("1.0",END)
    t6.update()
    t6.insert(END, "Loading...")
    t6.update()
    info = os.popen(f'powershell.exe "Get-ADUser -Filter * | Select-Object -Property Name"').read()
    t6.delete("1.0",END)
    t6.insert(1.0, info)

def grupos_de_Active_directory():
    ocultar_paneles()
    pw_grupos_active_directory.pack()
    t7.delete("1.0",END)
    t7.update()
    t7.insert(END, "Loading...")
    t7.update()
    info = os.popen(f'powershell.exe "Get-ADGroup -Filter * | Select-Object -Property Name"').read()
    t7.delete("1.0",END)
    t7.insert(1.0, info)

def crear_usuario():
    usuario=str(entrada_añadir_usuario.get())
    os.system(f'powershell.exe "New-ADUser -Name {usuario}"')
    entrada_añadir_usuario.delete(0, END)
    usuarios_de_Active_directory()

def borrar_usuario():
    usuario=str(entrada_borrar_usuario.get())
    os.system(f'powershell.exe "Remove-ADUser -Identity {usuario} -Confirm:$false"')
    entrada_borrar_usuario.delete(0, END)
    usuarios_de_Active_directory() 

def miembros():
    ocultar_paneles()
    pw_filtrado.pack()
    grupo=str(entrada_filtrar_por_grupo.get())
    t8.delete("1.0",END)
    t8.update()
    t8.insert(END, "Loading...")
    t8.update()
    info=os.popen(f'powershell.exe "Get-ADGroupMember -Identity {grupo} | Select-Object -Property Name"').read()
    print(info)
    t8.delete("1.0",END)
    t8.insert(1.0, info)
    entrada_filtrar_por_grupo.delete(0, END)
    

def Añadir_miembro_a_grupo():
    grupo=str(entrada_de_grupo.get())
    usuario=str(entrada_de_usuario.get())
    os.system(f'powershell.exe "Add-ADGroupMember -Identity "{grupo}" -Members "{usuario}""')
    entrada_de_grupo.delete(0, END)
    entrada_de_usuario.delete(0, END)
    administrar()

def Eliminar_miembro_de_grupo():
    grupo=str(entrada_de_grupo.get())
    usuario=str(entrada_de_usuario.get())
    os.system(f'powershell.exe "Remove-ADGroupMember -Identity "{grupo}" -Members "{usuario}" -Confirm:$false"')
    entrada_de_grupo.delete(0, END)
    entrada_de_usuario.delete(0, END)
    administrar()

def crear_grupo():
    grupo=str(entrada_crear_grupo.get())
    os.system(f'powershell.exe "New-ADGroup -Name {grupo} -GroupScope DomainLocal"')
    entrada_crear_grupo.delete(0, END)
    grupos_de_Active_directory()

def borrar_grupo():
    grupo=str(entrada_crear_grupo.get())
    os.system(f'powershell.exe "Remove-ADGroup -Identity {grupo} -Confirm:$false"')
    entrada_crear_grupo.delete(0, END)
    grupos_de_Active_directory()

def administrar():
    ocultar_paneles()
    pw_administrar_grupos.pack()
    t10.delete("1.0",END)
    t10.update()
    t10.insert(END, "Loading...")
    t10.update()
    info = os.popen(f'powershell.exe "Get-ADGroup -Filter * | Select-Object -Property Name"').read()
    t10.delete("1.0",END)
    t10.insert(1.0, info)


#------MAIN------#


#------VENTANA PRINCIPAL------#

raiz=Tk()
nombre_programa="XannaShell_System"
raiz.geometry("1000x700+0+0")
raiz.title(nombre_programa)
raiz.resizable(0,0)


#-------PANNED WINDOWS--------#

#------INFORMACIÓN GENERAL DEL SISTEMA--------#

pw_información_general_del_sistema = PanedWindow()
pw_información_general_del_sistema.pack(expand=True, fill='both')
pw_información_general_del_sistema.pack()
pw_información_general_del_sistema.pack_forget()
t1 = scrolledtext.ScrolledText(pw_información_general_del_sistema, height=30, width=120)
t1.pack(expand=True, fill='both')


#-------PROCESOS-------#

pw_procesos = PanedWindow()
pw_procesos.pack(expand=True, fill='both')
pw_procesos.pack()
pw_procesos.pack_forget()
t4 = scrolledtext.ScrolledText(pw_procesos, height=30, width=120)
entrada=ttk.Entry(pw_procesos)
entrada.pack()
boton = Button(pw_procesos,text="Finalizar proceso", command=finalizar_proceso)
boton.pack()

#-----CONFIGURACIÓN DE LA RED-------#

pw_red = PanedWindow()
pw_red.pack(expand=True, fill='both')
pw_red.pack()
pw_red.pack_forget()
t2 = scrolledtext.ScrolledText(pw_red, height=30, width=120)
t2.pack(expand=True, fill='both')


#------PUERTOS ABIERTOS DEL SISTEMA--------#

pw_puertos = PanedWindow()
pw_puertos.pack(expand=True, fill='both')
pw_puertos.pack()
pw_puertos.pack_forget()
t3 = scrolledtext.ScrolledText(pw_puertos, height=30, width=120)
t3.pack(expand=True, fill='both')


#-------FORMATEAR--------#

storage_devices = get_storage_devices()
pw_formatear = PanedWindow()
pw_formatear.pack(expand=True, fill='both')
pw_formatear.pack()
pw_formatear.pack_forget()
boton = Button(pw_formatear, text="FORMATEAR DISPOSITIVO", command=formateo)
combo_dispositivos = ttk.Combobox(pw_formatear, values=storage_devices, width=20)  # Ajustar el ancho de la caja desplegable
combo_dispositivos.pack()
boton.pack()
t11 = scrolledtext.ScrolledText(pw_formatear, height=30, width=120)
t11.pack(expand=True, fill='both')

#---------FORMATEO REALIZADO-------------#

pw_formateo_realizado = PanedWindow()
pw_formateo_realizado.pack(expand=True, fill='both')
pw_formateo_realizado.pack()
pw_formateo_realizado.pack_forget()
t12 = scrolledtext.ScrolledText(pw_formateo_realizado, height=30, width=120)
t12.pack(expand=True, fill='both')
boton_volver=Button(pw_formateo_realizado, text="VOLVER", command=formatear)
boton_volver.pack()

#--------SERVICIOS DEL SISTEMA------------#

pw_servicios = PanedWindow()
pw_servicios.pack(expand=True, fill='both')
pw_servicios.pack()
pw_servicios.pack_forget()
entrada_iniciar_Servicio=ttk.Entry(pw_servicios)
entrada_iniciar_Servicio.pack()
boton_levantar=Button(pw_servicios, text="Levantar servicio" ,command=iniciar_servicio)
boton_levantar.pack()
entrada_de_servicio=ttk.Entry(pw_servicios)
entrada_de_servicio.pack()
boton_parar=Button(pw_servicios, text="Detener servicio" ,command=detener_servicio)
boton_parar.pack()
t9 = scrolledtext.ScrolledText(pw_servicios, height=30, width=120)
t9.pack(expand=True, fill='both')

#------PW_DE_EVENTOS------#

get_events = get_event_type()
pw_eventos = PanedWindow()
pw_eventos.pack(expand=True, fill='both')
pw_eventos.pack()
pw_eventos.pack_forget()
combo_eventos = ttk.Combobox(pw_eventos, values=get_events, width=20)
combo_eventos.pack()
label=Label(pw_eventos, text="Días del evento")
label.pack()
entrada_de_dia=ttk.Entry(pw_eventos)
entrada_de_dia.pack()
boton_de_visualizar_evento=Button(pw_eventos, text="VISUALIZAR EVENTOS", command=eventos_activos)
boton_de_visualizar_evento.pack()
t13 = scrolledtext.ScrolledText(pw_eventos, height=30, width=120)
t13.pack(expand=True, fill='both')

#----PANEL DE LOS EVENTOS ACTIVOS--------#

pw_eventos_activos = PanedWindow()
pw_eventos_activos.pack(expand=True, fill='both')
pw_eventos_activos.pack()
pw_eventos_activos.pack_forget()
t14 = scrolledtext.ScrolledText(pw_eventos_activos, height=30, width=120)
t14.pack(expand=True, fill='both')
boton_volver=Button(pw_eventos_activos, text="VOLVER", command=eventlog)
boton_volver.pack()

#----USUARIOS DE ACTIVE DIRECTORY-----------#

pw_usuarios_active_directory = PanedWindow()
pw_usuarios_active_directory.pack(expand=True, fill='both')
pw_usuarios_active_directory.pack()
pw_usuarios_active_directory.pack_forget()
boton_añadir=Button(pw_usuarios_active_directory,text="Añadir usuario", command=crear_usuario)
entrada_añadir_usuario=ttk.Entry(pw_usuarios_active_directory)
entrada_añadir_usuario.pack()
boton_añadir.pack()
boton_borrar_usuario=Button(pw_usuarios_active_directory,text="Eliminar usuario", command=borrar_usuario)
entrada_borrar_usuario=ttk.Entry(pw_usuarios_active_directory)
entrada_borrar_usuario.pack()
boton_borrar_usuario.pack()
t6 = scrolledtext.ScrolledText(pw_usuarios_active_directory, height=30, width=120)
t6.pack(expand=True, fill='both')

#-----GRUPOS DE ACTIVE DIRECTORY--------#

#---------CREACIÓN Y ELIMINACIÓN DE GRUPO--------#
pw_grupos_active_directory = PanedWindow()
pw_grupos_active_directory.pack(expand=True, fill='both')
pw_grupos_active_directory.pack()
pw_grupos_active_directory.pack_forget()
entrada_crear_grupo=ttk.Entry(pw_grupos_active_directory)
entrada_crear_grupo.pack()
boton_crear_grupos=Button(pw_grupos_active_directory, text="Crear grupo", command=crear_grupo)
boton_crear_grupos.pack()
boton_borrar_grupos=Button(pw_grupos_active_directory, text="Eliminar grupo", command=borrar_grupo)
boton_borrar_grupos.pack()
t7 = scrolledtext.ScrolledText(pw_grupos_active_directory, height=30, width=120)
t7.pack(expand=True, fill='both')

#-------------BUSCAR MIEMBROS Y AÑADIR USUARIOS-----------#
pw_administrar_grupos=PanedWindow()
pw_administrar_grupos.pack(expand=True, fill='both')
pw_administrar_grupos.pack()
pw_administrar_grupos.pack_forget()
entrada_filtrar_por_grupo=ttk.Entry(pw_administrar_grupos)
entrada_filtrar_por_grupo.pack()
boton_filtrar=Button(pw_administrar_grupos, text="Buscar miembros de un grupo", command=miembros)
boton_filtrar.pack()
label_grupo=tk.Label(pw_administrar_grupos,text="Grupo")
label_grupo.pack()
entrada_de_grupo=ttk.Entry(pw_administrar_grupos)
entrada_de_grupo.pack()
label_usuario=tk.Label(pw_administrar_grupos,text="Usuario")
label_usuario.pack()
entrada_de_usuario=ttk.Entry(pw_administrar_grupos)
entrada_de_usuario.pack()
boton_añadir_usuario_a_grupo=Button(pw_administrar_grupos, text="Añadir usuario al grupo", command=Añadir_miembro_a_grupo)
boton_añadir_usuario_a_grupo.pack()
boton_eliminar_usuario_de_grupo=Button(pw_administrar_grupos, text="Eliminar usuario del grupo", command=Eliminar_miembro_de_grupo)
boton_eliminar_usuario_de_grupo.pack()
t10 = scrolledtext.ScrolledText(pw_administrar_grupos, height=30, width=120)
t10.pack(expand=True, fill='both')

#-----PW_FILTRADO_DE_MIEMBROS_DEL_GRUPO------#

pw_filtrado = PanedWindow()
pw_filtrado.pack(expand=True, fill='both')
pw_filtrado.pack()
pw_filtrado.pack_forget()
t8 = scrolledtext.ScrolledText(pw_filtrado, height=30, width=120)
t8.pack(expand=True, fill='both')
retorno=Button(pw_filtrado, text="VOLVER", command=administrar)
retorno.pack()

#------CONFIGURACIÓN DEL MENÚ------#

barra_de_menu = Menu(raiz)
raiz.config(menu=barra_de_menu)

Disp = Menu(barra_de_menu, tearoff=0)
Procesos = Menu(barra_de_menu, tearoff=0)
system_administration = Menu(barra_de_menu, tearoff=0)
Active_Directory=Menu(barra_de_menu, tearoff=0)
Services = Menu(barra_de_menu, tearoff=0)


#------MOSTRAR LAS BARRAS DE MENÚ-------#

barra_de_menu.add_cascade(label="Información General", menu=system_administration)
barra_de_menu.add_cascade(label="Procesos", menu=Procesos)
barra_de_menu.add_cascade(label="Servicios del sistema", menu=Services)
barra_de_menu.add_cascade(label="Dispositivos de almacenamiento", menu=Disp)
barra_de_menu.add_cascade(label="ActiveDirectory", menu=Active_Directory)


#------SUBMENUS PARA LA ADMINISTRACIÓN DEL SISTEMA--------#

system_administration.add_command(label="Características generales del sistema", command=informacion_general_del_sistema)
system_administration.add_command(label="Red del sistema", command=red)
system_administration.add_command(label="Puertos del sistema", command=puertos_abiertos)
system_administration.add_command(label="Eventos del sistema", command=eventlog)
system_administration.add_command(label="Rendimiento", command=rendimiento)

#-------SUBMENUS PARA LA ADMINISTRACIÓN DE LOS PROCESOS-------#

Procesos.add_command(label="Procesos en ejecución", command=procesos)

#-------SUBMENÚ PARA LOS DISPOSITIVOS------#

Disp.add_command(label="Formatear Volumen", command=formatear)

#--------SUBMENU PARA LOS SERVICIOS---------#

Services.add_command(label="Visualizar servicios", command=servicios)

#------SUBMENU DE ACTIVE DIRECTORY------#

Active_Directory.add_command(label="Usuarios del Dominio", command=usuarios_de_Active_directory)
Active_Directory.add_command(label="Grupos del Dominio", command=grupos_de_Active_directory)
Active_Directory.add_command(label="Administrar miembros de un grupo", command=administrar)

raiz.mainloop()
