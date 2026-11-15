

def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            entrada = input(mensaje).replace(",", ".")
            return float(entrada)
        except ValueError:
            print("se debe ingresar un float")

def leer_entero(mensaje: str) -> int:
    while True:
        try:
            entrada = input(mensaje)
            return int(entrada)
        except ValueError:
            print("Se debe ingresar un numero entero")



def leer_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        entrada = input(mensaje).strip()
        if not entrada and not permitir_vacio:
            print("El dato no puede estar vacio")
        else:
            return entrada

def leer_sn(mensaje: str) -> bool:
    while True:
        entrada = input(mensaje + " (S/N): ").strip().upper()
        if entrada == "S":
            return True
        elif entrada == "N":
            return False
        else:
            print("el campo debe ser 'S' o 'N'")