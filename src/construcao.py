import random
from typing import Optional

from src.database import Database
from src.missao import missao
from src.nave import Nave, printarNave
from src.partes import (
    Bateria,
    Gerador,
    Propulsor,
    bateria_basica,
    propulsor_basico,
    propulsor_hiper,
    propulsor_luz,
    bateria_avancada,
    bateria_media,
    bateria_reserva,
    bateria_velha,
    gerador_fissao_nuclear,
    gerador_biogas,
    gerador_biocombustivel,
    gerador_fusao_nuclear,
    gerador_solar,
)

from utils.menu import Opcao, menu
from utils.tui.efeitos import Cores1B
from utils.tui.render.elementos import Coluna, Texto


nave = Nave()
financiamento = 0

def obter_disponivel():
    return financiamento - sum(map(lambda parte: parte.preco, nave.partes))

def construir_nave():
    global financiamento
    db = Database.instancia()
    db.tempo = random.randint(6, 15)
    financiamento = db.temperatura * 100
    def iniciar():
        global nave
        missao(nave)
    while True:
        menu(
            "selecione",
            [
                Opcao(Coluna([Texto("Começar")]), iniciar),
                Opcao(Coluna([Texto("Escolha de propulsores")]), selecionar_propulsor),
                Opcao(Coluna([Texto("Escolha de bateria")]), selecionar_bateria),
                Opcao(Coluna([Texto("Escolha de gerador")]), selecionar_gerador),
            ],
            top=lambda : Coluna([Texto(printarNave(nave))])
        )

def selecionar_propulsor():
    def a(propulsor: Propulsor):
        
        def b():
            nave.propulsor = propulsor
        return b

    menu(
        "selecao de propulsores",
        [
            Opcao(Coluna([Texto("propulsor de basico")]), a(propulsor_basico)),
            Opcao(Coluna([Texto("propulsor hiper")]), a(propulsor_hiper)),
            Opcao(Coluna([Texto("propulsor de luz")]), a(propulsor_luz)),
        ],
    )


def selecionar_bateria():
    def a(bateria: Bateria):
        def b():
            nave.bateria = bateria            
        return b

    menu(
        "selecao de baterias",
        [
            Opcao(Coluna([Texto("bateria velha")]), a(bateria_velha)),
            Opcao(Coluna([Texto("bateria basica")]), a(bateria_basica)),
            Opcao(Coluna([Texto("bateria media")]), a(bateria_media)),
            Opcao(Coluna([Texto("bateria avancada")]), a(bateria_avancada)),
            Opcao(Coluna([Texto("bateria reserva")]), a(bateria_reserva)),
        ],
    )


def selecionar_gerador():
    def a(gerador: Gerador):
        def b():
            nave.gerador = gerador            
        return b

    menu(
        "selecao de geradores",
        [
            Opcao(
                Coluna([Texto("gerador solar")]),
                a(gerador_solar),
            ),
            Opcao(Coluna([Texto("Gerador de Biogás")]), a(gerador_biogas)),
            Opcao(Coluna([Texto("Gerador de Biocombustivel ")]), a(gerador_biocombustivel)),
            Opcao(Coluna([Texto("Gerador de fusão Nucelar")]), a(gerador_fusao_nuclear)),
            Opcao(Coluna([Texto("Gerador de fissão Nuclear")]), a(gerador_fissao_nuclear)),
        ],
    )
