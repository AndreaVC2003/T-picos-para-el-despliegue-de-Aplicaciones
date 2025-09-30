import socket
import threading

class ServidorChat:
    def __init__(self, host='localhost', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.clientes = []     # Lista de sockets de clientes
        self.ejecutando = True

    def iniciar_servidor(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((self.host, self.puerto))
        servidor.listen(5)

        print(f"Servidor iniciado en {self.host}:{self.puerto}")

        while self.ejecutando:
            cliente, direccion = servidor.accept()
            print(f"Conexión establecida con {direccion}")
            self.clientes.append(cliente)

            hilo = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            hilo.daemon = True
            hilo.start()

    def manejar_cliente(self, cliente):
        try:
            while True:
                data = cliente.recv(1024)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                print("Mensaje recibido:", mensaje)
                self.broadcast(mensaje, cliente)
        except:
            pass
        finally:
            if cliente in self.clientes:
                self.clientes.remove(cliente)
            cliente.close()
            print("Cliente desconectado")

    def broadcast(self, mensaje, remitente):
        """Envía el mensaje a todos menos al remitente"""
        for cliente in self.clientes:
            if cliente != remitente:
                try:
                    cliente.send(mensaje.encode('utf-8'))
                except:
                    cliente.close()
                    if cliente in self.clientes:
                        self.clientes.remove(cliente)

if __name__ == "__main__":
    servidor = ServidorChat()
    try:
        servidor.iniciar_servidor()
    except KeyboardInterrupt:
        print("\nServidor detenido")
