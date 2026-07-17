import os


class Transaccion:

    def __init__(self, cliente_id, tipo, monto):
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.monto = float(monto)

    def obtener_informacion(self):
        return (
            f"Cliente: {self.cliente_id} | "
            f"Tipo: {self.tipo} | "
            f"Monto: ${self.monto:,.2f}"
        )

    def validar_tipo(self):
        return self.tipo in ["DEBITO", "CREDITO"]

    def modificar_tipo(self, nuevo_tipo):
        self.tipo = nuevo_tipo

    def modificar_monto(self, nuevo_monto):
        self.monto = float(nuevo_monto)


def leer_y_almacenar_datos(nombre_archivo="transacciones.txt"):

    ruta = os.path.join(
        os.path.dirname(__file__),
        nombre_archivo
    )

    lista_transacciones = []

    try:

        with open(ruta, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                partes = linea.strip().split(",")

                if len(partes) == 3:

                    transaccion = Transaccion(
                        partes[0],
                        partes[1],
                        partes[2]
                    )

                    lista_transacciones.append(
                        transaccion
                    )

    except FileNotFoundError:

        print(
            "\nERROR: No se encontró el archivo "
            "transacciones.txt"
        )

    return lista_transacciones


def guardar_transacciones(
    lista_transacciones,
    nombre_archivo="transacciones.txt"
):

    ruta = os.path.join(
        os.path.dirname(__file__),
        nombre_archivo
    )

    with open(ruta, "w", encoding="utf-8") as archivo:

        for transaccion in lista_transacciones:

            archivo.write(
                f"{transaccion.cliente_id},"
                f"{transaccion.tipo},"
                f"{transaccion.monto}\n"
            )


def calcular_monto_total(lista_transacciones):

    total = 0

    for transaccion in lista_transacciones:
        total += transaccion.monto

    return total


def mostrar_transacciones(lista_transacciones):

    print("\n===== LISTA DE TRANSACCIONES =====\n")

    for transaccion in lista_transacciones:
        print(
            transaccion.obtener_informacion()
        )


def filtrar_por_tipo(
    lista_transacciones,
    tipo_a_filtrar
):

    resultado = []

    for transaccion in lista_transacciones:

        if transaccion.tipo == tipo_a_filtrar:
            resultado.append(transaccion)

    return resultado


def modificar_transaccion(lista_transacciones):

    cliente = input(
        "\nIngrese el ID del cliente: "
    ).upper()

    for transaccion in lista_transacciones:

        if transaccion.cliente_id.upper() == cliente:

            print("\nTransacción encontrada:")
            print(
                transaccion.obtener_informacion()
            )

            while True:

                print("\nSeleccione el nuevo tipo:")
                print("1. DEBITO")
                print("2. CREDITO")

                opcion = input("Opción: ")

                if opcion == "1":
                    nuevo_tipo = "DEBITO"
                    break

                elif opcion == "2":
                    nuevo_tipo = "CREDITO"
                    break

                else:
                    print(
                        "Opción inválida."
                    )

            nuevo_monto = float(
                input(
                    "Ingrese el nuevo monto: "
                )
            )

            transaccion.modificar_tipo(
                nuevo_tipo
            )

            transaccion.modificar_monto(
                nuevo_monto
            )

            guardar_transacciones(
                lista_transacciones
            )

            print(
                "\nTransacción actualizada "
                "y guardada."
            )

            return

    print("\nCliente no encontrado.")


def menu():

    while True:

        datos = leer_y_almacenar_datos()

        print("\n")
        print("=" * 40)
        print(" SISTEMA DE TRANSACCIONES ")
        print("=" * 40)

        print("1. Ver transacciones")
        print("2. Ver créditos")
        print("3. Calcular monto total")
        print("4. Modificar transacción")
        print("5. Salir")

        opcion = input(
            "\nSeleccione una opción: "
        )

        if opcion == "1":

            mostrar_transacciones(datos)

        elif opcion == "2":

            creditos = filtrar_por_tipo(
                datos,
                "CREDITO"
            )

            print(
                "\n===== TRANSACCIONES DE CRÉDITO =====\n"
            )

            for transaccion in creditos:

                print(
                    transaccion.obtener_informacion()
                )

        elif opcion == "3":

            total = calcular_monto_total(
                datos
            )

            print(
                f"\nMonto Total: "
                f"${total:,.2f}"
            )

        elif opcion == "4":

            modificar_transaccion(datos)

        elif opcion == "5":

            print(
                "\nPrograma finalizado."
            )

            break

        else:

            print(
                "\nOpción no válida."
            )

        input(
            "\nPresione ENTER para continuar..."
        )


menu()