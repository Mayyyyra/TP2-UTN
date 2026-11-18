from Consola.Menu import Menu
from Consola.lector import leer_entero, leer_texto, leer_sn, leer_flotante
from Entidades.Usuario import Usuario
from Entidades.Rol import Rol
from Entidades.EnumsPedido import FormaPago, Estado
from Servicios.CategoriaServicio import CategoriaServicio
from Servicios.ProductoServicio import ProductoServicio
from Servicios.UsuarioServicio import UsuarioServicio
from Servicios.PedidoServicio import PedidoServicio
from Exepciones.FoodStoreError import FoodStoreError, DatoInvalidoError

class MenuAdministrador(Menu):
    def __init__(self, usuario: Usuario, cat_servicio: CategoriaServicio, 
                 prod_servicio: ProductoServicio, user_servicio: UsuarioServicio, 
                 ped_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self.cat_servicio = cat_servicio
        self.prod_servicio = prod_servicio
        self.user_servicio = user_servicio
        self.ped_servicio = ped_servicio

    def mostrar(self) -> bool:
        while True:
            self.limpiar_pantalla()
            print("="*40)
            print(f" FOOD STORE - ADMIN ({self.usuario.nombre}) ")
            print("="*40)
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            
            opcion = leer_entero("Seleccione una opción: ")

            if opcion == 1:
                self.submenu_categorias()
            elif opcion == 2:
                self.submenu_productos()
            elif opcion == 3:
                self.submenu_usuarios()
            elif opcion == 4:
                self.submenu_pedidos()
            elif opcion == 9:
                print("\nCerrando sesión")
                return True
            elif opcion == 0:
                print("\nSaliendo del sistema")
                return False
            else:
                print("\nOpción inválida. Intente de nuevo.")

    def submenu_categorias(self) -> None:
        while True:
            self.limpiar_pantalla()
            print("-"*30)
            print(" GESTIÓN DE CATEGORÍAS ")
            print("-"*30)
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver al menú principal")
            
            opcion = leer_entero("Seleccione una operación: ")

            if opcion == 0:
                break

            try:
                if opcion == 1:
                    categorias = self.cat_servicio.listar()
                    if not categorias:
                        print("No hay categorías cargadas.")
                    else:
                        for c in categorias:
                            print(c)
                
                elif opcion == 2:
                    nombre = leer_texto("Nombre de la categoría: ")
                    desc = leer_texto("Descripción: ")
                    cat = self.cat_servicio.crear(nombre, desc)
                    print(f"Categoría creada con ID {cat.id}.")
                
                elif opcion == 3:
                    id_cat = leer_entero("ID de la categoría a editar: ")
                    nuevo_nombre = leer_texto("Nuevo nombre (Enter para conservar): ", permitir_vacio=True)
                    nueva_desc = leer_texto("Nueva descripción (Enter para conservar): ", permitir_vacio=True)
                    
                    nombre_final = nuevo_nombre if nuevo_nombre != "" else None
                    desc_final = nueva_desc if nueva_desc != "" else None
                    
                    self.cat_servicio.editar(id_cat, nombre_final, desc_final)
                    print("Categoría actualizada.")
                
                elif opcion == 4:
                    id_cat = leer_entero("ID de la categoría a eliminar: ")
                    if leer_sn("¿Estás seguro de eliminarla?"):
                        self.cat_servicio.eliminar(id_cat, list(self.prod_servicio.productos))
                        print("Categoría eliminada.")
                    else:
                        print("Operación cancelada.")
                else:
                    print("Opción inválida.")
                        
            except FoodStoreError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            
            input("\nPresione Enter para continuar...")

    def submenu_productos(self) -> None:
        while True:
            self.limpiar_pantalla()
            print("-"*30)
            print(" GESTIÓN DE PRODUCTOS ")
            print("-"*30)
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            
            opcion = leer_entero("Seleccione: ")

            if opcion == 0:
                break

            try:
                if opcion == 1:
                    prods = self.prod_servicio.listar()
                    if not prods:
                        print("No hay productos.")
                    else:
                        for p in prods:
                            print(p)
                
                elif opcion == 2:
                    nom = leer_texto("Nombre: ")
                    precio = leer_flotante("Precio: ")
                    desc = leer_texto("Descripción: ")
                    stock = leer_entero("Stock: ")
                    img = leer_texto("Imagen: ")
                    disp = leer_sn("Está disponible?")
                    id_cat = leer_entero("ID de la categoría (0 para ninguna): ")
                    
                    prod = self.prod_servicio.crear(nom, precio, desc, stock, img, disp, id_cat, self.cat_servicio)
                    print(f"Producto creado con ID {prod.id}.")
                
                elif opcion == 3:
                    id_prod = leer_entero("ID del producto: ")
                    print("Deja vacío para conservar el valor actual.")
                    
                    nom = leer_texto("Nuevo nombre: ", permitir_vacio=True)
                    precio_str = leer_texto("Nuevo precio: ", permitir_vacio=True)
                    
                    precio_float = None
                    if precio_str:
                        try:
                            precio_float = float(precio_str.replace(",", "."))
                        except ValueError:
                            raise DatoInvalidoError("El precio debe ser un número válido")
                    
                    print("\nEditar categoría:")
                    print("Ingresa el ID de la nueva categoría.")
                    print("(Ingresa 0 para dejarlo SIN categoría, o presiona Enter para no cambiar nada)")
                    
                    cat_str = leer_texto("ID de categoría: ", permitir_vacio=True)
                    
                    id_cat_final = None
                    if cat_str:
                        try:
                            id_cat_final = int(cat_str)
                        except ValueError:
                            raise DatoInvalidoError("El ID de categoría debe ser un número entero")

                    self.prod_servicio.editar(
                        id_prod, 
                        nombre=nom if nom else None, 
                        precio=precio_float,
                        id_categoria=id_cat_final,
                        cat_servicio=self.cat_servicio
                    )
                    print("Producto actualizado.")
                
                elif opcion == 4:
                    id_prod = leer_entero("ID del producto: ")
                    if leer_sn("¿Seguro de eliminarlo?"):
                        self.prod_servicio.eliminar(id_prod)
                        print("Producto eliminado.")
                else:
                    print("Opción inválida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")
            
            input("\nPresione Enter para continuar...")

    def submenu_usuarios(self) -> None:
        while True:
            self.limpiar_pantalla()
            print("-"*30)
            print(" GESTIÓN DE USUARIOS ")
            print("-"*30)
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            
            opcion = leer_entero("Seleccione: ")

            if opcion == 0:
                break

            try:
                if opcion == 1:
                    users = self.user_servicio.listar()
                    if not users:
                        print("No hay usuarios.")
                    else:
                        for u in users:
                            print(u)
                
                elif opcion == 2:
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
                    print(f"Usuario creado con ID {user.id}.")
                
                elif opcion == 3:
                    id_prod = leer_entero("ID del producto: ")
                    print("Deja vacío para conservar el valor actual.")
                    
                    nom = leer_texto("Nuevo nombre: ", permitir_vacio=True)
                    precio_str = leer_texto("Nuevo precio: ", permitir_vacio=True)
                    
                    precio_float = None
                    if precio_str:
                        try:
                            precio_float = float(precio_str.replace(",", "."))
                        except ValueError:
                            raise DatoInvalidoError("El precio debe ser un número válido")
                    
                    print("\nEditar categoría:")
                    print("Ingresa el ID de la nueva categoría.")
                    print("(Ingresa 0 para dejarlo SIN categoría, o presiona Enter para no cambiar nada)")
                    
                    cat_str = leer_texto("ID de categoría: ", permitir_vacio=True)
                    
                    id_cat_final = None
                    if cat_str:
                        try:
                            id_cat_final = int(cat_str)
                        except ValueError:
                            raise DatoInvalidoError("El ID de categoría debe ser un número entero")

                    self.prod_servicio.editar(
                        id_prod, 
                        nombre=nom if nom else None, 
                        precio=precio_float,
                        id_categoria=id_cat_final,
                        cat_servicio=self.cat_servicio
                    )
                    print("Producto actualizado.")
                
                elif opcion == 4:
                    id_user = leer_entero("ID del usuario: ")
                    if leer_sn("¿Seguro de eliminarlo?"):
                        self.user_servicio.eliminar(id_user, self.usuario.id)
                        print("Usuario eliminado.")
                else:
                    print("Opción inválida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")
            
            input("\nPresione Enter para continuar...")

    def submenu_pedidos(self) -> None:
        while True:
            self.limpiar_pantalla()
            print("-"*30)
            print(" GESTIÓN DE PEDIDOS ")
            print("-"*30)
            print("1. Listar")
            print("2. Crear")
            print("3. Actualizar Estado")
            print("4. Eliminar")
            print("0. Volver")
            
            opcion = leer_entero("Seleccione: ")

            if opcion == 0:
                break

            try:
                if opcion == 1:
                    peds = self.ped_servicio.listar()
                    if not peds:
                        print("No hay pedidos.")
                    else:
                        for p in peds:
                            print(p)
                
                elif opcion == 2:
                    users = self.user_servicio.listar()
                    if users:
                        for u in users:
                            print(u)
                    id_user = leer_entero("ID del usuario que hace el pedido: ")
                    user = self.user_servicio.buscar_por_id(id_user)
                    
                    print("Formas de pago: 1=Tarjeta, 2=Transferencia, 3=Efectivo")
                    fp_num = leer_entero("Opción: ")
                    try:
                        fp = FormaPago.desde_numero(fp_num)
                    except ValueError:
                        raise DatoInvalidoError("Forma de pago incorrecta.")
                    
                    prod_list = []
                    while True:
                        prods = self.prod_servicio.listar()
                        if prods:
                            for p in prods:
                                print(p)
                        else:
                            print("No hay productos cargados")
                            break
                        id_prod = leer_entero("ID del producto (0 para terminar): ")
                        if id_prod == 0: break
                        cant = leer_entero("Cantidad: ")
                        prod = self.prod_servicio.buscar_por_id(id_prod)
                        prod_list.append((prod, cant))
                    
                    pedido = self.ped_servicio.crear(user, fp, prod_list, self.prod_servicio)
                    print(f"Pedido creado con ID {pedido.id} y Total: ${pedido.total:.2f}")
                
                elif opcion == 3:
                    id_ped = leer_entero("ID del pedido: ")
                    print("Nuevo Estado: 1=Pendiente, 2=Confirmado, 3=Terminado, 4=Cancelado")
                    est_num = leer_entero("Opción: ")
                    try:
                        est = Estado.desde_numero(est_num)
                    except ValueError:
                        raise DatoInvalidoError("Estado incorrecto.")
                    self.ped_servicio.actualizar_estado(id_ped, est)
                    print("Estado actualizado.")

                elif opcion == 4:
                    id_ped = leer_entero("ID del pedido: ")
                    if leer_sn("¿Seguro de eliminarlo?"):
                        self.ped_servicio.eliminar(id_ped)
                        print("Pedido eliminado.")
                else:
                    print("Opción inválida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")
            
            input("\nPresione Enter para continuar...")