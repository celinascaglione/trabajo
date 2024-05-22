# DESDE MODELO.PY, LOGRAMOS LA CONEXIÓN CON LA BASE DE DATOS, Y LAS OPERACIONES DE CRUD QUE SE CONECTAN CON ELLA
# ASI COMO TAMBIÉN MANIPULAR EL TREEVIEW, Y LOS DECORADORES.
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import sqlite3
import os
import re
from datetime import datetime
from peewee import *
from observadores import Observador
from observadores import RAZAS_PELIGROSAS
from observadores import detectar_raza_peligrosa

from observadores import RazasPeligrosasSujeto
from tkinter import messagebox
from tkinter import StringVar
from tkinter.messagebox import askyesno, showinfo
from tkinter.messagebox import showerror
from functools import wraps
import functools

from utils import registrar_en_archivo, registro_texto, carpeta


####################BASES DE DATOS##########################################

class ConexionBD:
    def __init__(self):
        super().__init__()
        self.conexion = None
    
    def conectar(self):
        self.conexion = sqlite3.connect("mibase3.db")

    def desconectar(self):
        if self.conexion:
            self.conexion.close()

    def crear_base(self):
        try:
            self.conectar()
            self.crear_tabla2()
        except Exception as e:
            print("Error:", e)
        finally:
            self.desconectar()        

    def tabla_existe(self, nombre_tabla):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nombre_tabla}'")
        return cursor.fetchone() is not None

    def crear_tabla2(self):
        if not self.tabla_existe("petcare1"):
            cursor = self.conexion.cursor()
            sql = """CREATE TABLE petcare1
            (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, especie TEXT, raza TEXT, edad INTEGER, color TEXT, sexo TEXT, dueno TEXT NOT NULL, direccion VARCHAR NOT NULL, ciudad TEXT, tel VARCHAR(20) NOT NULL, email VARCHAR NOT NULL);"""
            cursor.execute(sql)
            self.conexion.commit()
            print("Tabla 'petcare1' creada con éxito.")
        else:
            print("La tabla 'petcare1' ya existe en la base de datos.")
################OPERACIONES CON LAS BASES DE DATOS Y CRUD############################

# DECORADORES

# Decoradores para informar operaciones
# Decorador para informar ingreso

def informar_ingreso(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        detalles = func(*args, **kwargs)
        if detalles:
            registrar_en_archivo("Ingreso de nuevo registro", detalles)
        return detalles
    return wrapper

#Decorador para informar la eliminación.
def informar_eliminacion(func):
    def wrapper(*args, **kwargs):
        detalles = func(*args, **kwargs)
        registrar_en_archivo("Eliminación de registro", detalles)
        return detalles
    return wrapper

# Decorador para informar actualización
def informar_modificacion(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        detalles = func(*args, **kwargs)
        if detalles:
            registrar_en_archivo("Modificación de registro", detalles)
        return detalles
    return wrapper

        
class OperacionesBD:
    def __init__(self, vista_principal):
        self.vista_principal = vista_principal
        self.mi_id = 0


    def crear_tabla(self):
        con = ConexionBD()
        con.crear_base()

    def set_mi_id(self, mi_id):
        self.mi_id = mi_id

    def get_mi_id(self):
        return self.mi_id
    
    @informar_ingreso
    def alta_mascota(self, nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email):
        # Expresión regular para validar teléfono (10 dígitos numéricos)
        patron_tel = r'^[\d()+\- ]+$'
        # Expresión regular para validar correo electrónico
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Validar teléfono
        if not re.match(patron_tel, tel):
            messagebox.showerror("Error", "El formato del teléfono es incorrecto.")
            return None
        
        # Validar correo electrónico
        if not re.match(patron_email, email):
            messagebox.showerror("Error", "El formato del correo electrónico es incorrecto.")
            return None

        # Si el teléfono y el correo electrónico tienen el formato correcto, proceder con la inserción en la base de datos
        con = ConexionBD()
        con.conectar()
        cursor = con.conexion.cursor()
        try:
            data = (nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email)
            sql = "INSERT INTO petcare1(nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.conexion.commit()
            messagebox.showinfo("Alta", "Registro agregado exitosamente.")
            
            # Detalles del registro para el archivo de log
            detalles = (
                f"Nombre: {nombre}, "
                f"Especie: {especie}, "
                f"Raza: {raza}, "
                f"Edad: {edad}, "
                f"Color: {color}, "
                f"Sexo: {sexo}, "
                f"Dueño: {dueno}, "
                f"Dirección: {direccion}, "
                f"Ciudad: {ciudad}, "
                f"Teléfono: {tel}, "
                f"Email: {email}"
            )
            
            return detalles
            
        except sqlite3.Error as e:
            print("Error en la inserción:", e)
            messagebox.showerror("Error", "Hubo un error al agregar el registro.")
            return None
        finally:
            con.desconectar()
    

    def actualizar_treeview(self, tree):
        con = ConexionBD()
        con.conectar()
        try:
            records = tree.get_children()
            for element in records:
                tree.delete(element)

            sql = "SELECT * FROM petcare1 ORDER BY id ASC"
            cursor = con.conexion.cursor()
            datos = cursor.execute(sql)
            resultado = datos.fetchall()
            for fila in resultado:
                tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11]))
        except sqlite3.Error as e:
            print("Error al actualizar Treeview:", e)
        finally:
            con.desconectar()


    def mostrar_resultados(self, resultados):
        if not hasattr(self, "ventana_resultados") or not self.ventana_resultados.winfo_exists():
            self.ventana_resultados = tk.Toplevel()
            self.ventana_resultados.title("Resultados de la Búsqueda")
        else:
            self.ventana_resultados.deiconify()  # Asegurarse de que la ventana esté visible
        
        resultados_label = tk.Label(self.ventana_resultados, text="Resultados de la búsqueda:\n")
        resultados_label.grid(row=0, column=0)

        for resultado in resultados:
            resultados_label.config(text=resultados_label.cget("text") + "\n" + str(resultado))



    def consultar(self, mi_id, nombre, dueno, tel):
        con = sqlite3.connect("mibase3.db")
        cursor = con.cursor()

        if mi_id:
            mi_id = int(mi_id)
        else:
            mi_id = 0

        conditions = []
        if mi_id > 0:
            conditions.append(f"id = {mi_id}")

        if nombre:
            conditions.append(f"nombre LIKE '{nombre}%'")
        
        if dueno:
            conditions.append(f"dueno LIKE '{dueno}%'")  

        if tel:
            conditions.append(f"tel = '{tel}'")

        if conditions:
            sql = "SELECT * FROM petcare1 WHERE " + " AND ".join(conditions)
        
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if resultados:
                lista_resultados = []
                for resultado in resultados:
                    if len(resultado) >= 12:
                        mensaje = ""
                        mensaje += "ID: {}\n".format(resultado[0])
                        mensaje += "Nombre: {}\n".format(resultado[1])
                        mensaje += "Especie: {}\n".format(resultado[2])
                        mensaje += "Raza: {}\n".format(resultado[3])
                        mensaje += "Edad: {}\n".format(resultado[4])
                        mensaje += "Color: {}\n".format(resultado[5])
                        mensaje += "Sexo: {}\n".format(resultado[6])
                        mensaje += "Dueño: {}\n".format(resultado[7])
                        mensaje += "Dirección: {}\n".format(resultado[8])
                        mensaje += "Ciudad: {}\n".format(resultado[9])
                        mensaje += "Teléfono: {}\n".format(resultado[10])
                        mensaje += "Email: {}\n".format(resultado[11])
                        lista_resultados.append(mensaje)
                    else:
                        lista_resultados.append("Registro incompleto")
                self.mostrar_resultados(lista_resultados)
            else:
                self.mostrar_resultados(["No se encontraron resultados para la búsqueda."])
        else:
            self.mostrar_resultados(["No se especificaron criterios de búsqueda válidos."])
        con.close()
   
    @informar_modificacion
    def modificar(self, mi_id, nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email, tree):
        con = ConexionBD()  # Crear una instancia de la clase ConexionBD
        try:
            con.conectar()  # Conectar a la base de datos

            cursor = con.conexion.cursor()
            
            # Obtener los datos antes de la actualización
            datos_anteriores = self.cargar_datos_por_id(mi_id)

            # Realizar la actualización
            data = (nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email, mi_id)
            sql = "UPDATE petcare1 SET nombre=?, especie=?, raza=?, edad=?, color=?, sexo=?, dueno=?, direccion=?, ciudad=?, tel=?, email=? WHERE id=?"
            cursor.execute(sql, data)
            con.conexion.commit()  # Confirmar la transacción

            # Obtener los datos actualizados después de la actualización
            datos_actuales = self.cargar_datos_por_id(mi_id)

            # Formatear los detalles para el registro
            detalles = f"ID: {mi_id}\n"
            detalles += f"Datos anteriores:\n{self.formato_datos(datos_anteriores)}\n"
            detalles += f"Datos actualizados:\n{self.formato_datos(datos_actuales)}"

            # Registrar la operación en el archivo de registro
            registrar_en_archivo("Modificación de registro", detalles)
            detectar_raza_peligrosa(raza)

            print("Registro actualizado exitosamente.")
            self.actualizar_treeview(tree)

        except sqlite3.Error as e:
            print("Error al modificar el registro:", e)
            con.conexion.rollback()  # Retroceder la transacción en caso de error
        finally:
            con.desconectar()  # Desconectar de la base de datos

        #return detalles  # Retornar los detalles para el registro

    def cargar_datos_por_id(self, mi_id):
        con = ConexionBD()  # Crear una instancia de la clase ConexionBD
        con.conectar()  # Conectar a la base de datos
        cursor = con.conexion.cursor()
        data = (mi_id,)
        sql = "SELECT * FROM petcare1 WHERE id = ?;"
        cursor.execute(sql, data)
        con.conexion.commit()
        rows = cursor.fetchall()
        con.desconectar()  # Desconectar de la base de datos
        return rows
    
    def formato_datos(self, datos):
        # Función para formatear los datos de la base de datos en una cadena legible
        if not datos:
            return "Registro no encontrado"
        
        mensaje = ""
        mensaje += f"ID: {datos[0][0]}\n"
        mensaje += f"Nombre: {datos[0][1]}\n"
        mensaje += f"Especie: {datos[0][2]}\n"
        mensaje += f"Raza: {datos[0][3]}\n"
        mensaje += f"Edad: {datos[0][4]}\n"
        mensaje += f"Color: {datos[0][5]}\n"
        mensaje += f"Sexo: {datos[0][6]}\n"
        mensaje += f"Dueño: {datos[0][7]}\n"
        mensaje += f"Dirección: {datos[0][8]}\n"
        mensaje += f"Ciudad: {datos[0][9]}\n"
        mensaje += f"Teléfono: {datos[0][10]}\n"
        mensaje += f"Email: {datos[0][11]}\n"
        
        return mensaje


    def cargar_datos(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        con = ConexionBD()  # Crear una instancia de la clase ConexionBD
        con.conectar()  # Conectar a la base de datos
        cursor = con.conexion.cursor()
        data = (mi_id,)
        sql = "SELECT * FROM petcare1 WHERE id =?;"
        cursor.execute(sql, data)
        con.conexion.commit()
        rows = cursor.fetchall()
        return rows

    @informar_eliminacion
    def eliminar_registro(self, mi_id):
        try:
            con = ConexionBD()  # Crear una instancia de la clase ConexionBD
            con.conectar()  # Conectar a la base de datos
            
            # Obtener los datos del registro antes de eliminarlo
            cursor = con.conexion.cursor()
            cursor.execute("SELECT * FROM petcare1 WHERE id = ?;", (mi_id,))
            datos_registro = cursor.fetchone()
            
            if datos_registro:
                # Asumimos que la estructura de datos_registro es (id, nombre, especie, raza, edad, color, sexo, dueno, direccion, ciudad, tel, email)
                detalles = (
                    f"ID: {datos_registro[0]}, "
                    f"Nombre: {datos_registro[1]}, "
                    f"Especie: {datos_registro[2]}, "
                    f"Raza: {datos_registro[3]}, "
                    f"Edad: {datos_registro[4]}, "
                    f"Color: {datos_registro[5]}, "
                    f"Sexo: {datos_registro[6]}, "
                    f"Dueño: {datos_registro[7]}, "
                    f"Dirección: {datos_registro[8]}, "
                    f"Ciudad: {datos_registro[9]}, "
                    f"Teléfono: {datos_registro[10]}, "
                    f"Email: {datos_registro[11]}"
                )

                # Eliminar el registro de la base de datos
                cursor.execute("DELETE FROM petcare1 WHERE id = ?;", (mi_id,))
                con.conexion.commit()
                    
                print(f"Registro con ID {mi_id} eliminado correctamente.")
                return detalles
               
        except sqlite3.Error as e:
            print(f"Error al eliminar el registro: {e}")
        finally:
            con.desconectar()  # Desconectar de la base de datos
