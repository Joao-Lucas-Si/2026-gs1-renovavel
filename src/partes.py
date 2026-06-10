class Parte():
    nome: str
    preco: int
    def __init__(self, nome: str, preco: int) -> None:
        self.nome = nome
        self.preco = preco

class Bateria(Parte):
    energia:int
    
    def __init__(self, energia: int, nome: str, preco: int) -> None:
        super().__init__(nome, preco)
        self.energia = energia

bateria_avancada = Bateria(5000, "Bateria Modo Superior", 1000)
bateria_media = Bateria(3500, "Bateria Modo Média", 500)
bateria_basica = Bateria(2000, "Bateria Modo Básica", 300)
# bateria_reserva = Bateria(2000, "Bateria de Reserva", 100)
bateria_velha = Bateria(1000, "Bateria Modo Velha", 50)


class Energia():
    nome: str
    custo: float
    poluicao: int
    
    def __init__(self,  nome: str, custo: float, poluicao: int) -> None:
        self.nome = nome
        self.custo = custo
        self.poluicao = poluicao

class Gerador(Parte):
    energia: int
    
    def __init__(self,nome: str, energia: int, preco: int) -> None:
        super().__init__(nome, preco)
        self.energia = energia
        



class GeradorNaoRenovavel(Gerador):
    impacto: int
    
    def __init__(self, nome: str, energia: int, preco: int, impacto: int = 0) -> None:
        super().__init__(nome, energia, preco)
        self.impacto = impacto
    pass

gerador_solar = Gerador("gerador solar", 50, 1000)
gerador_biogas = Gerador("gerador po gás", 25, 1000)
gerador_fusao_nuclear = GeradorNaoRenovavel("mini nuclear", 100, 1000)
# gerador_fissao_nuclear = GeradorNaoRenovavel("Gerador por fissão nuclear", 55000, 1000)
gerador_combustivel = GeradorNaoRenovavel("Gerador de combustivel", 50, 1000)


class Propulsor(Parte):
    velocidade: int
    energia: int
    def __init__(self, nome: str, velocidade: int, energia: int, preco: int) -> None:
        super().__init__(nome, preco)
        self.velocidade = velocidade
        self.energia = energia
        
propulsor_luz = Propulsor("propulsor de luz", 2, 100, 150)
propulsor_hiper = Propulsor("propulsor hiper", 3, 50, 250)
propulsor_basico = Propulsor("propolsor básico", 0, 10, 50)
