
# class Parametro():
#     valor: int

class Database():
    energia = 10000
    temperatura = 100
    oxigenio = 100
    modulo = 100
    comunicacao = 100
    
    custo_temperatura = 20
    custo_oxigenio = 20
    custo_modulo = 20
    custo_comunicacao = 20
    
    tempo = 0

    @staticmethod
    def instancia():
        return db

db = Database()