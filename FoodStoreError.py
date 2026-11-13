
class FoodStoreError(Exception):
    pass
class EntidadNoEncontradaError(FoodStoreError):
    "No pudimos encontrar la id, revise si la id que puso es correcta o esta eliminada"
class DatoInvalidoError(FoodStoreError):
    "Este dato no es un dato valido"
class StockInsuficienteError(FoodStoreError):
    pass
class DuplicadoError(FoodStoreError):
    pass
class OperacionNoPermitidaError(FoodStoreError):
    pass
class CredencialesInvalidasError(FoodStoreError):
    pass