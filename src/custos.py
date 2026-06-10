from enum import Enum

# temperatura = 0 , 50
# comunicacao = 0 , 100
# energia = 0.0 , 100.000
# oxigenio = 0 , 100
# modulo = 0 , 100

class Caracteristica(Enum):
    TEMPERATURA=1,
    COMUNICACAO=2,
    MODULO=3,
    OXIGENIO=4,
    

class Custo:
    energia: int
    caracteristica: Caracteristica   
    valor: float
    
    @property
    def energia_gasta(self):
        return self.calcular_gasto(self.valor)
    
    @property
    def incremento(self):
        return int(self.maximo * self.valor)
    
    def calcular_gasto(self, valor: float):
        return int(self.energia * (valor/self.maximo))
    
    def __init__(self, energia: int, caracteristica: Caracteristica, valor: float, maximo: int = 0) -> None:
        self.energia = energia
        self.caracteristica = caracteristica
        self.valor = valor
        self.maximo = maximo