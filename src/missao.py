import random
from time import sleep

from src.partes import GeradorNaoRenovavel
from src.database import Database, Tendencia, Tendencias
from src.nave import printarNave
from src.custos import Caracteristica, Custo
from src.nave import Nave
from src.telas import derrota, vitoria
from utils.menu import Opcao, menu
from utils.sistema import limpar
from utils.tui.render.elementos import Coluna, Tabela, Texto

custos = [
    Custo(
        20,
        Caracteristica.TEMPERATURA,
        0.25,
        30,
    ),
    Custo(10, Caracteristica.COMUNICACAO, 0.25, 30),
    Custo(25, Caracteristica.MODULO, 0.25, 30),
    Custo(20, Caracteristica.OXIGENIO, 0.25, 30),
]


def parametro_mortifero():
    db = Database.instancia()
    return (
        db.temperatura <= -40 or db.oxigenio <= 0 or db.modulo <= 0 or db.comunicacao <= 0
    )


def mudar_tendencias():
    db = Database.instancia()

    for tendencia in db.tendencias:
        if tendencia.tendencia.atividade >= tendencia.tendencia.duracao:
            chance = random.randint(0, 10)
            duracao = random.randint(2, 5)
            if chance > 8:

                tendencia.tendencia = Tendencias.CRITICO.value.novo(duracao)
            elif chance > 6:
                tendencia.tendencia = Tendencias.ATENCAO.value.novo(duracao)
            else:
                tendencia.tendencia = Tendencias.ESTAVEL.value.novo(duracao)


def missao(nave: Nave):
    db = Database.instancia()
    db.tempo -= nave.propulsor.velocidade
    while db.atual <= db.tempo and db.energia > 0 and not parametro_mortifero():
        limpar()

        def nada():
            pass

        def configurar():
            def porcentagem() -> float:
                valor: float = 0

                def aplicar(a: float):
                    def callback():
                        nonlocal valor
                        valor = a

                    return callback

                menu(
                    "redirecionamento de energia",
                    [
                        Opcao(Coluna([Texto("1. 25%")]), aplicar(0.25)),
                        Opcao(Coluna([Texto("2. 50%")]), aplicar(0.5)),
                        Opcao(Coluna([Texto("3. 74%")]), aplicar(0.75)),
                        Opcao(Coluna([Texto("4. 100%")]), aplicar(1)),
                    ],
                )
                return valor
                # while True:hile True:
                #     try:

                #         valor = int(
                #             input("quanta energia será distribuida(de 0 a 100%)?:")
                #         )

                #         if 0 <= valor <= 100:
                #             return valor / 100
                #         print("valor invalido")
                #     except:
                #         print("valor invalido
                #     try:

                #         valor = int(
                #             input("quanta energia será distribuida(de 0 a 100%)?:")
                #         )

                #         if 0 <= valor <= 100:
                #             return valor / 100
                #         print("valor invalido")
                #     except:
                #         print("valor invalido")

            def atribuir(caracteristica: Caracteristica):
                def callback():
                    valor = porcentagem()

                    match (caracteristica):
                        case Caracteristica.TEMPERATURA:
                            custos[0].valor = valor
                        case Caracteristica.COMUNICACAO:
                            custos[1].valor = valor
                        case Caracteristica.MODULO:
                            custos[2].valor = valor
                        case Caracteristica.OXIGENIO:
                            custos[3].valor = valor

                return callback

            menu(
                "Configurar",
                [
                    Opcao(
                        Coluna([Texto("1. Temperatura")]),
                        atribuir(Caracteristica.TEMPERATURA),
                    ),
                    Opcao(
                        Coluna([Texto("2. Comunicação")]),
                        atribuir(Caracteristica.COMUNICACAO),
                    ),
                    Opcao(
                        Coluna([Texto("3. Oxigenio")]),
                        atribuir(Caracteristica.OXIGENIO),
                    ),
                    Opcao(
                        Coluna([Texto("4. modulo")]),
                        atribuir(Caracteristica.MODULO),
                    ),
                ],
            )

        menu(
            f"Ciclo {db.atual}",
            [
                Opcao(Coluna([Texto("1. continuar")]), codigo=nada),
                Opcao(Coluna([Texto("2. configurar")]), codigo=configurar),
            ],
            colunas=2,
            top=lambda: menuMisao(nave),
        )
        if nave.gerador:
            db.energia = nave.gerador.energia
            if isinstance(nave.gerador, GeradorNaoRenovavel):
                db.poluicao += nave.gerador.impacto
        aplicarCustos()
        aplicarTendencia()
        for tendencia in db.tendencias:
            tendencia.tendencia.atividade += 1
        mudar_tendencias()

        db.atual += 1

    if db.energia < 0 or parametro_mortifero():
        derrota()
        pass
    else:
        vitoria()
        pass


def aplicarTendencia():
    db = Database.instancia()
    for tendencia in db.tendencias:
        valor = tendencia.tendencia.aplicar()
        match (tendencia.caracteristica):
            case Caracteristica.TEMPERATURA:
                db.temperatura -= valor
                if db.temperatura < -40:
                    db.temperatura = -40
            case Caracteristica.COMUNICACAO:
                db.comunicacao -= valor

                if db.comunicacao < 0:
                   
                    db.comunicacao = 0
            case Caracteristica.OXIGENIO:
                db.oxigenio -= valor
                if db.oxigenio < 0:
                    db.oxigenio = 0
            case Caracteristica.MODULO:
                db.modulo -= valor
                if db.modulo < 0:
                    db.modulo = 0


def aplicarCustos():
    db = Database.instancia()
    for custo in custos:
        match (custo.caracteristica):
            case Caracteristica.TEMPERATURA:
                db.temperatura += custo.incremento
                if db.temperatura > 40:
                    db.temperatura = 40
            case Caracteristica.COMUNICACAO:
                db.comunicacao += custo.incremento
                if db.comunicacao > 100:
                    db.comunicacao = 100
            case Caracteristica.OXIGENIO:
                db.oxigenio += custo.incremento
                if db.oxigenio > 100:
                    db.oxigenio = 100
            case Caracteristica.MODULO:
                db.modulo += custo.incremento
                if db.modulo > 100:
                    db.modulo = 100
        db.energia -= custo.energia


def menuMisao(nave: Nave):
    # printarNave
    db = Database.instancia()

    return Coluna(
        [
            Tabela(
                2,
                [
                    Coluna([Texto("Energia")]),
                    Coluna([Texto(f"{db.energia}")]),
                    Coluna([Texto("Poluição")]),
                    Coluna([Texto(f"{db.poluicao}")]),
                ],
            ),
            Tabela(
                4,
                [
                    Coluna([Texto("Temperatura")]),
                    Coluna([Texto(f"{db.temperatura}")]),
                    Coluna([Texto(f"{custos[0].valor *100}%")]),
                    Coluna([Texto(f"{db.tendencias[0].tendencia.nome}")]),
                    Coluna([Texto("Comunicação")]),
                    Coluna([Texto(f"{db.comunicacao}")]),
                    Coluna([Texto(f"{custos[1].valor *100}%")]),
                    Coluna([Texto(f"{db.tendencias[1].tendencia.nome}")]),
                    Coluna([Texto("Modulo")]),
                    Coluna([Texto(f"{db.modulo}")]),
                    Coluna([Texto(f"{custos[2].valor *100}%")]),
                    Coluna([Texto(f"{db.tendencias[2].tendencia.nome}")]),
                    Coluna([Texto("Oxigênio")]),
                    Coluna([Texto(f"{db.oxigenio}")]),
                    Coluna([Texto(f"{custos[3].valor *100}%")]),
                    Coluna([Texto(f"{db.tendencias[3].tendencia.nome}")]),
                ],
            ),
            # Coluna([Texto(printarNave(nave))]),
        ]
    )
