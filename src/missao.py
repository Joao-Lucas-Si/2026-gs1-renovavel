from ast import mod
from time import sleep

from src.database import Database
from src.nave import printarNave
from src.custos import Caracteristica, Custo
from src.nave import Nave
from src.telas import derrota, vitoria
from utils.sistema import limpar
from utils.tui.render.elementos import Coluna, Tabela, Texto

custos = [
    Custo(200, Caracteristica.TEMPERATURA, 10, ),
    Custo(100, Caracteristica.COMUNICACAO, 5),
    Custo(250, Caracteristica.MODULO, 10),
    Custo(200, Caracteristica.OXIGENIO, 10),
]



tempo = 10000000000000

def missao(nave: Nave):
    global tempo
    db = Database.instancia()
    while tempo > 0 and db.energia > 0:
        limpar()
        print(menuMisao(nave).renderizar())
        aplicarCustos()
        sleep(1)
        tempo-=1
        
    if db.energia < 0:
        derrota()
        pass
    else:
        vitoria()
        pass

def aplicarCustos():
    db = Database.instancia()
    for custo in custos:
        match (custo.caracteristica):
            case Caracteristica.TEMPERATURA:
                db.temperatura += custo.valor
            case Caracteristica.COMUNICACAO:
                db.comunicacao += custo.valor
            case Caracteristica.OXIGENIO:
                db.oxigenio += custo.valor
            case Caracteristica.MODULO:
                db.modulo += custo.valor
        db.energia -= custo.energia


def menuMisao(nave: Nave):
    # printarNave
    db = Database.instancia()
    
    return Tabela(
        2,
        [
            Tabela(
                2,
                [
                    Coluna([Texto("Energia")]),
                    Coluna([Texto(f"{db.energia}")]),
                    Coluna([Texto("Oxigênio")]),
                    Coluna([Texto(f"{db.oxigenio}")]),
                    Coluna([Texto("Temperatura")]),
                    Coluna([Texto(f"{db.temperatura}")]),
                    Coluna([Texto("Modulo")]),
                    Coluna([Texto(f"{db.modulo}")]),
                    Coluna([Texto("Comunicação")]),
                    Coluna([Texto(f"{db.comunicacao}")]),
                ],
            ),
            Coluna([Texto(printarNave(nave))])
        ],
    )
