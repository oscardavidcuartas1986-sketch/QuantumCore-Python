# Correcciones — Sistema de Gestión Agrícola CEIPA

Este documento explica qué errores tenía el proyecto original y qué se cambió en cada archivo para corregirlos. Todo se validó ejecutando el programa con casos que antes lo hacían fallar.

## Archivos modificados
- `main.py`
- `repuesto.py`
- `sistema_de_riego.py`
- `operador.py`

## Archivos sin cambios
- `tractor.py`
- `mantenimiento.py`
- `maquinaria.py`

---

## 1. `repuesto.py` — código de prueba se ejecutaba solo

**Problema:** las líneas de prueba al final del archivo no estaban comentadas (a diferencia de `tractor.py` y `sistema_de_riego.py`), así que cada vez que `main.py` importaba el módulo, se creaba un `Repuesto` de prueba y se imprimía en pantalla antes de mostrar el menú.

**Corrección:** se comentaron esas líneas, igual que en los demás archivos.

```python
# --- PRUEBAS DE SOFTWARE ---
# filtro = Repuesto("Filtro de Aceite", "P-101", 10)
# filtro.set_stock(15)
# print(f"Repuesto: {filtro.nombre} | Stock actual: {filtro.get_stock()}")
```

---

## 2. `main.py` — el índice de la máquina no se validaba (opción 4)

**Problema:** en "Registrar Mantenimiento", el programa pedía la posición del equipo pero nunca revisaba si ese número existía en la lista. Si el usuario ingresaba un número fuera de rango, el programa se cerraba con `IndexError: list index out of range`.

**Corrección:** se agregó un bucle que vuelve a pedir el número hasta que corresponda a una máquina que sí existe en el inventario, igual de estricto que la validación que ya tenía el índice de repuestos.

```python
while True:
    idx = pedir_entero("Ingrese numero de posicion del equipo: ")
    if 0 <= idx < len(inventario_maquinas):
        break
    print("Error: Ese número de posición no existe en el inventario.")
```

---

## 3. `main.py` — no había manejo de errores en los datos numéricos

**Problema:** todas las conversiones `int(input(...))` y `float(input(...))` (potencia, horas, caudal, presión, costo, cantidad de repuestos, índice de máquina) no tenían `try/except`. Si el usuario escribía una letra o dejaba el campo vacío, el programa se caía con `ValueError`.

**Corrección:** se crearon dos funciones auxiliares al inicio del archivo que piden el dato en un bucle y no dejan avanzar hasta que sea válido:

```python
def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        try:
            return int(valor)
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def pedir_decimal(mensaje):
    while True:
        valor = input(mensaje)
        try:
            return float(valor)
        except ValueError:
            print("Error: Debe ingresar un número válido (puede tener decimales).")
```

Y se reemplazaron todas las conversiones directas por estas funciones (potencia, horas, caudal, presión, cantidad inicial de repuesto, costo del mantenimiento, cantidad usada, e índice de la máquina).

---

## 4. `main.py` — el menú principal no avisaba si la opción no existía

**Problema:** si el usuario escribía algo distinto a 1, 2, 3, 4 o 5, el programa simplemente volvía a mostrar el menú sin ningún mensaje. El submenú de almacén (opción 3) sí tenía este aviso, pero el menú principal no.

**Corrección:** se agregó un `else` final con el mensaje de error correspondiente.

```python
else:
    print("Error: Opción no válida. Seleccione un número del 1 al 5.")
```

---

## 5. `sistema_de_riego.py` — la presión inicial se saltaba la validación de seguridad

**Problema:** `set_presion()` valida que la presión esté entre 0 y 12 bar, pero el constructor asignaba `self.presion = presion` directamente, sin pasar por esa validación. Esto significa que al **registrar** un sistema de riego (opción 1 del menú) se podía guardar una presión fuera de rango de seguridad sin ningún aviso.

**Corrección:** el constructor ahora llama a `set_presion()` en vez de asignar el valor directo, así la validación aplica también al crear el objeto.

```python
self.presion = None
self.set_presion(presion)
```

---

## 6. `operador.py` — comentarios de prueba con nombres de método incorrectos

**Problema:** el código de prueba comentado al final del archivo llamaba a `op.asignar_maquina(...)` y `op.realizar_labor()`, pero los métodos reales de la clase se llaman `asignar_equipo()` y `realizar_trabajo()`. Si alguien descomentaba ese bloque tal cual, obtenía un `AttributeError`.

**Corrección:** se actualizaron los nombres en los comentarios para que coincidan con los métodos reales.

> **Nota aparte (no corregida):** la clase `Operador` sigue sin usarse en `main.py` — no existe ninguna opción de menú para registrar operadores o asignarles maquinaria. Es una funcionalidad incompleta, no un error de código. Si quieres, puedo agregar una opción de menú para integrarla.

---

## Pruebas realizadas

Se corrió el programa simulando entradas de consola para confirmar que cada corrección funciona:

| Caso probado | Antes | Después |
|---|---|---|
| Índice de máquina fuera de rango en opción 4 | `IndexError`, se cierra el programa | Pide el número de nuevo hasta que sea válido |
| Letra en un campo numérico (ej. potencia) | `ValueError`, se cierra el programa | Pide el dato de nuevo hasta que sea válido |
| Opción de menú inválida (ej. "9") | No decía nada | Muestra "Error: Opción no válida..." |
| Importar `repuesto.py` | Imprimía datos de prueba en pantalla | Import limpio, sin salida extra |
| Presión fuera de rango al registrar sistema de riego | Se guardaba sin aviso | Pasa por la validación de seguridad |

Todos los casos se probaron y ya no rompen el programa.
