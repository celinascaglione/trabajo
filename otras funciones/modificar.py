import tkinter as tk
from tkinter import ttk

# para boton eliminar:
from tkinter.messagebox import *
from tkinter.messagebox import askyesno, showinfo

root = tk.Tk()
tree = ttk.Treeview(root)


mi_id = 0

root = tk.Tk()

var_nombre = tk.StringVar()
var_especie = tk.StringVar()
var_raza = tk.StringVar()
var_edad = tk.StringVar()
var_color = tk.StringVar()
var_sexo = tk.StringVar()
var_dueno = tk.StringVar()
var_direccion = tk.StringVar()
var_ciudad = tk.StringVar()
var_tel = tk.StringVar()
var_email = tk.StringVar()


nombre = tk.Label(root, text="Nombre de la mascota")
nombre.grid(row=0, column=0)

especie = tk.Label(root, text="Especie")
especie.grid(row=1, column=0)

raza = tk.Label(root, text="Raza")
raza.grid(row=2, column=0)

edad = tk.Label(root, text="Edad")
edad.grid(row=3, column=0)

color = tk.Label(root, text="Color")
color.grid(row=4, column=0)

sexo = tk.Label(root, text="Sexo")
sexo.grid(row=5, column=0)

# opcion macho o hembra con check list? o boton?

dueno = tk.Label(root, text="Nombre Completo del Dueño")
dueno.grid(row=6, column=0)

direccion = tk.Label(root, text="Dirección")
direccion.grid(row=7, column=0)

ciudad = tk.Label(root, text="Ciudad")
ciudad.grid(row=8, column=0)

tel = tk.Label(root, text="Teléfono de contacto")
tel.grid(row=9, column=0)

email = tk.Label(root, text="Email de contacto")
email.grid(row=10, column=0)


entry_nombre = tk.Entry(root, textvariable=var_nombre, width=30)
entry_nombre.grid(row=0, column=1)

entry_especie = tk.Entry(root, textvariable=var_especie, width=30)
entry_especie.grid(row=1, column=1)

entry_raza = tk.Entry(root, textvariable=var_raza, width=30)
entry_raza.grid(row=2, column=1)

entry_edad = tk.Entry(root, textvariable=var_edad, width=30)
entry_edad.grid(row=3, column=1)

entry_color = tk.Entry(root, textvariable=var_color, width=30)
entry_color.grid(row=4, column=1)

entry_sexo = tk.Entry(root, textvariable=var_sexo, width=30)
entry_sexo.grid(row=5, column=1)

entry_dueno = tk.Entry(root, textvariable=var_dueno, width=30)
entry_dueno.grid(row=6, column=1)

entry_direccion = tk.Entry(root, textvariable=var_direccion, width=30)
entry_direccion.grid(row=7, column=1)

entry_ciudad = tk.Entry(root, textvariable=var_ciudad, width=30)
entry_ciudad.grid(row=8, column=1)

entry_tel = tk.Entry(root, textvariable=var_tel, width=30)
entry_tel.grid(row=9, column=1)

entry_email = tk.Entry(root, textvariable=var_email, width=30)
entry_email.grid(row=10, column=1)  # acá se le puede poner el atributo sticky=W


def funcion_m():
    if askyesno("ALERTA", "Usted está por MODIFICAR un registro"):
        global mi_id
        item = tree.focus()
        tree.delete(item)
        mi_id -= 1
        showinfo("MODIFICADO", "El registro de modificado exitosamente.")
    else:
        showinfo("No modificado", "No se ha modificado el registro.")


boton_m = tk.Button(root, text="Modificar", command=funcion_m)
boton_m.grid(row=11, column=1)


def funcion_g():
    print("Hola")


boton_g = tk.Button(root, text="Guardar", command=funcion_g)
boton_g.grid(row=12, column=1)

tree = ttk.Treeview(root)
tree["columns"] = (
    "col1",
    "col2",
    "col3",
    "col4",
    "col5",
    "col6",
    "col7",
    "col8",
    "col9",
    "col10",
    "col11",
    "col12",
)
tree.column("col1", width=80, minwidth=80, anchor="w")
tree.column("col2", width=80, minwidth=80, anchor="w")
tree.column("col3", width=100, minwidth=100, anchor="w")
tree.column("col4", width=50, minwidth=50, anchor="w")
tree.column("col5", width=50, minwidth=50, anchor="w")
tree.column("col6", width=50, minwidth=50, anchor="w")
tree.column("col7", width=50, minwidth=50, anchor="w")
tree.column("col8", width=50, minwidth=50, anchor="w")
tree.column("col9", width=50, minwidth=50, anchor="w")
tree.column("col10", width=50, minwidth=50, anchor="w")
tree.column("col11", width=50, minwidth=50, anchor="w")
tree.column("col12", width=50, minwidth=50, anchor="w")


root.mainloop()
