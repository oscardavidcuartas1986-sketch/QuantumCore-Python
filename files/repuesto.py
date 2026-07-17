#!/usr/bin/python
# -*- coding: utf-8 -*-

class Repuesto:
    def __init__(self, nombre, codigo, stock_inicial):
        self.nombre = nombre
        self.codigo = codigo
        self.__stock = stock_inicial 

    def get_stock(self):
        """Devuelve la cantidad disponible"""
        return self.__stock

    def set_stock(self, cantidad):
        """Actualiza el stock asegurando que no sea negativo"""
        if cantidad >= 0:
            self.__stock = cantidad
        else:
            print(f"Error: No se puede asignar un stock negativo a {self.nombre}")

    def usar_repuesto(self, unidades):
        """Resta unidades del stock si hay suficientes"""
        if unidades <= self.__stock:
            self.__stock -= unidades
            print(f"Se usaron {unidades} unidades de {self.nombre}.")
        else:
            print(f"Stock insuficiente de {self.nombre} (Disponibles: {self.__stock})")

# --- PRUEBAS DE SOFTWARE ---
# filtro = Repuesto("Filtro de Aceite", "P-101", 10)
# filtro.set_stock(15)
# print(f"Repuesto: {filtro.nombre} | Stock actual: {filtro.get_stock()}")