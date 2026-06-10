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
    
class Nivel():
    valor: int
    gasto: int
    nivel: int
    
    def __init__(self, valor: int, gasto: int) -> None:
        self.valor = valor
        self.gasto = gasto
        # self.nivel = nivel
    

class Custo:
    energia: int
    caracteristica: Caracteristica   
    valor: int
    niveis: list[Nivel]
    
    @property
    def energia_gasta(self):
        return self.calcular_gasto(self.valor)
    
    def calcular_gasto(self, valor: int):
        return int(self.energia * (valor/self.maximo))
    def __init__(self, energia: int, caracteristica: Caracteristica, valor: int, maximo: int = 0, niveis: list[Nivel] = []) -> None:
        self.energia = energia
        self.caracteristica = caracteristica
        self.valor = valor
        self.maximo = maximo
        self.niveis = niveis
