from ..Entidades.Usuario import Usuario
from ..Entidades.Rol import Rol
from ..Exepciones.FoodStoreError import  DuplicadoError, EntidadNoEncontradaError, CredencialesInvalidasError, OperacionNoPermitidaError

class UsuarioServicio():
    def __init__(self):
        self.__usuarios:list[Usuario] = []
    @property


    def usuarios(self) -> tuple[Usuario, ...]:
        return tuple(self.__usuarios)

    
    def __existe_mail(self, mail: str, id_excluir: int | None = None) -> bool:
        for i in self.__usuarios:
            if not i.eliminado and i.mail.lower() == mail.lower():
                if id_excluir is not None and i.id == id_excluir:
                    continue
                return True
        return False
    
    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        if self.__existe_mail(mail):
            raise DuplicadoError(f"El mail '{mail}' ya está registrado.")
        nuevo_usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(nuevo_usuario)
        return nuevo_usuario
    
    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for i in self.__usuarios:
            if i.id == id_usuario and not i.eliminado:
                return i
        raise EntidadNoEncontradaError(f"No se encontró un usuario activo con ID {id_usuario}.")

    
    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    
    def eliminar(self, id_usuario: int, id_sesion: int) -> None:
        if id_usuario == id_sesion:
            raise OperacionNoPermitidaError("No puedes eliminarte a ti mismo.")
        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminar()
    
    
    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for i in self.__usuarios:
            if i.mail.lower() == mail.lower():
                if not i.eliminado and i.verificar_contrasenia(contrasenia):
                    return i
                break
                
        raise CredencialesInvalidasError("Mail o/y contraseña incorrectos.")

    def editar(self, id_usuario: int, nombre: str | None = None, apellido: str | None = None, mail: str | None = None, celular: str | None = None, contrasenia: str | None = None, rol: Rol | None = None) -> None: 
        usuario = self.buscar_por_id(id_usuario)
        if mail is not None and mail.lower() != usuario.mail.lower():
            if self.__existe_mail(mail, id_excluir=usuario.id):
                raise DuplicadoError(f"El mail '{mail}' ya está en uso por otro usuario.")
            usuario.mail = mail

        if nombre is not None: usuario.nombre = nombre
        if apellido is not None: usuario.apellido = apellido
        if celular is not None: usuario.celular = celular
        if rol is not None: usuario.rol = rol
        if contrasenia is not None:
            usuario._Usuario__contrasenia = contrasenia