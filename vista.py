#A TRAVÉS DE VISTA.PY LOGRAMOS ENLAZAR LOS DOS MODULOS DE MODELO.PY Y CONTROLADOR.PY, ES LA VISTA DE LA APLICACIÓN
#PODREMOS MANIPULAR LA BASE DE DATOS A TRAVÉS DE LOS BOTONES QUE ENCONTRAMOS, ASÍ COMO TAMBIÉN SALIR DE LA APP.

#IMPORTAMOS LAS LIBRERIAS QUE NECESITAMOS Y LOS MODULOS CON LOS MÉTODOS QUE NECESITAMOS PARA QUE FUNCIONE.
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk

from tkinter import PhotoImage

from tkinter.ttk import Treeview

import os
import sqlite3

from pathlib import Path
from tkinter import Button, Entry, Label, Scrollbar, StringVar, Toplevel
from tkinter import Scrollbar

from tkinter.messagebox import askyesno, showinfo
from tkinter.messagebox import showerror
from tkinter import messagebox

from modelo import OperacionesBD
from modelo import ConexionBD


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(
            self.tooltip,
            text=self.text,
            background="lightyellow",
            relief="solid",
            borderwidth=1,
        )
        label.grid(row=0, column=0)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None



#AQUÍ ESTRUCTURAMOS LO QUE VAMOS A VER EN LA APP, LOS BOTONES, LOS ENTRY, LOGOS E IMÁGENES Y EL TREEVIEW
            
class VistaPrincipal:
    ventana_busqueda = None
    boton_buscar = None
    resultados_label = None
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.mi_id = 0
        self.operaciones_bd = OperacionesBD(self)
        self.conexion_bd = ConexionBD()
        
        self.var_nombre = tk.StringVar()
        self.var_especie = tk.StringVar()
        self.var_raza = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_color = tk.StringVar()
        self.var_sexo = tk.StringVar()
        self.var_dueno = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_ciudad = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_email = tk.StringVar()
        
        
        self.configurar_ventana_principal()
        
        self.create_gui()
        self.logo_loaded = False
        self.header_frame = self.create_header_frame() 
    
        self.tree = None
        self.resultados_consulta = []


    def ingresar_nuevo_registro(self):
        # Limpiar ventana o realizar otras acciones antes de agregar un nuevo registro
        self.limpiar_ventana()  # Por ejemplo, limpiar los campos del formulario

        # Desplazar la ventana al primer campo de entrada (nombre)
        self.entry_nombre.focus_set()


    def actualizar_treeview(self, tree):
        self.operaciones_bd.actualizar_treeview(tree)

    def consultar(self, mi_id, nombre, dueno, tel):
        operaciones_bd = OperacionesBD(self.root)
        resultados = operaciones_bd.consultar(mi_id, nombre, dueno, tel)
        
        
    def limpiar_ventana(self):
        self.var_nombre.set("")
        self.var_especie.set("")
        self.var_raza.set("")
        self.var_edad.set("")
        self.var_color.set("")
        self.var_sexo.set("")
        self.var_dueno.set("")
        self.var_direccion.set("")
        self.var_ciudad.set("")
        self.var_tel.set("")
        self.var_email.set("")

    
    
    def mostrar_datos_en_ventana(self, datos):
        if datos is not None:  # Verificar si datos no es None
            ventana_datos = tk.Toplevel(self.root)
            ventana_datos.title("Datos de la Mascota")
            etiquetas = ["ID", "Nombre", "Especie", "Raza", "Edad", "Color", "Sexo", "Dueño", "Dirección", "Ciudad", "Teléfono", "Email"]
            
            if len(datos) >= len(etiquetas):
                for i, etiqueta in enumerate(etiquetas):
                    tk.Label(ventana_datos, text=etiqueta).grid(row=i, column=0)
                    tk.Label(ventana_datos, text=datos[i]).grid(row=i, column=1)
            else: 
                tk.Label(ventana_datos, text="Datos insuficientes").grid(row=0, column=0)
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron resultados para la búsqueda.")

        
       
    def create_frame(self, parent, row, column, rowspan, columnspan):
        frame = tk.Frame(parent, borderwidth=2, relief="ridge")
        frame.grid(
            row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10
            )
        return frame

    def configurar_ventana_principal(self):
        self.root.geometry("1200x600")
        self.root.title("PET CARE")

    def create_gui(self):
        self.cargar_imagenes()
        self.limpiar_ventana() 
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=6)
        button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)


        boton_ingresar = tk.Button(
            button_frame, image=self.imagen_ingresar, command=self.ingresar_nuevo_registro, width=30, height=30
        )
        boton_modificar = tk.Button(
            button_frame, image=self.imagen_modificar, command=self.accion_modificar, width=30, height=30
        )
        boton_eliminar = tk.Button(
            button_frame, image=self.imagen_eliminar, command=self.accion_eliminar, width=30, height=30
        )
        self.boton_buscar_principal = tk.Button(
            button_frame, image=self.imagen_buscar, command=self.mostrar_ventana_busqueda, width=30, height=30
        )

        boton_salir = tk.Button(
            button_frame, image=self.imagen_salir, command=lambda: self.root.quit(), width=30, height=30
        )
        boton_guardar = tk.Button(
            self.root,
            text="Guardar",
            command=self.funcion_g,
            activebackground="green",
            font=("courier", 8, "bold"),
        )

        boton_ingresar.grid(row=2, column=0, padx=10)
        boton_modificar.grid(row=2, column=1, padx=10)
        boton_eliminar.grid(row=2, column=2, padx=10)
        self.boton_buscar_principal.grid(row=2, column=3, padx=10)
        boton_salir.grid(row=2, column=4, padx=10)
        boton_guardar.grid(row=9, column=5)


        ToolTip(boton_ingresar, "Ingresar nuevo registro")
        ToolTip(boton_modificar, "Modificar")
        ToolTip(boton_eliminar, "Eliminar un registro")
        ToolTip(self.boton_buscar_principal, "Buscar un registro")
        ToolTip(boton_salir, "Salir de la aplicación")
        ToolTip(boton_guardar, "Guardar nuevo registro")
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.grid(row=12, column=0, columnspan=6, padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=(
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
            ),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        self.tree.column("#0", width=70, minwidth=50, anchor="w")
        self.tree.column("col1", width=130, minwidth=100, anchor="w")
        self.tree.column("col2", width=130, minwidth=100, anchor="w")
        self.tree.column("col3", width=130, minwidth=100, anchor="w")
        self.tree.column("col4", width=70, minwidth=50, anchor="w")
        self.tree.column("col5", width=130, minwidth=100, anchor="w")
        self.tree.column("col6", width=50, minwidth=50, anchor="w")
        self.tree.column("col7", width=130, minwidth=100, anchor="w")
        self.tree.column("col8", width=130, minwidth=100, anchor="w")
        self.tree.column("col9", width=90, minwidth=80, anchor="w")
        self.tree.column("col10", width=130, minwidth=100, anchor="w")
        self.tree.column("col11", width=130, minwidth=100, anchor="w")


        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="NOMBRE MASCOTA")
        self.tree.heading("col2", text="ESPECIE")
        self.tree.heading("col3", text="RAZA")
        self.tree.heading("col4", text="EDAD")
        self.tree.heading("col5", text="COLOR")
        self.tree.heading("col6", text="SEXO")
        self.tree.heading("col7", text="NOMBRE DEL DUEÑO")
        self.tree.heading("col8", text="DIRECCIÓN")
        self.tree.heading("col9", text="CIUDAD")
        self.tree.heading("col10", text="TEL")
        self.tree.heading("col11", text="EMAIL")

        self.actualizar_treeview(self.tree)
            
        
    
    def create_header_frame(self):
        header_frame = self.create_frame(self.root, 0, 0, 2, 6)
        if not self.logo_loaded:
            trabajo = os.path.dirname(os.path.abspath(__file__))
            ruta_logo = os.path.join(trabajo, "img", "logopet.png")
            logo1 = Image.open(ruta_logo)
            logo2 = logo1.resize((200, 200), Image.BILINEAR)
            
            self.logo_image = ImageTk.PhotoImage(logo2)
            self.logo_loaded = True
        logoimg = tk.Label(header_frame, image=self.logo_image)
        logoimg.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
       
    

        petcare = tk.Label(

        header_frame,
        text="CLINICA VETERINARIA PET CARE",
        foreground="green",
        font=("courier", 22, "bold"),
        )
        petcare.grid(row=1, column=0, columnspan=5)

        espacio_vacio = tk.Label(self.root, text="", height=3)
        espacio_vacio.grid(row=2, column=0)

        self.tree.bind("<<TreeviewSelect>>", self.on_item_selection)


        nombre = tk.Label(
            self.root, text="Nombre de la mascota", foreground="green", font=("courier", 12, "bold")
        )
        nombre.grid(row=4, column=0)

        especie = tk.Label(self.root, text="Especie", font=("courier", 12, "bold"))
        especie.grid(row=5, column=0)

        raza = tk.Label(self.root, text="Raza", foreground="green", font=("courier", 12, "bold"))
        raza.grid(row=6, column=0)

        edad = tk.Label(self.root, text="Edad", font=("courier", 12, "bold"))
        edad.grid(row=7, column=0)

        color = tk.Label(self.root, text="Color", foreground="green", font=("courier", 12, "bold"))
        color.grid(row=8, column=0)

        sexo = tk.Label(self.root, text="Sexo", font=("courier", 12, "bold"))
        sexo.grid(row=9, column=0)

        dueno = tk.Label(
            self.root,
            text="Nombre Completo del Dueño",
            foreground="green",
            font=("courier", 12, "bold"),
        )
        dueno.grid(row=4, column=4)

        direccion = tk.Label(self.root, text="Dirección", font=("courier", 12, "bold"))
        direccion.grid(row=5, column=4)

        ciudad = tk.Label(self.root, text="Ciudad", foreground="green", font=("courier", 12, "bold"))
        ciudad.grid(row=6, column=4)

        tel = tk.Label(self.root, text="Teléfono de contacto", font=("courier", 12, "bold"))
        tel.grid(row=7, column=4)

        email = tk.Label(
            self.root, text="Email de contacto", foreground="green", font=("courier", 12, "bold")
        )
        email.grid(row=8, column=4)


        entry_nombre = tk.Entry(self.root, textvariable=self.var_nombre, width=50)
        entry_nombre.grid(row=4, column=1)
        self.entry_nombre = entry_nombre

        entry_especie = tk.Entry(self.root, textvariable=self.var_especie, width=50)
        entry_especie.grid(row=5, column=1)

        entry_raza = tk.Entry(self.root, textvariable=self.var_raza, width=50)
        entry_raza.grid(row=6, column=1)

        entry_edad = tk.Entry(self.root, textvariable=self.var_edad, width=50)
        entry_edad.grid(row=7, column=1)

        entry_color = tk.Entry(self.root, textvariable=self.var_color, width=50)
        entry_color.grid(row=8, column=1)

        entry_sexo = tk.Entry(self.root, textvariable=self.var_sexo, width=50)
        entry_sexo.grid(row=9, column=1)

        entry_dueno = tk.Entry(self.root, textvariable=self.var_dueno, width=50)
        entry_dueno.grid(row=4, column=5)

        entry_direccion = tk.Entry(self.root, textvariable=self.var_direccion, width=50)
        entry_direccion.grid(row=5, column=5)

        entry_ciudad = tk.Entry(self.root, textvariable=self.var_ciudad, width=50)
        entry_ciudad.grid(row=6, column=5)

        entry_tel = tk.Entry(self.root, textvariable=self.var_tel, width=50)
        entry_tel.grid(row=7, column=5)

        entry_email = tk.Entry(self.root, textvariable=self.var_email, width=50)
        entry_email.grid(row=8, column=5)  

   
    def load_logo_image(self):
        
        pass    
  
    def cargar_imagenes(self):
        trabajo = os.path.dirname(os.path.abspath(__file__))
        self.ruta0 = os.path.join(trabajo, "img", "agregar6.png")       
        self.ruta1 = os.path.join(trabajo, "img", "editar.png")
        self.ruta2 = os.path.join(trabajo, "img", "delete.png")
        self.ruta3 = os.path.join(trabajo, "img", "buscar3.png")
        self.ruta5 = os.path.join(trabajo, "img", "salir6.png")
        
        self.imagen_ingresar = self.redimensionar_imagen(self.ruta0)
        self.imagen_modificar = self.redimensionar_imagen(self.ruta1)
        self.imagen_eliminar = self.redimensionar_imagen(self.ruta2)
        self.imagen_buscar = self.redimensionar_imagen(self.ruta3)
        self.imagen_salir = self.redimensionar_imagen(self.ruta5)
    
        
    def redimensionar_imagen(self, ruta):
        imagen1 = Image.open(ruta)
        imagen2 = imagen1.resize((30, 30), Image.BILINEAR)  # Redimensionar a 30x30
        return ImageTk.PhotoImage(imagen2)   
    

   
    def cargar_datos(self, tree, mi_id):
        self.conexion_bd.crear_base()
        con = self.conexion_bd.conexion
        cursor = con.cursor()
        data = (mi_id,)
        sql = "SELECT * FROM petcare1 WHERE id = ?;"
        cursor.execute(sql, data)
        row = cursor.fetchone()
        if row:
            self.mostrar_datos_en_ventana(row)
        else:
            print("Registro no encontrado")

        con.close()



    def funcion_g(self):
        # Obtener los datos del formulario
        nombre = self.var_nombre.get()
        especie = self.var_especie.get()
        raza = self.var_raza.get()
        edad = self.var_edad.get()
        color = self.var_color.get()
        sexo = self.var_sexo.get()
        dueno = self.var_dueno.get()
        direccion = self.var_direccion.get()
        ciudad = self.var_ciudad.get()
        tel = self.var_tel.get()
        email = self.var_email.get()

        try:
            # Llamar al método alta_mascota de OperacionesBD para agregar el registro
            operaciones_bd = OperacionesBD(self)  # Pasar la vista principal al modelo
            operaciones_bd.alta_mascota(nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email)
            # Limpiar ventana
            self.limpiar_ventana()
            self.actualizar_treeview(self.tree)
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el registro: {e}")

    
    

    def obtener_datos_de_treeview(self, item):  # CAMBIOS(self, tree, item)
        mi_id = self.tree.item(item, "text")   # CAMBIOS tree.item(item, "text")
        valores = self.tree.item(item, "values")  # CAMBIOS tree.item(item, "values")
        if valores:
            datos = list(valores)
        else:
            datos = [""] * len(self.tree["columns"])   #CAMBIOS len(tree["columns"])
        return [mi_id] + datos
    
    def on_item_selection(self, event):
        item = self.tree.focus()
        if item:
            datos = self.obtener_datos_de_treeview(item)       
            self.mostrar_datos_en_ventana(datos)
            print("Datos del ítem seleccionado:", datos)
        else:
            print("No se encontraron datos para el ítem seleccionado.")

    #CON TOOLTIP PODREMOS OBSERVAR PARA QUÉ SIRVE CADA BOTÓN QUE TENEMOS CONECTADOS AL CRUD, CON IMÁGENES
    #DE ESTA MANERA APARECE COMO INFORMACION ADICIONAL AL PASAR EL CURSOR SOBRE ELLOS        
   
    def accion_modificar(self):
    
        item = self.tree.focus()
        if not item:
            showinfo("Error", "Seleccione un registro para modificar.")
            return

        if askyesno("Alerta", "¿Está seguro de que desea modificar este registro?"):
            datos_actuales = self.obtener_datos_de_treeview(item)
      

            if len(datos_actuales) >= 12:
                mi_id = datos_actuales[0] 
                self.ventana_edicion = tk.Toplevel(self.root)
                self.ventana_edicion.title("Editar Registro")
                self.var_nombre_edit = tk.StringVar(value=datos_actuales[1])
                self.var_especie_edit = tk.StringVar(value=datos_actuales[2])
                self.var_raza_edit = tk.StringVar(value=datos_actuales[3])
                self.var_edad_edit = tk.StringVar(value=datos_actuales[4])
                self.var_color_edit = tk.StringVar(value=datos_actuales[5])
                self.var_sexo_edit = tk.StringVar(value=datos_actuales[6])
                self.var_dueno_edit = tk.StringVar(value=datos_actuales[7])
                
                self.var_direccion_edit = tk.StringVar(value=datos_actuales[8])
                self.var_ciudad_edit = tk.StringVar(value=datos_actuales[9])
                self.var_tel_edit = tk.StringVar(value=datos_actuales[10])
                self.var_email_edit = tk.StringVar(value=datos_actuales[11])

                nombre_edit = tk.Label(self.ventana_edicion, text="Nombre de la mascota")
                nombre_edit.grid(row=0, column=0)
                entry_nombre_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_nombre_edit, width=50)
                entry_nombre_edit.grid(row=0, column=1)
    
                especie_edit = tk.Label(self.ventana_edicion, text="Especie")
                especie_edit.grid(row=1, column=0)
                entry_especie_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_especie_edit, width=50)
                entry_especie_edit.grid(row=1, column=1)

                raza_edit = tk.Label(self.ventana_edicion, text="Raza")
                raza_edit.grid(row=2, column=0)
                entry_raza_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_raza_edit, width=50)
                entry_raza_edit.grid(row=2, column=1)
    
                edad_edit = tk.Label(self.ventana_edicion, text="Edad")
                edad_edit.grid(row=3, column=0)
                entry_edad_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_edad_edit, width=50)
                entry_edad_edit.grid(row=3, column=1)

                color_edit = tk.Label(self.ventana_edicion, text="Color")
                color_edit.grid(row=4, column=0)
                entry_color_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_color_edit, width=50)
                entry_color_edit.grid(row=4, column=1)

                sexo_edit = tk.Label(self.ventana_edicion, text="Sexo")
                sexo_edit.grid(row=5, column=0)
                entry_sexo_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_sexo_edit, width=50)
                entry_sexo_edit.grid(row=5, column=1)

                dueno_edit = tk.Label(self.ventana_edicion, text="Nombre del dueño")
                dueno_edit.grid(row=6, column=0)
                entry_dueno_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_dueno_edit, width=50)
                entry_dueno_edit.grid(row=6, column=1)

                direccion_edit = tk.Label(self.ventana_edicion, text="Dirección")
                direccion_edit.grid(row=7, column=0)
                entry_direccion_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_direccion_edit, width=50)
                entry_direccion_edit.grid(row=7, column=1)

                ciudad_edit = tk.Label(self.ventana_edicion, text="Ciudad")
                ciudad_edit.grid(row=8, column=0)
                entry_ciudad_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_ciudad_edit, width=50)
                entry_ciudad_edit.grid(row=8, column=1)

                tel_edit = tk.Label(self.ventana_edicion, text="Teléfono")
                tel_edit.grid(row=9, column=0)
                entry_tel_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_tel_edit, width=50)
                entry_tel_edit.grid(row=9, column=1)

                email_edit = tk.Label(self.ventana_edicion, text="Email")
                email_edit.grid(row=10, column=0)
                entry_email_edit = tk.Entry(self.ventana_edicion, textvariable=self.var_email_edit, width=50)
                entry_email_edit.grid(row=10, column=1)
    
                guardar_cambios = tk.Button(self.ventana_edicion, text="Guardar Cambios", command=self.guardar_cambios)
                guardar_cambios.grid(row=11, column=1, columnspan=2)
   
            else:
                showinfo("Datos Insuficientes", "Los datos del registro seleccionado son insuficientes para la edición.")
        else:
            showinfo("No modificado", "No se ha modificado el registro.")
        

    

    def guardar_cambios(self):
        item = self.tree.focus()
        if not item:
            print("No se ha seleccionado un registro para editar.")
            return

        mi_id, *datos_actuales = self.obtener_datos_de_treeview(item)
        print("ID del registro:", mi_id)
        print("Datos actuales:", datos_actuales)

        nuevo_nombre = self.var_nombre_edit.get()
        nuevo_especie = self.var_especie_edit.get()
        nuevo_raza = self.var_raza_edit.get()
        nuevo_edad = self.var_edad_edit.get()
        nuevo_color = self.var_color_edit.get()
        nuevo_sexo = self.var_sexo_edit.get()
        nuevo_dueno = self.var_dueno_edit.get()
        nuevo_direccion = self.var_direccion_edit.get()
        nuevo_ciudad = self.var_ciudad_edit.get()
        nuevo_tel = self.var_tel_edit.get()
        nuevo_email = self.var_email_edit.get()

        if (nuevo_nombre != datos_actuales[1] or
            nuevo_especie != datos_actuales[2] or
            nuevo_raza != datos_actuales[3] or
            nuevo_edad != datos_actuales[4] or
            nuevo_color != datos_actuales[5] or
            nuevo_sexo != datos_actuales[6] or
            nuevo_dueno != datos_actuales[7] or
            nuevo_direccion != datos_actuales[8] or
            nuevo_ciudad != datos_actuales[9] or
            nuevo_tel != datos_actuales[10] or
            nuevo_email != datos_actuales[11]):

            operaciones_bd = OperacionesBD(self)
            operaciones_bd.modificar(
                mi_id,
                nuevo_nombre,
                nuevo_especie,
                nuevo_raza,
                nuevo_edad,
                nuevo_color,
                nuevo_sexo,
                nuevo_dueno,
                nuevo_direccion,
                nuevo_ciudad,
                nuevo_tel,
                nuevo_email,
                self.tree
            )
           
            # Actualizar los valores del ítem en el treeview
            if self.tree.exists(item):
                self.tree.item(item, values=(mi_id, nuevo_nombre, nuevo_especie, nuevo_raza, nuevo_edad, nuevo_color, nuevo_sexo, nuevo_dueno, nuevo_direccion, nuevo_ciudad, nuevo_tel, nuevo_email))
        
            if self.ventana_edicion:
                self.ventana_edicion.destroy()
            
    def actualizar_dato_en_base_de_datos(self, id, columna, nuevo_valor):
        try:
            con = sqlite3.connect("mibase3.db")
            cursor = con.cursor()
            
            sql = f"UPDATE petcare1 SET {columna}=? WHERE id=?"
            cursor.execute(sql, (nuevo_valor, id))
            
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"Error al actualizar el dato en la base de datos: {e}")

    def accion_eliminar(self):
        item = self.tree.focus()
        if not item:
            showinfo("Error", "Seleccione un registro para eliminar.")
            return
        if askyesno("Alerta", "¿Está seguro de que desea eliminar este registro?"):
            mi_id = self.tree.item(item)['text']
            operaciones_bd = OperacionesBD(self)  # Crear una instancia de OperacionesBD
            operaciones_bd.eliminar_registro(mi_id)  # Llamar a la función eliminar_registro()
            self.tree.delete(item)
            showinfo("Eliminado", "El registro se ha eliminado exitosamente.")
        else:
            showinfo("No eliminado", "No se ha eliminado el registro.")
  
    def mostrar_ventana_busqueda(self):
        self.ventana_busqueda = tk.Toplevel(self.root)
        self.ventana_busqueda.title("Ventana de Búsqueda")

        label_mi_id = tk.Label(self.ventana_busqueda, text="Id:")
        entry_mi_id = tk.Entry(self.ventana_busqueda)

        label_nombre = tk.Label(self.ventana_busqueda, text="Nombre mascota:")
        entry_nombre = tk.Entry(self.ventana_busqueda)

        label_dueno = tk.Label(self.ventana_busqueda, text="Nombre Dueño:")
        entry_dueno = tk.Entry(self.ventana_busqueda)

        label_tel = tk.Label(self.ventana_busqueda, text="Telefono de contacto:")
        entry_tel = tk.Entry(self.ventana_busqueda)

        self.resultados_label = tk.Label(self.ventana_busqueda, text="")
        
        
        def realizar_busqueda():
            resultados = self.consultar(entry_mi_id.get(), entry_nombre.get(), entry_dueno.get(), entry_tel.get())

        boton_buscar = tk.Button(
            self.ventana_busqueda,
            text="Buscar",
            command=realizar_busqueda
        )

        label_mi_id.grid(row=0, column=0)
        entry_mi_id.grid(row=0, column=1)

        label_nombre.grid(row=1, column=0)
        entry_nombre.grid(row=1, column=1)

        label_dueno.grid(row=2, column=0)
        entry_dueno.grid(row=2, column=1)

        label_tel.grid(row=3, column=0)
        entry_tel.grid(row=3, column=1)

        self.resultados_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        boton_buscar.grid(row=4, column=0, columnspan=2)
        