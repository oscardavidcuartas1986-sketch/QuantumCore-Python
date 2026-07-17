import os

class TransaccionBase:

    def __init__(self, cliente_id, tipo, monto):
        self._cliente_id = cliente_id
        self._tipo = tipo
        self._monto = float(monto)

    @property
    def cliente_id(self):
        return self._cliente_id

    @cliente_id.setter
    def cliente_id(self, nuevo_id):
        self._cliente_id = nuevo_id

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, nuevo_tipo):
        self._tipo = nuevo_tipo

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, nuevo_monto):
        if nuevo_monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        self._monto = nuevo_monto

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

    def calcular_impacto(self):
        # Placeholder: cada subclase DEBE sobreescribir este
        # método con su propia lógica. Si alguna hija no lo
        # hace, mejor que reviente aquí a que devuelva un
        # número inventado.
        raise NotImplementedError(
            "Las subclases deben implementar calcular_impacto()"
        )

# CLASES HIJAS (Extensión)
class TransaccionCredito(TransaccionBase):

    # Tasa de interés aplicada a las transacciones de crédito.
    TASA_INTERES = 0.02  # 2%

    def __init__(self, cliente_id, monto):
        super().__init__(cliente_id, "CREDITO", monto)

    def calcular_impacto(self):
        # El "impacto" de un crédito es el interés que genera
        # sobre el monto de la transacción.
        return self.monto * self.TASA_INTERES


class TransaccionDebito(TransaccionBase):

    # Comisión fija cobrada por cada transacción de débito,
    # sin importar el monto que se mueva.
    COMISION_FIJA = 1000.0  # $1.000 COP

    def __init__(self, cliente_id, monto):
        super().__init__(cliente_id, "DEBITO", monto)

    def calcular_impacto(self):
        # El "impacto" de un débito es una comisión fija.
        return self.COMISION_FIJA


# ============================================================
# FÁBRICA
# Función auxiliar para crear la subclase correcta según el
# tipo que venga del archivo o del usuario. La agrego para que
# el resto del programa no tenga que saber que ahora existen
# subclases: solo le pide una Transaccion a esta función.
# ============================================================
def crear_transaccion(cliente_id, tipo, monto):

    tipo = tipo.upper()

    if tipo == "CREDITO":
        return TransaccionCredito(cliente_id, monto)

    elif tipo == "DEBITO":
        return TransaccionDebito(cliente_id, monto)

    else:
        raise ValueError(f"Tipo de transacción inválido: {tipo}")


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

                    transaccion = crear_transaccion(
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


def agregar_transaccion(lista_transacciones):

    print("\n===== NUEVA TRANSACCIÓN =====")

    # Validar que el ID no exista
    while True:

        cliente = input("Ingrese el ID del cliente: ").upper()

        existe = False

        for transaccion in lista_transacciones:
            if transaccion.cliente_id.upper() == cliente:
                existe = True
                print("\nERROR: Ese ID de cliente ya existe.")
                print("Ingrese un ID diferente.\n")
                break

        if not existe:
            break

    # Seleccionar tipo
    while True:

        print("\nSeleccione el tipo:")
        print("1. DEBITO")
        print("2. CREDITO")

        opcion = input("Opción: ")

        if opcion == "1":
            tipo = "DEBITO"
            break

        elif opcion == "2":
            tipo = "CREDITO"
            break

        else:
            print("Opción inválida.")

    # Ingresar monto
    while True:

        try:
            monto = float(input("Ingrese el monto: "))

            if monto > 0:
                break
            else:
                print("El monto debe ser mayor que cero.")

        except ValueError:
            print("Ingrese un número válido.")

    nueva = crear_transaccion(cliente, tipo, monto)

    lista_transacciones.append(nueva)

    guardar_transacciones(lista_transacciones)

    print("\nCliente agregado correctamente.")


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
        print("5. Agregar cliente")
        print("6. Ver impacto por transacción")
        print("7. Salir")

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

            agregar_transaccion(datos)

        elif opcion == "6":

            print(
                "\n===== IMPACTO POR TRANSACCIÓN =====\n"
            )

            for transaccion in datos:

                # Misma llamada, resultado distinto según la
                # clase real del objeto: esto es polimorfismo.
                impacto = transaccion.calcular_impacto()

                etiqueta = (
                    "Interés generado"
                    if transaccion.tipo == "CREDITO"
                    else "Comisión cobrada"
                )

                print(
                    f"Cliente: {transaccion.cliente_id} | "
                    f"Tipo: {transaccion.tipo} | "
                    f"{etiqueta}: ${impacto:,.2f}"
                )

        elif opcion == "7":

             print("\nPrograma finalizado.")

             break

        else:

            print(
                "\nOpción no válida."
            )

        input(
            "\nPresione ENTER para continuar..."
        )


menu()