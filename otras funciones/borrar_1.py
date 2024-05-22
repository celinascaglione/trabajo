# para boton eliminar:
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.messagebox import askyesno, showinfo

root = tk.Tk()
tree = ttk.Treeview(root)


def funcion_e():
    if askyesno("Alerta", "Usted está por eliminar un registro"):
        global mi_id
        item = tree.focus()
        tree.delete(item)
        mi_id -= 1
        showinfo("Eliminado", "El registro de ha eliminado exitosamente.")
    else:
        showinfo("No eliminado", "No se ha eliminado el registro.")


boton_e = tk.Button(root, text="Eliminar", command=funcion_e)
boton_e.grid(row=11, column=1)


# mensaje de verificacion


root.mainloop()
