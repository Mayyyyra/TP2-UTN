from Entidades.Base import Base
from Entidades.Rol import Rol
from Exepciones.FoodStoreError import DatoInvalidoError
class Usuario(Base):
    def __init__(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str,rol:Rol):
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia = contrasenia
        self.rol = rol
        

    #-------------
    @property
    def nombre(self) -> str:
        return self.__nombre
    @property
    def apellido(self) -> str:
        return self.__apellido
    @property
    def mail(self) -> str:
        return self.__mail
    @property
    def celular(self) -> str:
        return self.__celular
    @property
    def rol(self) -> Rol:
        return self.__rol
        #-----------
    @nombre.setter
    def nombre(self,valor:str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("Este valor esta vacio")
        self.__nombre = valor.strip()
    @apellido.setter
    def apellido(self,valor:str) -> None:
            if not valor.strip():
                raise DatoInvalidoError("Este valor esta vacio")
            self.__apellido = valor.strip()
    @mail.setter
    def mail(self,valor:str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("Este valor esta vacio")
        if "@" not in valor or not "." in valor:
            raise DatoInvalidoError("este valor no es un mail valido")
        self.__mail = valor.strip()

    @celular.setter
    def celular(self,valor:str) -> None:
        try:
            int(valor.replace("+", ""))
            self.__celular = valor.strip()
        except ValueError:
            raise DatoInvalidoError("El celular debe contener solo números (puede iniciar con +).")
        
    @rol.setter
    def rol(self,valor:Rol) -> None:
        if not isinstance(valor,Rol):
            raise DatoInvalidoError("este valor no es un rol valido")
        self.__rol = valor
    #--------------
    def verificar_contrasenia(self,contrasenia: str) -> bool:
        return contrasenia == self.__contrasenia
        
    def __str__(self):
        return f"Nombre:{self.__nombre}|Apellido:{self.__apellido}|\nmail:{self.__mail}|Celular:{self.__celular}"