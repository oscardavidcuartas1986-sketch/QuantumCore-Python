#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date

class Mantenimiento:
    def __init__(self, tipo, descripcion, costo):
        self.tipo = tipo
        self.descripcion = descripcion
        self.costo = costo
        # Se usa date.today() para que el sistema asigne la fecha actual automáticamente
        self.fecha = date.today() 

# # --- PRUEBAS DE SOFTWARE (Punto 5) ---
# m = Mantenimiento("Preventivo", "Cambio de filtros", 250000)
# print(f"Fecha: {m.fecha} | Tipo: {m.tipo} | Costo: {m.costo}")
