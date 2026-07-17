#!/usr/bin/python
# -*- coding: utf-8 -*-

from maquinaria import Maquinaria


class Sistema_de_riego(Maquinaria):
    def __init__(self, modelo, serie, caudal, emisor, presion):
        # Herencia: modelo y serie heredados de la clase madre(Maquinaria)
        super().__init__(modelo, serie)
        self.caudal = caudal
        self.emisor = emisor
        # Antes se asignaba directo con self.presion = presion, lo que permitía
        # crear el equipo con una presión fuera de rango de seguridad.
        # Ahora la presión inicial pasa por el mismo setter validado.
        self.presion = None
        self.set_presion(presion)

    def realizar_operacion(self):
        return f"El sistema {self.modelo} (S/N: {self.get_numero_serie()}) irrigado por {self.emisor} a {self.presion} bar"

    def get_presion(self):
        return self.presion
    
    def set_presion(self, nueva_presion):
        if 0 <= nueva_presion <= 12:
            self.presion = nueva_presion
        else:
            print("Peligro, presion excediendo limites de seguridad")


# #---PRUEBAS DE SOFTWARE---      
# mi_riego = Sistema_de_riego("Hunter-Eco", "DEF-002", 15.5, "Goteo", 3.2)
# print(mi_riego.realizar_operacion())
# mi_riego.set_presion(4.5)
# print(f"Nueva presion: {mi_riego.get_presion()} bar")