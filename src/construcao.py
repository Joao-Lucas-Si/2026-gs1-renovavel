import random
from typing import Optional

from src.database import Database
from src.missao import missao
from src.nave import Nave, printarNave
from src.partes import (
    Bateria,
    Energia,
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


def obter_energia():
    energias: list[Energia] = [
        Energia("Solar", 2, 0),
        Energia("Biogas", 4, 0),
        Energia("Fossil", 1, 2),
    ]

    menu(
        "abastecendo",
        [
            Opcao(
                Coluna([Texto(f"{i + 1}. {energia.nome}")]), lambda: abastecer(energia)
            )
            for i, energia in enumerate(energias)
        ],
    )


def abastecer(energia: Energia):
    db = Database.instancia()
    while True:
        try:
            valor = int(
                input(f"digite a quantidade de combustivel({nave.bateria.energia}): ")
            )

            if 0 < valor < nave.bateria.energia:
                preco = int((valor / 2) * energia.custo)

                if preco > db.orcamento:
                    print(preco, db.orcamento)
                    print("orçamento limitado para a quantidade requerida")
                    continue
                db.energia = valor
                break
            else:
                print("valor invalido")
        except:
            print("valor invalido")


def construir_nave():
    global financiamento
    db = Database.instancia()
    db.tempo = random.randint(6, 15)
    financiamento = db.temperatura * 100
    continuar = True
    def iniciar():
        global nave
        nonlocal continuar
        continuar = False
        obter_energia()
        missao(nave)

    while continuar:
        menu(
            "selecione",
            [
                Opcao(Coluna([Texto("1. Começar")]), iniciar),
                Opcao(
                    Coluna([Texto("2. Escolha de propulsores")]), selecionar_propulsor
                ),
                Opcao(Coluna([Texto("3. Escolha de bateria")]), selecionar_bateria),
                Opcao(Coluna([Texto("4. Escolha de gerador")]), selecionar_gerador),
            ],
            top=lambda: Coluna(
                [Texto(f"orçamento: {db.orcamento}, tempo estimado: {db.tempo}"), Texto(printarNave(nave))]
            ),
        )


def selecionar_propulsor():
    def a(propulsor: Propulsor):

        def b():
            nave.propulsor = propulsor

        return b

    menu(
        "selecao de propulsores",
        [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 1}. {propulsor.nome}"),
                        Texto(f"preço: {propulsor.preco}"),
                        Texto(f"velocidade: {propulsor.velocidade}"),
                    ]
                ),
                a(propulsor),
            )
            for i, propulsor in enumerate(
                [propulsor_basico, propulsor_luz, propulsor_hiper]
            )
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
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 1}. {bateria.nome}"),
                        Texto(f"preço: {bateria.preco}"),
                        Texto(f"capacidade: {bateria.energia}"),
                    ]
                ),
                a(bateria),
            )
            for i, bateria in enumerate(
                [
                    bateria_basica,
                    bateria_media,
                    bateria_velha,
                    bateria_reserva,
                    bateria_avancada,
                ]
            )
        ],
    )


def selecionar_gerador():
    def a(gerador: Gerador | None):
        def b():
            nave.gerador = gerador

        return b

    menu(
        "selecao de geradores",
        [Opcao(Coluna([Texto("1. nenhum")]), a(None))]
        + [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 2}. {bateria.nome}"),
                        Texto(f"preço: {bateria.preco}"),
                        Texto(f"energia: {bateria.energia}"),
                    ]
                ),
                a(bateria),
            )
            for i, bateria in enumerate(
                [
                    gerador_solar,
                    gerador_fissao_nuclear,
                    gerador_biocombustivel,
                    gerador_biogas,
                    gerador_fusao_nuclear,
                ]
            )
        ],
        # [
        #     Opcao(
        #         Coluna([Texto("gerador solar")]),
        #         a(gerador_solar),
        #     ),
        #     Opcao(Coluna([Texto("Gerador de Biogás")]), a(gerador_biogas)),
        #     Opcao(
        #         Coluna([Texto("Gerador de Biocombustivel ")]), a(gerador_biocombustivel)
        #     ),
        #     Opcao(
        #         Coluna([Texto("Gerador de fusão Nucelar")]), a(gerador_fusao_nuclear)
        #     ),
        #     Opcao(
        #         Coluna([Texto("Gerador de fissão Nuclear")]), a(gerador_fissao_nuclear)
        #     ),
        # ],
    )
