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
    bateria_velha,
    gerador_biogas,
    gerador_combustivel,
    gerador_fusao_nuclear,
    gerador_solar,
)

from utils.menu import Opcao, menu
from utils.tui.efeitos import Cores1B
from utils.tui.render.elementos import Coluna, Texto

nave = Nave()


def obter_energia():
    energias: list[Energia] = [
        Energia("Solar", 1, 0),
        Energia("Biogas", 2, 0),
        Energia("Fossil", 0.5, 2),
        Energia("Nuclear", 2.5, 4),
    ]
    db = Database.instancia()
    disponivel = db.orcamento - db.gastos()
    menu(
        f"abastecendo ({disponivel})",
        [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 1}. {energia.nome}"),
                        Texto(f"preco por energia: {energia.custo}"),
                        (
                            Texto(
                                f"{"lixo radioativo gerado por uso" if energia.nome == "Nuclear" else "poluição por uso"}: {energia.poluicao}"
                            )
                            if energia.poluicao > 0
                            else Texto("")
                        ),
                    ]
                ),
                lambda: abastecer(energia),
            )
            for i, energia in enumerate(energias)
        ],
    )


def abastecer(energia: Energia):
    db = Database.instancia()
    
    disponivel = db.orcamento - db.gastos()
    while True:
        try:
            valor = int(
                input(f"digite a quantidade de combustivel(maximo da bateria: {nave.bateria.energia}, maximo orçamentario: {int(disponivel / energia.custo)}): ")
            )

            if 0 < valor <= nave.bateria.energia:
                preco = int(valor * energia.custo)

                if preco > disponivel:
                    print("orçamento limitado para a quantidade requerida")
                    continue
                db.energia = valor
                db.poluicao = valor * energia.poluicao
                break
            else:
                print("valor invalido")
        except:
            print("valor invalido")


def construir_nave():
    global financiamento, nave
    db = Database.instancia()
    nave = db.nave
    db.tempo = random.randint(6, 15)
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
                [
                    Texto(
                        f"orçamento: {db.orcamento}, gastos atuais: {db.gastos()} tempo estimado: {db.tempo}"
                    ),
                    Texto(printarNave(nave)),
                ]
            ),
        )


def selecionar_propulsor():
    db = Database.instancia()
    disponivel = db.orcamento - db.gastos(Propulsor)

    def atribuir(propulsor: Propulsor):

        def callback():
            if disponivel - propulsor.preco > 0:

                nave.propulsor = propulsor
            else:
                print("valor excedente ao orçamento disponivel")
            nave.propulsor = propulsor

        return callback

    menu(
        f"selecao de propulsores ({disponivel} de orçamento disponivel)",
        [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 1}. {propulsor.nome}"),
                        Texto(f"preço: {propulsor.preco}"),
                        Texto(f"velocidade: {propulsor.velocidade}"),
                    ]
                ),
                atribuir(propulsor),
            )
            for i, propulsor in enumerate(
                [propulsor_basico, propulsor_luz, propulsor_hiper]
            )
        ],
    )


def selecionar_bateria():
    db = Database.instancia()
    disponivel = db.orcamento - db.gastos(Bateria)

    def atribuir(bateria: Bateria):
        def callback():
            if disponivel - bateria.preco > 0:

                nave.bateria = bateria
            else:
                print("valor excedente ao orçamento disponivel")

        return callback

    menu(
        f"selecao de baterias ({disponivel} de orçamento disponivel)",
        [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 1}. {bateria.nome}"),
                        Texto(f"preço: {bateria.preco}"),
                        Texto(f"capacidade: {bateria.energia}"),
                    ]
                ),
                atribuir(bateria),
            )
            for i, bateria in enumerate(
                [
                    bateria_basica,
                    bateria_media,
                    bateria_velha,
                    bateria_avancada,
                ]
            )
        ],
    )


def selecionar_gerador():
    db = Database.instancia()
    disponivel = db.orcamento - db.gastos(Propulsor)

    def atribuir(gerador: Gerador | None):
        def callback():
            if not gerador:
                nave.gerador = None
            elif disponivel - gerador.preco < db.orcamento:

                nave.gerador = gerador
            else:
                print("valor excedente ao orçamento disponivel")

        return callback

    menu(
        f"selecao de geradores ({disponivel} de orçamento disponivel)",
        [Opcao(Coluna([Texto("1. nenhum")]), atribuir(None))]
        + [
            Opcao(
                Coluna(
                    [
                        Texto(f"{i + 2}. {bateria.nome}"),
                        Texto(f"preço: {bateria.preco}"),
                        Texto(f"energia: {bateria.energia}"),
                    ]
                ),
                atribuir(bateria),
            )
            for i, bateria in enumerate(
                [
                    gerador_solar,
                    gerador_combustivel,
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
