#AQUÍ EL SERVIDOR.PY RECIBE DE UN HIPOTETICO CLIENTE LA SOLICITUD PARA TURNOS PARA CASTRA MASCOTAS.
# EL CLIENTE RECIBE UN MENSAJE. LA RECEPCION DEL PEDIDO DE TURNO SE REGISTRA EN LOG_SERVIDOR.TXT, EN FORMA AUTOMÁTICA.

import socket

LOG_ARCHIVO = "log_servidor.txt"  # Nombre del archivo de log personalizado

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 5000))
    servidor.listen(5)
    print("Servidor iniciado y esperando conexiones...")

    while True:
        cliente, direccion = servidor.accept()
        print(f"Conexión establecida con {direccion}")
        
        mensaje = cliente.recv(1024).decode()
        print(f"Mensaje recibido: {mensaje}")
        
        # Guardar el mensaje recibido en el archivo de log personalizado
        guardar_log(mensaje)
        
        respuesta = "Los turnos para castraciones se dan por WhatsApp al 3416562387, de lunes a viernes de 8 a 18hs."
        cliente.send(respuesta.encode())
        cliente.close()

def guardar_log(mensaje):
    with open(LOG_ARCHIVO, "a") as archivo:
        archivo.write(f"Mensaje recibido: {mensaje}\n")

if __name__ == "__main__":
    iniciar_servidor()
