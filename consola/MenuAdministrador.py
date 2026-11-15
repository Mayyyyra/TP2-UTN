import questionary
from termcolor import colored
from .Menu import Menu
from .lector import leer_entero, leer_texto, leer_sn,leer_flotante
from ..Entidades.Usuario import Usuario
from ..Entidades.Rol import Rol
from ..Entidades.EnumsPedido import FormaPago,Estado
from ..Servicios.CategoriaServicio import CategoriaServicio
from ..Servicios.ProductoServicio import ProductoServicio
from ..Servicios.UsuarioServicio import UsuarioServicio
from ..Servicios.PedidoServicio import PedidoServicio
from ..Exepciones.FoodStoreError import FoodStoreError,DatoInvalidoError

class MenuAdministrador(Menu):
    def __init__(self, usuario: Usuario, cat_servicio: CategoriaServicio, 
                 prod_servicio: ProductoServicio, user_servicio: UsuarioServicio, 
                 ped_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self.cat_servicio = cat_servicio
        self.prod_servicio = prod_servicio
        self.user_servicio = user_servicio
        self.ped_servicio = ped_servicio
    def submenu_categorias(self) -> None:
        while True:
            print("\n" + "-"*30)
            print(colored(" GESTIÓN DE CATEGORÍAS ", "magenta", attrs=["bold"]))
            print("-"*30)
            
            opcion = questionary.select(
                "Seleccione una operación:",
                choices=[
                    "Listar",
                    "Crear",
                    "Editar",
                    "Eliminar",
                    "Volver al menú principal"
                ]
            ).ask()

            if opcion is None or opcion == "Volver al menú principal":
                break

            try:
                match opcion:
                    case "Listar":
                        categorias = self.cat_servicio.listar()
                        if not categorias:
                            print(colored("No hay categorías cargadas.", "yellow"))
                        else:
                            for c in categorias:
                                print(colored(str(c), "green"))
                    
                    case "Crear":
                        nombre = leer_texto("Nombre de la categoría: ")
                        desc = leer_texto("Descripción: ")
                        cat = self.cat_servicio.crear(nombre, desc)
                        print(colored(f"Categoría creada con ID {cat.id}.", "green"))
                    
                    case "Editar":
                        id_cat = leer_entero("ID de la categoría a editar: ")
                        nuevo_nombre = leer_texto("Nuevo nombre (Enter para conservar): ", permitir_vacio=True)
                        nueva_desc = leer_texto("Nueva descripción (Enter para conservar): ", permitir_vacio=True)
                        
                        nombre_final = nuevo_nombre if nuevo_nombre != "" else None
                        desc_final = nueva_desc if nueva_desc != "" else None
                        
                        self.cat_servicio.editar(id_cat, nombre_final, desc_final)
                        print(colored("Categoría actualizada.", "green"))
                    
                    case "Eliminar":
                        id_cat = leer_entero("ID de la categoría a eliminar: ")
                        if leer_sn("¿Estás seguro de eliminarla?"):
                            self.cat_servicio.eliminar(id_cat, list(self.prod_servicio.productos))
                            print(colored("Categoría eliminada.", "green"))
                        else:
                            print(colored("Operación cancelada.", "yellow"))
                            
            except FoodStoreError as e:
                print(colored(f"Error: {e}", "red"))
            except Exception as e:
                print(colored(f"Error inesperado: {e}", "red"))
    def submenu_productos(self) -> None:
        while True:
            print("-"*30)
            print(colored(" GESTIÓN DE PRODUCTOS ", "magenta", attrs=["bold"]))
            print("-"*30)
            
            opcion = questionary.select("Seleccione:", choices=["Listar", "Crear", "Editar", "Eliminar", "Volver"]).ask()
            if opcion is None or opcion == "Volver": break

            try:
                if opcion == "Listar":
                    prods = self.prod_servicio.listar()
                    print("\n".join([colored(str(p), "green") for p in prods]) if prods else colored("No hay productos.", "yellow"))
                
                elif opcion == "Crear":
                    nom = leer_texto("Nombre: ")
                    precio = leer_flotante("Precio: ")
                    desc = leer_texto("Descripción: ")
                    stock = leer_entero("Stock: ")
                    img = leer_texto("Imagen: ")
                    disp = leer_sn("¿Está disponible?")
                    id_cat = leer_entero("ID de la categoría: ")
                    
                    prod = self.prod_servicio.crear(nom, precio, desc, stock, img, disp, id_cat, self.cat_servicio)
                    print(colored(f"Producto creado con ID {prod.id}.", "green"))
                
                elif opcion == "Editar":
                    id_prod = leer_entero("ID del producto: ")
                    print(colored("Deja vacío para conservar el valor actual.", "yellow"))
                    nom = leer_texto("Nuevo nombre: ", permitir_vacio=True)
                    precio_str = leer_texto("Nuevo precio: ", permitir_vacio=True)
                    
                    precio_float = None
                    if precio_str:
                        try:
                            precio_float = float(precio_str.replace(",", "."))
                        except ValueError:
                            raise DatoInvalidoError("El precio debe ser un número válido")
                        
                    self.prod_servicio.editar(id_prod, nombre=nom if nom else None, precio=precio_float)
                    print(colored("Producto actualizado.", "green"))
                
                elif opcion == "Eliminar":
                    id_prod = leer_entero("ID del producto: ")
                    if leer_sn("¿Seguro de eliminarlo?"):
                        self.prod_servicio.eliminar(id_prod)
                        print(colored("Producto eliminado.", "green"))
            except FoodStoreError as e:
                print(colored(f"Error: {e}", "red"))
            except ValueError as e:
                print(colored(f"Error de entrada: {e}", "red"))
    def submenu_usuarios(self) -> None:
        while True:
            print("-"*30)
            print(colored(" GESTIÓN DE USUARIOS ", "magenta", attrs=["bold"]))
            print("-"*30)
            
            opcion = questionary.select("Seleccione:", choices=["Listar", "Crear", "Editar", "Eliminar", "Volver"]).ask()
            if opcion is None or opcion == "Volver": break

            try:
                if opcion == "Listar":
                    users = self.user_servicio.listar()
                    print("".join([colored(str(u), "green") for u in users]) if users else colored("No hay usuarios.", "yellow"))
                
                elif opcion == "Crear":
                    nom = leer_texto("Nombre: ")
                    ape = leer_texto("Apellido: ")
                    mail = leer_texto("Mail: ")
                    cel = leer_texto("Celular: ")
                    passw = leer_texto("Contraseña: ")
                    rol_num = leer_entero("Rol (1=ADMIN, 2=USUARIO): ")
                    
                    try:
                        rol = Rol.desde_numero(rol_num)
                    except ValueError:
                        raise DatoInvalidoError("Rol incorrecto. Debe ser 1 o 2.")
                        
                    user = self.user_servicio.crear(nom, ape, mail, cel, passw, rol)
                    print(colored(f"Usuario creado con ID {user.id}.", "green"))
                
                elif opcion == "Editar":
                    id_user = leer_entero("ID del usuario a editar: ")
                    print(colored("Deja vacío para conservar el valor actual.", "yellow"))
                    
                    nom = leer_texto("Nuevo nombre: ", permitir_vacio=True)
                    ape = leer_texto("Nuevo apellido: ", permitir_vacio=True)
                    mail = leer_texto("Nuevo mail: ", permitir_vacio=True)
                    cel = leer_texto("Nuevo celular: ", permitir_vacio=True)
                    passw = leer_texto("Nueva contraseña: ", permitir_vacio=True)
                    
                    self.user_servicio.editar(
                        id_user, 
                        nombre=nom if nom else None, 
                        apellido=ape if ape else None,
                        mail=mail if mail else None,
                        celular=cel if cel else None,
                        contrasenia=passw if passw else None
                    )
                    print(colored("Usuario actualizado.", "green"))
                
                elif opcion == "Eliminar":
                    id_user = leer_entero("ID del usuario: ")
                    if leer_sn("¿Seguro de eliminarlo?"):
                        self.user_servicio.eliminar(id_user, self.usuario.id)
                        print(colored("Usuario eliminado.", "green"))
            except FoodStoreError as e:
                print(colored(f"Error: {e}", "red"))
            except ValueError as e:
                print(colored(f"Error de entrada: {e}", "red"))
    def submenu_pedidos(self) -> None:
            while True:
                print("-"*30)
                print(colored(" GESTIÓN DE PEDIDOS ", "magenta", attrs=["bold"]))
                print("-"*30)
                opcion = questionary.select("Seleccione:", choices=["Listar", "Crear", "Actualizar Estado", "Eliminar", "Volver"]).ask()
                if opcion is None or opcion == "Volver": break

                try:
                    if opcion == "Listar":
                        peds = self.ped_servicio.listar()
                        print("\n".join([colored(str(p), "green") for p in peds]) if peds else colored("No hay pedidos.", "yellow"))
                    
                    elif opcion == "Crear":
                        id_user = leer_entero("ID del usuario que hace el pedido: ")
                        user = self.user_servicio.buscar_por_id(id_user)
                        
                        print(colored("Formas de pago: 1=Tarjeta, 2=Transferencia, 3=Efectivo", "cyan"))
                        fp_num = leer_entero("Opción: ")
                        try:
                            fp = FormaPago.desde_numero(fp_num)
                        except ValueError:
                            raise DatoInvalidoError("Forma de pago incorrecta.")
                        
                        prod_list = []
                        while True:
                            id_prod = leer_entero("ID del producto (0 para terminar): ")
                            if id_prod == 0: break
                            cant = leer_entero("Cantidad: ")
                            prod = self.prod_servicio.buscar_por_id(id_prod)
                            prod_list.append((prod, cant))
                        
                        # ¡Acá creamos el pedido de verdad!
                        pedido = self.ped_servicio.crear(user, fp, prod_list, self.prod_servicio)
                        print(colored(f"Pedido creado con ID {pedido.id} y Total: ${pedido.total:.2f}", "green"))
                    
                    elif opcion == "Actualizar Estado":
                        id_ped = leer_entero("ID del pedido: ")
                        print(colored("Nuevo Estado: 1=Pendiente, 2=Confirmado, 3=Terminado, 4=Cancelado", "cyan"))
                        est_num = leer_entero("Opción: ")
                        try:
                            est = Estado.desde_numero(est_num)
                        except ValueError:
                            raise DatoInvalidoError("Estado incorrecto.")
                        self.ped_servicio.actualizar_estado(id_ped, est)
                        print(colored("Estado actualizado.", "green"))

                    elif opcion == "Eliminar":
                        id_ped = leer_entero("ID del pedido: ")
                        if leer_sn("¿Seguro de eliminarlo?"):
                            self.ped_servicio.eliminar(id_ped)
                            print(colored("Pedido eliminado.", "green"))
                except FoodStoreError as e:
                    print(colored(f"Error: {e}", "red"))
                except ValueError as e:
                    print(colored(f"Error de entrada: {e}", "red"))

    
    def mostrar(self) -> bool:
        while True:
            print("="*40)
            print(colored(f" FOOD STORE - ADMIN ({self.usuario.nombre}) ", "cyan", attrs=["bold"]))
            print("="*40)
            
            opcion = questionary.select(
                "¿Qué deseas gestionar?",
                choices=[
                    "Categorías",
                    "Productos",
                    "Usuarios",
                    "Pedidos",
                    "Cerrar sesión",
                    "Salir"
                ]
            ).ask()

            if opcion is None:
                return False

            match opcion:
                case "Categorías":
                    self.submenu_categorias()
                case "Productos":
                    print(colored("Menú de productos en construcción", "yellow"))
                    self.submenu_productos()
                case "Usuarios":
                    print(colored("Menú de usuarios en construcción", "yellow"))
                    self.submenu_usuarios()
                case "Pedidos":
                    print(colored("Menú de pedidos en construcción", "yellow"))
                    self.submenu_pedidos()
                case "Cerrar sesión":
                    print(colored("Cerrando sesión", "yellow"))
                    return True
                case "Salir":
                    print(colored("Saliendo del sistema", "red"))
                    return False