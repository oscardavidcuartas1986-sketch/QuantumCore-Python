# Sistema de Transacciones (POO)

Proyecto de la asignatura **Fundamentos de Software** — Sistema de consola en Python para registrar, consultar y modificar transacciones bancarias (crédito y débito), aplicando los tres pilares de la Programación Orientada a Objetos, el principio SOLID de Abierto/Cerrado (OCP) y, en su última etapa, manejo robusto de errores con try-except.

INTEGRANTES:
Damian Taborda Moncada
Karen Durango
gordo valencia
braian loaiza
Oscar Cuartas

## Descripción general

El programa permite:

- Ver el listado completo de transacciones.
- Filtrar y ver solo las transacciones de crédito.
- Calcular el monto total de todas las transacciones.
- Modificar una transacción existente (tipo y monto).
- Agregar una nueva transacción, validando que el ID del cliente no se repita.
- Ver el **impacto** de cada transacción (interés o comisión), calculado de forma distinta según el tipo.
- Cargar los datos de forma **robusta**, detectando y aislando registros corruptos sin detener la ejecución.

Los datos se persisten en un archivo de texto plano `transacciones.txt`, con formato `cliente_id,tipo,monto` por línea.

## Estructura de clases

```
TransaccionBase
├── TransaccionCredito
└── TransaccionDebito
```

### `TransaccionBase`
Clase padre. Contiene:
- Atributos encapsulados (`_cliente_id`, `_tipo`, `_monto`) accedidos mediante `@property` y sus respectivos setters.
- Validación en el setter de `monto`: no permite valores negativos.
- Métodos comunes: `obtener_informacion()`, `validar_tipo()`, `modificar_tipo()`, `modificar_monto()`.
- `calcular_impacto()` como *placeholder*: lanza `NotImplementedError` para forzar a que cada subclase lo implemente.

Esta clase está **cerrada a modificación**: no se toca para agregar nuevos comportamientos, solo para corregir errores de la lógica común.

> Nota: en el constructor (`__init__`), el atributo `monto` se asigna directamente a `self._monto`, sin pasar por el setter. Esto significa que la validación de "no negativos" solo se aplica cuando una transacción ya creada se modifica (`modificar_monto()`), no en el momento de la creación. Es un comportamiento heredado del diseño original del proyecto.

### `TransaccionCredito` (hereda de `TransaccionBase`)
- Fija automáticamente el tipo como `"CREDITO"`.
- Define `TASA_INTERES = 0.02` (2%).
- Sobrescribe `calcular_impacto()`: retorna el interés generado (`monto * tasa_interes`).

### `TransaccionDebito` (hereda de `TransaccionBase`)
- Fija automáticamente el tipo como `"DEBITO"`.
- Define `COMISION_FIJA = 1000.0`.
- Sobrescribe `calcular_impacto()`: retorna una comisión fija, sin importar el monto.

## Pilares de POO aplicados

| Pilar | Dónde se ve en el código |
|---|---|
| **Encapsulamiento** | Atributos privados (`_cliente_id`, `_tipo`, `_monto`) expuestos solo mediante `@property`/setters, con validación de negocio en `monto`. |
| **Herencia** | `TransaccionCredito` y `TransaccionDebito` heredan toda la lógica común de `TransaccionBase` en vez de duplicar código. |
| **Polimorfismo** | `calcular_impacto()` se invoca igual desde cualquier parte del programa (`transaccion.calcular_impacto()`), pero el resultado depende de la clase real del objeto. |
| **OCP (Abierto/Cerrado)** | Para agregar un nuevo tipo de transacción (ej. `TransaccionTransferencia`) basta con crear otra clase hija; no se modifica `TransaccionBase` ni las clases existentes. |

## Función fábrica: `crear_transaccion()`

Para que el resto del programa (lectura de archivo, alta de nuevas transacciones) no necesite saber que existen subclases, toda creación de objetos pasa por esta función:

```python
def crear_transaccion(cliente_id, tipo, monto):
    tipo = tipo.upper()
    if tipo == "CREDITO":
        return TransaccionCredito(cliente_id, monto)
    elif tipo == "DEBITO":
        return TransaccionDebito(cliente_id, monto)
    else:
        raise ValueError(f"Tipo de transacción inválido: {tipo}")
```

Esto centraliza la decisión de qué clase instanciar y mantiene el resto del código desacoplado de los detalles de la jerarquía.

## Robustez del sistema: manejo de errores con try-except

En la versión inicial, la lectura del archivo de transacciones (`leer_y_almacenar_datos()`) asumía que todas las líneas venían bien formadas. Si un registro tenía datos corruptos (por ejemplo, un monto que no es un número, o menos columnas de las esperadas), la creación del objeto fallaba y el programa se detenía por completo, sin poder cargar el resto de los registros válidos.

Para resolver esto se agregó la función `leer_y_almacenar_datos_robusto()`, que lee el archivo `transacciones_corruptas.txt` línea por línea y envuelve la creación de cada transacción en un bloque `try-except`. Si una línea falla, el error se registra en consola (log) y el programa continúa con la siguiente línea, en vez de detener la ejecución.

```python
try:
    transaccion = crear_transaccion(*partes)
    lista_transacciones.append(transaccion)

except ValueError as error:
    # Conversión inválida (ej. "texto_invalido" a float)
    # o validación de negocio (ej. monto negativo).
    print(f"[ERROR - ValueError] Línea {numero_linea} ('{linea}'): {error}.")
    continue

except TypeError as error:
    # Datos insuficientes: faltan columnas en la línea.
    print(f"[ERROR - TypeError] Línea {numero_linea} ('{linea}'): {error}.")
    continue
```

### Detalles de la implementación

- **Un único punto de try-except**: toda la lógica de conversión/instanciación se concentra dentro de `leer_y_almacenar_datos_robusto()`, que es el único lugar del programa donde se transforman datos externos (texto plano) en objetos.
- **`except ValueError`**: atrapa dos escenarios distintos que producen el mismo tipo de excepción: (1) que `float(monto)` no pueda convertir el texto a número, y (2) que el setter de `monto` rechace un valor negativo cuando sí se llega a validar.
- **`except TypeError`**: se logra pasando los datos de la línea a la fábrica con desempaquetado (`crear_transaccion(*partes)`). Si a una línea le falta una columna, Python lanza automáticamente un `TypeError` por falta de un argumento posicional requerido, sin necesidad de validar manualmente `len(partes)`.
- **Estrategia de recuperación pasiva**: en cada bloque `except` se imprime un mensaje indicando el tipo de error, el número de línea y su contenido, y luego se usa `continue` para que el bucle `for` siga con el siguiente registro. Los registros fallidos simplemente no se agregan a la lista final; el resto del archivo sí se procesa.
- **Resumen final**: al terminar la lectura se imprime cuántas líneas se procesaron, cuántas transacciones se cargaron con éxito y cuántos errores se detectaron.

### Archivo de prueba: `transacciones_corruptas.txt`

```
C001,DEBITO,150000
C002,CREDITO,500000
C003,DEBITO,texto_invalido
C004,CREDITO,-200000
C005,DEBITO,45000
C006,DEBITO
C007,CREDITO,10000
```

Errores intencionales incluidos:

| Línea | Registro | Error esperado | Motivo |
|---|---|---|---|
| 3 | `C003,DEBITO,texto_invalido` | `ValueError` | `float("texto_invalido")` no se puede convertir a número. |
| 4 | `C004,CREDITO,-200000` | (según la versión del `__init__`) | Un monto negativo debería rechazarse por el setter de `monto`; en la versión actual del constructor esta validación no se dispara al crear el objeto, solo al modificarlo con `modificar_monto()`. |
| 6 | `C006,DEBITO` | `TypeError` | Faltan datos: la línea solo trae 2 columnas (falta el monto). |

## Uso

```bash
python robustez_try_except.py
```

Al ejecutarse, primero se muestra el resultado de la carga robusta del archivo `transacciones_corruptas.txt` (errores detectados y transacciones cargadas), y luego se despliega el menú principal del sistema original:

```
1. Ver transacciones
2. Ver créditos
3. Calcular monto total
4. Modificar transacción
5. Agregar cliente
6. Ver impacto por transacción
7. Salir
```

## Formato del archivo de datos

`transacciones.txt` (mismo directorio que el script):

```
CLI001,CREDITO,150000
CLI002,DEBITO,80000
```

## Posibles extensiones futuras

- Ajustar el `__init__` de `TransaccionBase` para que asigne `monto` a través de la propiedad (`self.monto = ...` en vez de `self._monto = ...`), de modo que la validación de negativos también aplique al crear el objeto y no solo al modificarlo.
- Nueva subclase `TransaccionTransferencia` con su propia lógica de `calcular_impacto()`.
- Persistencia en una base de datos en lugar de archivo de texto.
- Reportes exportables (PDF/Excel) del impacto total por tipo de transacción.
