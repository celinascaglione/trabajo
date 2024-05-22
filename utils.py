#ARCHIVO AUXILIAR CON EL CÓDIGO NECESARIO PARA REGISTRAR LO QUE REALIZAN LOS DECORADORES, EN EL ARCHIVO REGUSTRO.
import os
from datetime import datetime

def registro_texto():
    directorio_actual = os.getcwd()
    nuevo_directorio = "registro"
    ruta_nueva_carpeta = os.path.join(directorio_actual, nuevo_directorio)
    
    if not os.path.exists(ruta_nueva_carpeta):
        os.makedirs(ruta_nueva_carpeta)
    
    return ruta_nueva_carpeta

def registrar_en_archivo(accion, detalles):
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    hora_actual = datetime.now().strftime('%H:%M:%S')
    archivo = f"{fecha_actual}.txt"
    carpeta_registros = registro_texto()
    ruta_archivo = os.path.join(carpeta_registros, archivo)
    
    registro = f"{fecha_actual} {hora_actual} - {accion}: \n"
    registro += f"Detalles del registro:\n{detalles}\n\n"

    with open(ruta_archivo, 'a') as f:
        f.write(registro)

def carpeta():
    try:
        directorio_actual = os.getcwd()
        nuevo_directorio = "registro"  # Nombre de la carpeta donde se guardarán los registros
        ruta_nueva_carpeta = os.path.join(directorio_actual, nuevo_directorio)
        
        if not os.path.exists(ruta_nueva_carpeta):
            os.makedirs(ruta_nueva_carpeta)
        
        return ruta_nueva_carpeta
    except Exception as e:
        print(f"Error al crear la carpeta 'registro': {e}")
        return None
