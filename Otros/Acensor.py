import time
import os
import threading

# ── Colores ANSI ───────
RESET   = "\033[0m"
BOLD    = "\033[1m"
CYAN    = "\033[96m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
RED     = "\033[91m"
GRAY    = "\033[90m"
WHITE   = "\033[97m"
BG_BLUE = "\033[44m"
BG_RED  = "\033[41m"

TIEMPO_PUERTAS = 2
PISOS          = 4

# ── Estado global ─────
piso_actual = 1
solicitudes = [0, 0, 0, 0]
estado      = "q0"
emergencia  = False
log_msgs    = [ ]

# ── Helpers ───────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def agregar_log(msg):
    log_msgs.append(msg)
    if len(log_msgs) > 8:
        log_msgs.pop(0)

def SA():
    return any(solicitudes[k] for k in range(piso_actual, PISOS))

def SB():
    return any(solicitudes[k] for k in range(0, piso_actual - 1))

# ── Dibujo en consola ──────────
def dibujar():
    limpiar()

    print(f"\n  {BG_BLUE}{BOLD}{'  SIMULADOR DE ASCENSOR  ':^30}{RESET}\n")

    # Techo del shaft
    print(f"        ╔══════╗")

    for f in range(PISOS, 0, -1):
        tiene_req = solicitudes[f - 1] == 1
        es_actual = f == piso_actual

        dot = f"{YELLOW}●{RESET}" if tiene_req else f"{GRAY}○{RESET}"

        if es_actual:
            if estado == "q3":
                cabina = f"{GREEN}[≡≡]{RESET}"
            elif emergencia:
                cabina = f"{RED}[!!]{RESET}"
            else:
                cabina = f"{CYAN}[  ]{RESET}"
        else:
            cabina = "      "

        print(f"  {BOLD}{WHITE}Piso {f}{RESET}  ║ {cabina} ║  {dot}")

        # Línea separadora entre pisos (excepto después del último)
        if f > 1:
            print(f"        ╠══════╣")

    # Suelo del shaft
    print(f"        ╚══════╝")

    estado_color = {
        "q0": GRAY, "q1": CYAN, "q2": YELLOW, "q3": GREEN, "q4": RED,
    }.get(estado, WHITE)

    estado_nombre = {
        "q0": "Reposo",
        "q1": "Subiendo ⬆",
        "q2": "Bajando ⬇",
        "q3": "Puertas abiertas",
        "q4": "EMERGENCIA",
    }.get(estado, estado)

    print(f"\n  Estado : {estado_color}{BOLD}{estado_nombre}{RESET}")
    print(f"  Piso   : {BOLD}{piso_actual}{RESET}")
    req_str = " ".join(
        f"{YELLOW}{v}{RESET}" if v else f"{GRAY}{v}{RESET}"
        for v in solicitudes
    )
    print(f"  Filas  : [ {req_str} ]")

    print(f"\n  {GRAY}{'─' * 34}{RESET}")
    for m in log_msgs[-5:]:
        print(f"  {GRAY}{m}{RESET}")
    print(f"  {GRAY}{'─' * 34}{RESET}")

    if emergencia:
        print(f"\n  {BG_RED}{BOLD}  ASCENSOR DETENIDO — presiona 'r' para reiniciar  {RESET}\n")
    else:
        print(f"\n  Pisos {BOLD}[1-4]{RESET} separados por espacios (ej: {BOLD}1 3 4{RESET}), {BOLD}'e'{RESET} emergencia: ", end="", flush=True)

# ── Máquina de estados ────────────────────────────────────────────────────────
def mover_cabina(direccion):
    global piso_actual
    piso_actual = max(1, min(PISOS, piso_actual + direccion))

def piso_alcanzado():
    return solicitudes[piso_actual - 1] == 1

def ciclo_ascensor():
    global estado, emergencia

    while True:
        if emergencia:
            time.sleep(0.5)
            continue

        if estado == "q0":
            time.sleep(0.5)
            continue

        elif estado == "q1":
            time.sleep(1)
            if emergencia:
                continue
            mover_cabina(+1)
            agregar_log(f"Subiendo → piso {piso_actual}")
            dibujar()
            if piso_alcanzado():
                agregar_log(f"✔ Atendiendo piso {piso_actual}")
                solicitudes[piso_actual - 1] = 0
                estado = "q3"
                dibujar()
                time.sleep(TIEMPO_PUERTAS)
                agregar_log("Puertas cerradas")
                estado = "q1" if SA() else ("q2" if SB() else "q0")
                if estado == "q0":
                    agregar_log("Sin más solicitudes — en reposo")
                dibujar()

        elif estado == "q2":
            time.sleep(1)
            if emergencia:
                continue
            mover_cabina(-1)
            agregar_log(f"Bajando → piso {piso_actual}")
            dibujar()
            if piso_alcanzado():
                agregar_log(f"✔ Atendiendo piso {piso_actual}")
                solicitudes[piso_actual - 1] = 0
                estado = "q3"
                dibujar()
                time.sleep(TIEMPO_PUERTAS)
                agregar_log("Puertas cerradas")
                estado = "q1" if SA() else ("q2" if SB() else "q0")
                if estado == "q0":
                    agregar_log("Sin más solicitudes — en reposo")
                dibujar()

# ── Entrada del usuario ───────────────────────────────────────────────────────
def control_usuario():
    global estado, emergencia, piso_actual, solicitudes, log_msgs

    dibujar()

    while True:
        try:
            entrada = input()
        except EOFError:
            break

        if emergencia:
            if entrada.strip().lower() == "r":
                emergencia  = False
                estado      = "q0"
                piso_actual = 1
                solicitudes = [0, 0, 0, 0]
                log_msgs    = []
                agregar_log("Sistema reiniciado")
            dibujar()
            continue

        if entrada.strip() == "":
            dibujar()
            continue

        if entrada.strip().lower() == "e":
            emergencia = True
            estado     = "q4"
            agregar_log("⚠ EMERGENCIA ACTIVADA")
            dibujar()
            continue

        tokens = entrada.replace(",", " ").split()
        registrados = []

        for token in tokens:
            try:
                piso = int(token.strip())
                if 1 <= piso <= PISOS:
                    if piso == piso_actual and estado == "q0" and not solicitudes[piso - 1]:
                        agregar_log(f"Ya estás en el piso {piso}")
                    elif solicitudes[piso - 1]:
                        agregar_log(f"Piso {piso} ya está en cola")
                    else:
                        solicitudes[piso - 1] = 1
                        registrados.append(str(piso))
                else:
                    agregar_log(f"⚠ Piso inválido: {piso} (usa 1-{PISOS})")
            except ValueError:
                agregar_log(f"⚠ '{token}' no es válido")

        if registrados:
            agregar_log(f"Solicitudes registradas: piso(s) {', '.join(registrados)}")
            if estado == "q0":
                estado = "q1" if SA() else "q2"

        dibujar()

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    hilo = threading.Thread(target=ciclo_ascensor, daemon=True)
    hilo.start()
    control_usuario()
    