#CÓDIGO PARA OBSERVADORES, SE REGISTRAN LAS RAZAS PELIGROSAS AUTOMÁTICAMENTE CUANDO EN EL CAMPO RAZA,
# SE OBSERVA EL NOMBRE DE ALGUNA DE ELLAS. Y SE REGISTRA EN RAZAS_PELIGROSAS.TXT

import os
from datetime import datetime

import tkinter as tk

from utils import registrar_en_archivo, registro_texto, carpeta


class RazasPeligrosasSujeto:
    def __init__(self):
        self._observadores = []
        self.razas_peligrosas = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        for observador in self._observadores:
            observador.actualizar(mensaje)

    def set_razas_peligrosas(self, razas):
        self.razas_peligrosas = razas
        self.notificar_observadores("Se han actualizado las razas peligrosas.")
        registrar_en_archivo("Actualización de razas peligrosas", "\n".join(razas))
        print("Razas peligrosas actualizadas:", razas) 

    def get_razas_peligrosas(self):
        return self.razas_peligrosas

class Observador:
    def actualizar(self, mensaje):
        raise NotImplementedError("Los observadores deben implementar el método 'actualizar'.")

class RazasPeligrosasObserver(Observador):
    def __init__(self):
        super().__init__()

    def actualizar(self, mensaje):
        print("Observador notificado con mensaje:", mensaje)
        if mensaje == "Se han actualizado las razas peligrosas.":
            razas_peligrosas = sujeto_razas.get_razas_peligrosas()
            detalles = "\n".join(razas_peligrosas)
            registrar_en_archivo("Actualización de razas peligrosas", detalles)

# Instanciar el sujeto y el observador
sujeto_razas = RazasPeligrosasSujeto()
observador_razas = RazasPeligrosasObserver()
sujeto_razas.agregar_observador(observador_razas)

class Sujeto:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        for observador in self._observadores:
            observador.actualizar(mensaje)

class InterfazUsuario(Observador):
    def __init__(self, ui_element):
        self.ui_element = ui_element

    def actualizar(self, mensaje):
        self.ui_element.mostrar_mensaje(mensaje)

RAZAS_PELIGROSAS = ["Pit Bull", "Rottweiler", "Dogo Argentino", "Fila Brasileiro", "Tosa Inu", "Akita Inu", "American Staffordshire Terrier", "Staffordshire Bull Terrier", "Doberman"]

def detectar_raza_peligrosa(raza):
    if raza in RAZAS_PELIGROSAS:
        registrar_raza_peligrosa(raza)

def registrar_raza_peligrosa(raza):
    try:
        with open("razas_peligrosas.txt", "a") as archivo:
            archivo.write(f"Raza peligrosa detectada: {raza}\n")
    except Exception as e:
        print(f"Error al registrar raza peligrosa: {e}")