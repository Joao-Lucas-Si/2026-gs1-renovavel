from utils.tui.render.elementos import Ascii, AsciiAnimado
from src.database import Database
from utils.sistema import  esperar, limpar
from utils.tui.render.elementos import Coluna, Tabela, Texto
import os

def derrota():
    i = 0
    
    def elemento(i: int):
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
        ).renderizar())
    def padrao():
        limpar()
        print(f"ocorreu um erro com a renderização de animação, o projeto foi desenvolvido em linux, então certas funcionalidades mais complexas podem não funcionar em mac ou windows")
        elemento(i)
    try:
        if os.name == "nt":
            padrao()
        else:
            from utils.tarefa import InputTarefa
            pressionado = InputTarefa()
            while True:
                
                pressionado.iniciar()
                elemento(i)
                if pressionado.pressionado:
                    break
                esperar(0.25)
                pressionado.terminar()
                i += 1
                limpar()
    except:
        padrao()
        




def vitoria():
    i = 0
    def elemento(i: int):
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
                            Texto("Dados finais da missão:\n"),
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
    def padrao():
        limpar()
        print(f"ocorreu um erro com a renderização de animação, o projeto foi desenvolvido em linux, então certas funcionalidades mais complexas podem não funcionar em mac ou windows")
        elemento(i)
    try:
        if os.name == "nt":
            padrao()
        else:
            from utils.tarefa import InputTarefa
            pressionado = InputTarefa()
            while True:
                
                pressionado.iniciar()
                elemento(i)
                if pressionado.pressionado:
                    break
                esperar(0.25)
                pressionado.terminar()
                i += 1
                limpar()
    except:
        padrao()
        