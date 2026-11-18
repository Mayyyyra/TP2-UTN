from Consola.Menu import Menu
from Consola.lector import leer_entero, leer_sn
from Entidades.Usuario import Usuario
from Servicios.CategoriaServicio import CategoriaServicio
from Servicios.ProductoServicio import ProductoServicio
from Servicios.PedidoServicio import PedidoServicio
from Exepciones.FoodStoreError import FoodStoreError

class MenuCliente(Menu):
    def __init__(self, usuario: Usuario, cat_servicio: CategoriaServicio, 
                 prod_servicio: ProductoServicio, ped_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self.cat_servicio = cat_servicio
        self.prod_servicio = prod_servicio
        self.ped_servicio = ped_servicio

    def mostrar(self) -> bool:
        while True:
            self.limpiar_pantalla()
            print("="*40)
            print(f" FOOD STORE - CLIENTE ({self.usuario.nombre}) ")
            print("="*40)
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            
            opcion = leer_entero("Seleccione una opción: ")

            try:
                if opcion == 1:
                    cats = self.cat_servicio.listar()
                    if not cats:
                        print("\nNo hay categorías cargadas.")
                    else:
                        print("\n--- CATEGORÍAS ---")
                        for c in cats:
                            print(c)
                
                elif opcion == 2:
                    prods = self.prod_servicio.listar_disponibles()
                    if not prods:
                        print("\nNo hay productos disponibles.")
                    else:
                        print("\n--- PRODUCTOS DISPONIBLES ---")
                        for p in prods:
                            print(p)
                
                elif opcion == 3:
                    peds = self.ped_servicio.listar_por_usuario(self.usuario.id)
                    if not peds:
                        print("\nNo tenés pedidos realizados.")
                    else:
                        print("\n--- MIS PEDIDOS ---")
                        for p in peds:
                            print(p)
                        
                        if leer_sn("\n¿Querés ver los detalles de algún pedido?"):
                            id_ped = leer_entero("Ingresá el ID del pedido: ")
                            try:
                                pedido = self.ped_servicio.buscar_por_id(id_ped)
                                if pedido.usuario.id != self.usuario.id:
                                    print("\nPedido no encontrado.")
                                else:
                                    print(f"\n--- Detalles del Pedido {pedido.id} ---")
                                    for detalle in pedido.detalles:
                                        print(detalle)
                                    print(f"TOTAL: ${pedido.total:.2f}")
                            except FoodStoreError as e:
                                print(f"\nError: {e}")
                
                elif opcion == 4:
                    print("\n--- MIS DATOS ---")
                    print(self.usuario)
                    
                elif opcion == 9:
                    print("\nCerrando sesión...")
                    return True
                    
                elif opcion == 0:
                    print("\nSaliendo del sistema")
                    return False
                    
                else:
                    print("\nOpción inválida.")
                    
            except FoodStoreError as e:
                print(f"\nError: {e}")
            except ValueError:
                print("\nError: Ingresaste un dato inválido.")
            
            input("\nPresione Enter para continuar")