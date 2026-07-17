# Sistema de Transacciones (POO)

Proyecto de la asignatura **Fundamentos de Software** — Sistema de consola en Python para registrar, consultar y modificar transacciones bancarias (crédito y débito), aplicando los tres pilares de la Programación Orientada a Objetos y el principio SOLID de Abierto/Cerrado (OCP).

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

## Uso

```bash
python transaccion_poo_v2.py
```

Menú disponible:

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

- Nueva subclase `TransaccionTransferencia` con su propia lógica de `calcular_impacto()`.
- Persistencia en una base de datos en lugar de archivo de texto.
- Reportes exportables (PDF/Excel) del impacto total por tipo de transacción.