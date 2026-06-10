from utils.input import estaPressionado
from utils.tui.render.elementos import Ascii, AsciiAnimado
from src.database import Database
from utils.sistema import esperar, limpar
from utils.tui.render.elementos import Coluna, Tabela, Texto


def derrota():
    i = 0
    while True:
        print(Tabela(
            2,
            [
                Coluna(
                    [
                        Texto("Você sucumbiu"),
                        Texto("Dados da missão"),
                        Texto(f"energia: {Database.instancia().energia}"),
                        Texto(f"oxigênio: {Database.instancia().oxigenio}"),
                        Texto(f"modulo: {Database.instancia().modulo}"),
                        Texto(f"comunicação: {Database.instancia().comunicacao}"),
                        Texto(f"temperatura: {Database.instancia().temperatura}"),
                    ]
                ),
                Coluna([AsciiAnimado("recursos/ascii/esqueleto.txt", i, 31)]),
            ],
        ).renderizar()
        )
        esperar(0.1)
        i += 1
        limpar()


# def derrota():
#     i = 0
#     estados: list[Dado] = [
#         {"estado": estado_temperatura(dados_atuais[0]), "dado": "temperatura"},
#         {"estado": estado_comunicacao(dados_atuais[1]), "dado": "comunicação"},
#         {"estado": estado_bateria(dados_atuais[2]),"dado": "bateria"},
#         {"estado": estado_oxigenio(dados_atuais[3]),"dado": "oxigenio"},
#         {"estado": estado_estabilidade(dados_atuais[4]),"dado": "estabilidade"},
#         {"estado": estado_integridade(dados_atuais[5]),"dado": "integridade"},
#         {"estado": estado_motor(dados_atuais[6]),"dado": "motor"},
#     ]
#     dados = Coluna([Texto("Infelizmente, você morreu"), Texto(""), Texto("estados criticos")])
#     motivos = [Texto(f"{estado["dado"]}: {estado['estado'].name}") for estado in estados if estado["estado"] != Estado.ESTAVEL and estado["estado"] != Estado.MORTIFERO]
#     dados.filhos.extend(motivos)
#     dados.filhos.append(Texto(""))
#     dados.filhos.append(Texto(f"causa da morte: {','.join(estado["dado"] for estado in estados if estado["estado"] == Estado.MORTIFERO)}"))
#     while True:
#         if estaPressionado("\n"):
#             break

#         print(
#             Tabela(
#                 2,
#                 [
#                     dados,
#                     Coluna([AsciiAnimado("recursos/ascii/esqueleto.txt", i, 31)]),
#                 ],
#             ).renderizar()
#         )
#         esperar(0.1)
#         i += 1
#         limpar()


def vitoria():
    i = 0
    while True:
        if estaPressionado("\n") or estaPressionado("\r"):
            break
        print(
            Tabela(
                2,
                [
                    Coluna(
                        [
                            AsciiAnimado("recursos/ascii/parabens.txt", i, 14),
                        ],
                    ),
                    Coluna(
                        [
                            Texto("Parabéns, Você sobreviveu!\n"),
                            Texto("Dados coletados durante a missão:\n"),
                            Texto(f"Energia: {Database.instancia().energia}"),
                            Texto(f"\nTemperatura: {Database.instancia().temperatura}"),
                            Texto(f"\nOxigenio: {Database.instancia().oxigenio}"),
                            Texto(f"\nModulo: {Database.instancia().modulo}"),
                            Texto(f"\nComunicações: {Database.instancia().comunicacao}"),
                        ]
                    ),
                ],
            ).renderizar()
        )
        esperar(0.25)
        i += 1
        limpar()


# def vitoria():
#     i = 0
#     while True:
#         if estaPressionado("\n"):
#             break
#         print(
#             Tabela(
#                 3,
#                 [
#                     Coluna(
#                         [
#                             Texto("parabens, voce não morreu"),
#                             AsciiAnimado("recursos/ascii/parabens.txt", i, 14),

#                             # , efeitos=[Cores1B.AZUL.value.efeito(CorAlvo.TEXTO)]
#                         ]
#                     ),
#                     Coluna(
#                         [
#                             Ascii("recursos/ascii/dinheiro.txt"),
#                             Coluna(
#                                 [
#                                     Texto(f"{material.name}:{material.value.valor}")
#                                     for material in banco_dados.asteroide.materiais
#                                 ]
#                             ),
#                         ]
#                     ),
#                     Coluna([Ascii("recursos/ascii/astronauta-inteiro.txt" , efeitos=[Cores1B.ROXO.value.efeito(CorAlvo.TEXTO)])]),
#                     # , efeitos=[Cores1B.ROXO.value.efeito(CorAlvo.TEXTO)]
#                 ],
#             ).renderizar()
#         )
#         esperar(0.25)
#         i += 1
#         limpar()
