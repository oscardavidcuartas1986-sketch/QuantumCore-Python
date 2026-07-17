#!/usr/bin/python
# -*- coding: utf-8 -*-

from tractor import Tractor
from sistema_de_riego import Sistema_de_riego
from mantenimiento import Mantenimiento
from repuesto import Repuesto 

def main():
    # Estas listas actúan como nuestra base de datos en memoria
    inventario_maquinas = []
    almacen_repuestos = [] 

    while True:
        print("\n" + "="*45)
        print("      SISTEMA DE GESTIÓN AGRÍCOLA - CEIPA")
        print("="*45)
        print("1. Registrar Maquinaria (Tractor/Riego)")
        print("2. Ver Inventario y Operaciones")
        print("3. Gestionar Almacén (Repuestos)")
        print("4. Registrar Mantenimiento")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\n--- REGISTRO DE MAQUINARIA ---")
            
            # 1. Validación del tipo de maquinaria
            while True:
                tipo = input("¿Qué desea registrar? (1: Tractor / 2: Riego): ")
                if tipo in ["1", "2"]:
                    break 
                else:
                    print("Error: Por favor, ingrese '1' para Tractor o '2' para Riego.")

            mod = input("Modelo: ")
            ser = input("S/N: ")

            # Variable temporal para aplicar polimorfismo después
            nueva_maquina = None

            # 2. Captura de atributos específicos según el tipo
            if tipo == "1":
                while True:
                    try:
                       pot = int(input("Potencia (HP): "))
                       if pot > 0:
                          break
                       print("La potencia debe ser mayor que cero.")
                    except ValueError:
                        print("Error: ingrese un numero entero valido.")
                tra = input("Tracción: ")
                hrs = float(input("Horas actuales: "))
                nueva_maquina = Tractor(mod, ser, pot, tra, hrs)
            
            elif tipo == "2":
                cau = float(input("Caudal: "))
                emi = input("Emisor: ")
                pre = float(input("Presión: "))
                nueva_maquina = Sistema_de_riego(mod, ser, cau, emi, pre)

            # 3. Validación de estado inicial (General para ambos)
            while True:
                sta = input(f"¿Está el equipo {mod} en estado operativo? (Si/No): ").strip().capitalize()
                if sta == "Si":
                    nueva_maquina.set_estado("Operativo")
                    break
                elif sta == "No":
                    nueva_maquina.set_estado("No operativo")
                    break
                else:
                    print("Opción inválida. Responda 'Si' o 'No'.")

            inventario_maquinas.append(nueva_maquina)
            print(f"{nueva_maquina.modelo} registrado con éxito.")

        elif opcion == "2":
            if not inventario_maquinas:
                print("\nInventario vacío.")
            else:
                print("\n--- EQUIPOS EN CAMPO ---")
                for i, eq in enumerate(inventario_maquinas):
                    # Aquí ocurre el polimorfismo: cada máquina sabe qué operación realizar
                    print(f"[{i}] {eq.realizar_operacion()} - Estado: {eq.estado}")

        elif opcion == "3":
            while True: # Bucle de seguridad para el submenú
                print("\n--- GESTIÓN DE ALMACÉN ---")
                print("a. Agregar nuevo repuesto")
                print("b. Ver stock actual")
                print("c. Volver al menú principal")
                sub_op = input("Seleccione una opción: ").lower().strip()
                
                if sub_op == "a":
                    nom = input("Nombre del repuesto: ")
                    cod = input("Código de pieza: ")
                    stk = int(input("Cantidad inicial: "))
                    almacen_repuestos.append(Repuesto(nom, cod, stk))
                    print("✔ Repuesto guardado con éxito.")
                    break # Salimos del bucle después de registrar
                    
                elif sub_op == "b":
                    if not almacen_repuestos:
                        print("\n El almacén está vacío.")
                    else:
                        print("\n--- STOCK DISPONIBLE ---")
                        for r in almacen_repuestos:
                            print(f"Pieza: {r.nombre} | Código: {r.codigo} | Stock: {r.get_stock()}")
                    break 
                
                elif sub_op == "c":
                    break 
                
                else:
                    print("Error: Opción no válida. Utilice una de las opciones disponibles")

        elif opcion == "4":
            if not inventario_maquinas:
                print("\n No hay máquinas para mantenimiento.")
                continue
            
            for i, eq in enumerate(inventario_maquinas):
                print(f"{i}. {eq.modelo} (S/N: {eq.get_numero_serie()} estado: {eq.estado})")
            
            idx = int(input("Ingrese numero de posicion del equipo: "))
            tipo_m = input("Tipo (Preventivo/Correctivo): ")
            desc = input("Descripción: ")
            costo = float(input("Costo: "))
            
            
            if almacen_repuestos:
                print("\n¿Se utilizó algún repuesto del almacén?")
                for i, r in enumerate(almacen_repuestos):
                    print(f"{i}. {r.nombre} (Stock: {r.get_stock()})")
                
                r_idx = input("Seleccione índice o presione Enter para omitir: ")
                
               
                if r_idx.isdigit() and int(r_idx) < len(almacen_repuestos):
                    cant = int(input("Cantidad usada: "))
                    almacen_repuestos[int(r_idx)].usar_repuesto(cant)

            # --- INTEGRACIÓN: Finalización del Registro ---
            # Creamos el objeto mantenimiento con la info capturada arriba
            m = Mantenimiento(tipo_m, desc, costo)
            
            # Lo guardamos en la lista interna de la máquina seleccionada
            inventario_maquinas[idx].mantenimientos.append(m)
            
            # Actualizamos el estado a Operativo automáticamente tras el servicio
            inventario_maquinas[idx].set_estado("Operativo")
            
            print(f"✔ Mantenimiento registrado y equipo {inventario_maquinas[idx].modelo} puesto en servicio.")
            print(f"✔ Mantenimiento {tipo_m} registrado con éxito para {inventario_maquinas[idx].modelo}.")

        elif opcion == "5":
            print("Saliendo del sistema agrícola ZAO. ¡Buen día!")
            break

# Este es el disparador que mencionamos, asegura que el programa inicie aquí
if __name__ == "__main__":
    main()