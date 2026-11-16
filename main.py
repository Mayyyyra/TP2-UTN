from getpass import getpass
from Servicios.UsuarioServicio import UsuarioServicio
from Servicios.CategoriaServicio import CategoriaServicio
from Servicios.ProductoServicio import ProductoServicio
from Servicios.PedidoServicio import PedidoServicio
from Consola.MenuAdministrador import MenuAdministrador
from Consola.MenuCliente import MenuCliente
from Entidades.Rol import Rol
from Exepciones.FoodStoreError import CredencialesInvalidasError

def main():
    user_servicio = UsuarioServicio()
    cat_servicio = CategoriaServicio()
    prod_servicio = ProductoServicio()
    ped_servicio = PedidoServicio()

    try:
        user_servicio.crear(
            nombre="Admin", apellido="FoodStore", 
            mail="admin@foodstore.com", celular="123456789", 
            contrasenia="admin123", rol=Rol.ADMIN
        )
    except Exception:
        pass

    print("      BIENVENIDO A FOOD STORE           ")
    while True:
        print("INICIO DE SESIÓN")
        mail = input("Mail: ").strip()
        contrasenia = getpass("Contraseña: ") 

        try:
            usuario_actual = user_servicio.autenticar(mail, contrasenia)
            print(f"Bienvenido, {usuario_actual.nombre} {usuario_actual.apellido} [{usuario_actual.rol.name}]!")
            break
        except CredencialesInvalidasError as e:
            print(f"{e}")

    salir_del_programa = False
    while not salir_del_programa:

        if usuario_actual.rol == Rol.ADMIN:
            menu = MenuAdministrador(usuario_actual, cat_servicio, prod_servicio, user_servicio, ped_servicio)
        else:
            menu = MenuCliente(usuario_actual, cat_servicio, prod_servicio, ped_servicio)

        cerrar_sesion = menu.mostrar()

        if not cerrar_sesion:
            salir_del_programa = True
        else:
            print("\nINICIO DE SESIÓN")
            sesion_iniciada = False
            intentos = 0
            
            while not sesion_iniciada and intentos < 3:
                mail = input("Mail: ").strip()
                contrasenia = getpass("Contraseña: ")
                
                try:
                    usuario_actual = user_servicio.autenticar(mail, contrasenia)
                    print(f"\n¡Bienvenido, {usuario_actual.nombre} {usuario_actual.apellido} [{usuario_actual.rol.name}]!")
                    sesion_iniciada = True
                except CredencialesInvalidasError as e:
                    print(f"{e}")
                    intentos += 1
            
            if not sesion_iniciada:
                print("Demasiados intentos fallidos. El programa se cerrará.")
                salir_del_programa = True

if __name__ == "__main__":
    main()