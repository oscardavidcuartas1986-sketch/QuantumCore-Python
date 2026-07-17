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
        tipos_validos = [
            "CREDITO",
            "DEBITO",
            "TRANSFERENCIA",
            "PAGO",
            "RETIRO"
        ]
        return self.tipo in tipos_validos


def leer_y_almacenar_datos(nombre_archivo="transacciones.txt"):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)

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

                    lista_transacciones.append(transaccion)

    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo: {ruta}")

    return lista_transacciones


def calcular_monto_total(lista_transacciones):
    total = 0

    for transaccion in lista_transacciones:
        total += transaccion.monto

    return total


def filtrar_por_tipo(lista_transacciones, tipo_a_filtrar):
    resultado = []

    for transaccion in lista_transacciones:
        if transaccion.tipo == tipo_a_filtrar:
            resultado.append(transaccion)

    return resultado


def ejecutar_sistema():

    datos_cargados = leer_y_almacenar_datos()

    print("\n===== INICIO DEL PROCESO =====\n")

    print(f"Total de registros cargados: {len(datos_cargados)}")

    total = calcular_monto_total(datos_cargados)

    print(f"\nMonto Total de todas las transacciones: ${total:,.2f}")

    creditos = filtrar_por_tipo(datos_cargados, "CREDITO")

    print("\n===== TRANSACCIONES DE CREDITO =====\n")

    for transaccion in creditos:
        print(transaccion.obtener_informacion())

    print("\n===== VALIDACION DE TIPOS =====\n")

    for transaccion in datos_cargados:
        estado = "VALIDO" if transaccion.validar_tipo() else "NO VALIDO"

        print(
            f"{transaccion.cliente_id} - "
            f"{transaccion.tipo} - "
            f"{estado}"
        )

    print("\n===== FIN DEL PROCESO =====\n")


ejecutar_sistema()