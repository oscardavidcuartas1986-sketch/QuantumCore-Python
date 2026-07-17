#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importamos la clase madre
from maquinaria import Maquinaria

# HERENCIA
class Tractor(Maquinaria):
    def __init__(self, modelo, serie, potencia, traccion, horas):
        # HERENCIA - atributos modelo y serie se agregan a la clase tractor, proveninetes de la clase madre(Maquinaria)
        super().__init__(modelo,serie)
        
        # Atributos especificos de la clase hija
        self.potencia = potencia
        self.traccion = traccion
        self.horas = horas

    def realizar_operacion(self):
        return f"El tractor {self.modelo} (S/N: {self.get_numero_serie()}) arando con potencia {self.potencia} HP"

    def get_horas(self):
        return self.horas
    
    def set_horas(self, nuevas_horas):
        if nuevas_horas >= self.horas:
            self.horas = nuevas_horas
        else:
            print("Alerta: Las horas de motor no pueden disminuir")


# # #---PRUEBAS DE SOFTWARE---
# mi_tractor = Tractor("5065E", "ABC-001", 65, "4x4", 250)
# print(mi_tractor.realizar_operacion())
# print(f"Numero de serie: {mi_tractor.get_numero_serie()}")
# print(mi_tractor.set_horas(300.5))
# print(f"Nuevas horas: {mi_tractor.get_horas()}")
