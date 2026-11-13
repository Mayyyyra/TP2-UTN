import Base
import Rol
class Usuario(Base):
    def __init__(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str,rol:Rol):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.contrasenia = contrasenia

        super().__init__(Base)
    def verificar_contrasenia(self,contrasenia: str) -> bool:
        if contrasenia == self.__contrasenia:
            return True
    def __str__(self):
        return f"Nombre:{self.__nombre}|Apellido:{self.__apellido}|\nmail:{self.__mail}|Celular:{self.__celular}"