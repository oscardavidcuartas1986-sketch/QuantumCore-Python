
def leer_y_almacenar_datos(nombre_archivo):
    lista_transacciones = []


    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            partes = linea.split(",")

            if len(partes) == 3:
                transaccion_dict = {
                    "cliente_id": partes[0],
                    "tipo": partes[1],
                    "monto": float(partes[2])
                }

                lista_transacciones.append(transaccion_dict)

    return lista_transacciones


def calcular_monto_total(lista_transacciones):
    total_monto = 0

    for transaccion in lista_transacciones:
        total_monto += transaccion["monto"]

    return total_monto



def filtrar_por_tipo(lista_transacciones, tipo_a_filtrar):
    lista_filtrada = []

    for transaccion in lista_transacciones:
        if transaccion["tipo"] == tipo_a_filtrar:
            lista_filtrada.append(transaccion)

    return lista_filtrada


def ejecutar_sistema():
    nombre_archivo = "transacciones.txt"

    datos_cargados = leer_y_almacenar_datos(nombre_archivo)

    print("\n    INICIO PROCESAMIENTO DE IMPUTO \n")

    print(f"Total de registros cargados: {len(datos_cargados)}")
    
    total = calcular_monto_total(datos_cargados)
    print(f"\nMonto Total de todas las transacciones: ${total:,.2f}")

    creditos = filtrar_por_tipo(datos_cargados, "CREDITO")

    print("\n    Resultado del Filtrado \n")
    print(f"Transacciones de CREDITO encontradas: {len(creditos)}")

    for transaccion in creditos:
        print(
            f"  > Cliente {transaccion['cliente_id']} / "
            f"Monto: ${transaccion['monto']:,.2f}"
        )

    print("\n     FIN DEL PROCESO \n")


ejecutar_sistema()