#Cliente de Chat con Tkinter + Sockets
# - Permite conectarse a un servidor de chat.
# - Soporta mensajes generales y privados.
# - Interfaz gráfica con lista de usuarios conectados.
# - Muestra notificaciones de usuarios y mensajes nuevos.


# 🔹 Importamos librerías necesarias
import tkinter as tk
from tkinter import ttk, messagebox   
import threading                      
import time                          


class ClienteChat:
    """
    Cliente de chat con interfaz gráfica.
    - Maneja la conexión con el servidor vía sockets.
    - Soporta chat general y privado.
    - Incluye notificaciones en tiempo real.
    """


    #Constructor: inicializa variables y lanza ventana de conexión

    def __init__(self):
        # Conexión
        self.socket_cliente = None
        self.conectado = False
        self.nombre_usuario = ""
        self.host_servidor = ""
        self.puerto_servidor = 12345

        # Interfaz
        self.root = None
        self.usuarios_listbox = None
        self.chat_text = None
        self.mensaje_entry = None
        self.destinatario_var = None
        self.combo_destinatario = None
        self.ventana_notificacion = None

        # Almacenamiento de mensajes
        self.mensajes_privados = {}     # {usuario: [mensajes]}
        self.mensajes_generales = []    # Lista de mensajes del chat general
        self.usuarios_con_mensajes_nuevos = set()  # Para marcar con 🔴

        # Mostrar ventana de conexión
        self.mostrar_ventana_conexion()



    # Ventana de conexión (inicio del programa)

    def mostrar_ventana_conexion(self):
        ventana_conexion = tk.Tk()
        ventana_conexion.title("🔗 Conectar al Chat")
        ventana_conexion.geometry("400x300")
        ventana_conexion.resizable(False, False)
        ventana_conexion.eval('tk::PlaceWindow . center')

        # Título
        titulo = tk.Label(ventana_conexion, text="💬 Cliente de Chat", 
                         font=("Arial", 16, "bold"))
        titulo.pack(pady=20)

        # Campos
        frame_campos = tk.Frame(ventana_conexion)
        frame_campos.pack(pady=20, padx=40, fill="x")

        # Nombre
        tk.Label(frame_campos, text="👤 Nombre de usuario:", font=("Arial", 10)).pack(anchor="w")
        self.entry_nombre = tk.Entry(frame_campos, font=("Arial", 12))
        self.entry_nombre.pack(fill="x", pady=(5, 15))

        # IP
        tk.Label(frame_campos, text="🌐 IP del servidor:", font=("Arial", 10)).pack(anchor="w")
        self.entry_ip = tk.Entry(frame_campos, font=("Arial", 12))
        self.entry_ip.insert(0, "localhost")
        self.entry_ip.pack(fill="x", pady=(5, 15))

        # Puerto
        tk.Label(frame_campos, text="🔌 Puerto del servidor:", font=("Arial", 10)).pack(anchor="w")
        self.entry_puerto = tk.Entry(frame_campos, font=("Arial", 12))
        self.entry_puerto.insert(0, "12345")
        self.entry_puerto.pack(fill="x", pady=(5, 15))

        # Botón conectar
        btn_conectar = tk.Button(frame_campos, text="🚀 Conectar", 
                               font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white",
                               command=lambda: self.intentar_conexion(ventana_conexion))
        btn_conectar.pack(pady=20, fill="x")

        # Permitir Enter para conectar
        ventana_conexion.bind('<Return>', lambda e: self.intentar_conexion(ventana_conexion))  
        ventana_conexion.mainloop()



    # Intenta conectar al servidor con los datos ingresados

    def intentar_conexion(self, ventana_conexion):
        nombre = self.entry_nombre.get().strip()
        ip = self.entry_ip.get().strip()
        puerto = self.entry_puerto.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "Por favor ingresa tu nombre de usuario")
            return
        if not ip:
            ip = "localhost"
        try:
            puerto = int(puerto) if puerto else 12345
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido")
            return

        # Guardar datos
        self.nombre_usuario = nombre
        self.host_servidor = ip
        self.puerto_servidor = puerto

        # Intentar conectar
        if self.conectar_servidor():
            ventana_conexion.destroy()
            self.mostrar_ventana_chat()
        else:
            messagebox.showerror("Error de Conexión", 
                               "No se pudo conectar al servidor.\n"
                               "Verifica que esté ejecutándose y los datos sean correctos.")



    # Crea socket y envía comando CONNECT

    def conectar_servidor(self):
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect((self.host_servidor, self.puerto_servidor))

            # Enviar solicitud de conexión
            comando_conexion = f"CONNECT|{self.nombre_usuario}"
            self.socket_cliente.send(comando_conexion.encode('utf-8'))

            # Esperar respuesta
            respuesta = self.socket_cliente.recv(1024).decode('utf-8')
            if respuesta.startswith("SUCCESS"):
                self.conectado = True

                # Hilo para escuchar mensajes en segundo plano
                hilo_recibir = threading.Thread(target=self.recibir_mensajes)
                hilo_recibir.daemon = True
                hilo_recibir.start()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error conectando: {e}")
            return False



    # Ventana principal del chat (solo si se conecta)

    def mostrar_ventana_chat(self):
        self.root = tk.Tk()
        self.root.title(f"💬 Chat - {self.nombre_usuario}")
        self.root.geometry("800x600")

        # Crear interfaz
        self.crear_interfaz_chat()

        # Pedir lista de usuarios e historial
        self.solicitar_usuarios()
        self.solicitar_historial()

        # Actualizar lista de usuarios periódicamente
        self.actualizar_usuarios_periodicamente()

        # Cerrar correctamente al salir
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.root.mainloop()
