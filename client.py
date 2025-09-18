import socket

# Configuración del cliente
SERVER_IP = '192.168.1.18'  # Cambia esto por la IP del servidor
PORT = 5000

# Crear socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print("Conectado al servidor.")

while True:
    mensaje = input("Escribe un mensaje: ")
    client_socket.sendall(mensaje.encode())

    data = client_socket.recv(1024)
    print("Respuesta del servidor:", data.decode())
