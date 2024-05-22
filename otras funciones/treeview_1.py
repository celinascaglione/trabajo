import tkinter as tk
from tkinter import ttk

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
dueno.grid(row=0, column=3)

direccion = tk.Label(root, text="Dirección")
direccion.grid(row=1, column=3)

ciudad = tk.Label(root, text="Ciudad")
ciudad.grid(row=2, column=3)

tel = tk.Label(root, text="Teléfono de contacto")
tel.grid(row=3, column=3)

email = tk.Label(root, text="Email de contacto")
email.grid(row=4, column=3)


entry_nombre = tk.Entry(root, textvariable=var_nombre, width=50)
entry_nombre.grid(row=0, column=1)

entry_especie = tk.Entry(root, textvariable=var_especie, width=50)
entry_especie.grid(row=1, column=1)

entry_raza = tk.Entry(root, textvariable=var_raza, width=50)
entry_raza.grid(row=2, column=1)

entry_edad = tk.Entry(root, textvariable=var_edad, width=50)
entry_edad.grid(row=3, column=1)

entry_color = tk.Entry(root, textvariable=var_color, width=50)
entry_color.grid(row=4, column=1)

entry_sexo = tk.Entry(root, textvariable=var_sexo, width=50)
entry_sexo.grid(row=5, column=1)

entry_dueno = tk.Entry(root, textvariable=var_dueno, width=50)
entry_dueno.grid(row=0, column=4)

entry_direccion = tk.Entry(root, textvariable=var_direccion, width=50)
entry_direccion.grid(row=1, column=4)

entry_ciudad = tk.Entry(root, textvariable=var_ciudad, width=50)
entry_ciudad.grid(row=2, column=4)

entry_tel = tk.Entry(root, textvariable=var_tel, width=50)
entry_tel.grid(row=3, column=4)

entry_email = tk.Entry(root, textvariable=var_email, width=50)
entry_email.grid(row=4, column=4)  # acá se le puede poner el atributo sticky=W


def funcion_g():
    global mi_id
    mi_id += 1
    tree.insert(
        "",
        "end",
        text=str(mi_id),
        values=(
            var_nombre.get(),
            var_especie.get(),
            var_raza.get(),
            var_edad.get(),
            var_color.get(),
            var_sexo.get(),
            var_dueno.get(),
            var_direccion.get(),
            var_ciudad.get(),
            var_tel.get(),
            var_email.get(),
        ),
    )


boton_g = tk.Button(root, text="Guardar", command=funcion_g)
boton_g.grid(row=5, column=4)


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
)
tree.column("#0", width=70, minwidth=50, anchor="w")
tree.column("col1", width=130, minwidth=100, anchor="w")
tree.column("col2", width=130, minwidth=100, anchor="w")
tree.column("col3", width=130, minwidth=100, anchor="w")
tree.column("col4", width=70, minwidth=50, anchor="w")
tree.column("col5", width=130, minwidth=100, anchor="w")
tree.column("col6", width=50, minwidth=50, anchor="w")
tree.column("col7", width=130, minwidth=100, anchor="w")
tree.column("col8", width=130, minwidth=100, anchor="w")
tree.column("col9", width=90, minwidth=80, anchor="w")
tree.column("col10", width=130, minwidth=100, anchor="w")
tree.column("col11", width=130, minwidth=100, anchor="w")


tree.heading("#0", text="ID")
tree.heading("col1", text="NOMBRE MASCOTA")
tree.heading("col2", text="ESPECIE")
tree.heading("col3", text="RAZA")
tree.heading("col4", text="EDAD")
tree.heading("col5", text="COLOR")
tree.heading("col6", text="SEXO")
tree.heading("col7", text="NOMBRE DEL DUEÑO")
tree.heading("col8", text="DIRECCIÓN")
tree.heading("col9", text="CIUDAD")
tree.heading("col10", text="TEL")
tree.heading("col11", text="EMAIL")


tree.grid(column=0, row=12, columnspan=12)


root.mainloop()


# para boton eliminar:
# def funcion_e():
# global mi_id
# item = tree.focus()
# print(item)
# tree.delete(item)
# mi_id -=1

# boton_e = tk.Button(root, text="Eliminar", command=funcion_g)
# boton_e.grid(row=11, column=1)
