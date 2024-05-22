#DESDE CONTROLADOR SE LANZA LA APP, Y DONDE SE INICIA EL SERVIDOR CONJUNTAMENTE CON EL LANZAMIENTO DE LA APLICACIÓN.

import tkinter as tk
from tkinter import ttk
from vista import VistaPrincipal
from modelo import OperacionesBD
import threading
from servidor import iniciar_servidor

class Controlador:
    def __init__(self):
        self.root = tk.Tk()
        self.vista_principal = VistaPrincipal(self.root, self)
        self.operaciones_bd = OperacionesBD(self.vista_principal)
    
    def iniciar_servidor(self):
        servidor_thread = threading.Thread(target=iniciar_servidor, daemon=True)
        servidor_thread.start()

    def iniciar_aplicacion(self):
        self.vista_principal.create_gui()
        self.iniciar_servidor()  
        self.root.mainloop()
        self.tree = self.vista_principal.tree


if __name__ == '__main__':
    app = Controlador()
    app.iniciar_aplicacion()

