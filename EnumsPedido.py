from enum import Enum

class FormaPago(Enum):
    TARJETA = "Tarjeta"
    TRANSFERENCIA =  "Transferencia"
    EFECTICO = "Efectivo"

class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO =  "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"