import questionary
from termcolor import colored

def Menu():
    opciones = ["Categorías","Productos","Usuarios","Pedidos","Cerrar sesión","Salir"]
    Op = questionary.select(
    "Elija una opcion del menu",
    choices=(opciones)).ask()
    while Op != "Salir":
        match Op:
            case "Categorías":
                raise NotImplementedError
            case "Productos":
                raise NotImplementedError
            case "Usuarios":
                raise NotImplementedError
            case "Pedidos":
                raise NotImplementedError
            case "Cerrar sesión":
                raise NotImplementedError
    print(colored("Saliendo del sistema","red"))
Menu()