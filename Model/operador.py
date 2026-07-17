#!/usr/bin/python
# -*- coding: utf-8 -*-

class Operador:
    def __init__(self, nombre, id_empleado):
        self.nombre = nombre
        self.identificacion = id_empleado
        self.equipo_asignado = None #Variable creada para guardar el objeto maquinaria 

    def get_identificacion(self):
        return self.identificacion
    
    def asignar_equipo(self, maquina):
        self.equipo_asignado = maquina

    def realizar_trabajo(self):
        if self.equipo_asignado:
            return f"Operador {self.nombre} informa: {self.equipo_asignado.realizar_operacion()}"
        else:
            return f"El operador {self.nombre} no tiene equipo asignado actualmente."

# --- PRUEBAS DE SOFTWARE (Punto 5) ---
# from tractor import Tractor
# op = Operador("Camilo Perez", "ID-1020")
# trac = Tractor("JD-5090", "TR-77", 90, "4x4", 100)
# op.asignar_maquina(trac)
# print(op.realizar_labor())