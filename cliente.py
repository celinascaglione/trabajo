#AQUÍ UN EJEMPLO DONDE UN CLIENTE HIPOTÉTICO LE MANDA AL SERVIDOR UNA PETICIÓN DE TURNO PARA CASTRAR A SU MASCOTA. 
#EN LOG_SERVIDOR.TXT SE DEJA CONSTANCIA DE QUE EL SERVIDOR RECIBE LA PETICIÓN. EN EL CMD, EN EL DIRECTORIO DE ESTE ARCHIVO,ESCRIBIENDO PYTHON CLIENTE.PY, PODREMOS VER LA RESPUESTA DEL SERVIDOR.
import socket

def solicitar_turno():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('192.168.1.4', 5000)) 

    mensaje = "Solicito un turno para castración"
    cliente.send(mensaje.encode())

    respuesta = cliente.recv(1024).decode()
    print(f"Respuesta del servidor: {respuesta}")

    cliente.close()

if __name__ == "__main__":
    solicitar_turno()
