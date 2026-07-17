#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

# --- PILAR: ABSTRACCIÓN ---
class Maquinaria(ABC):
    # El constructor DEBE recibir modelo y serie
    def __init__(self, modelo, serie): 
        self.modelo = modelo
        # PILAR: ENCAPSULAMIENTO (Privado con __)
        self.__serie = serie  
        self.estado = "Operativo"
        self.mantenimientos = [] # Relación 1 a *

    # METODO GETTER
    def get_numero_serie(self):
        return self.__serie

    # METODO SETTER
    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    @abstractmethod
    def realizar_operacion(self):
        """Método que las hijas deben implementar (Polimorfismo)"""
        pass