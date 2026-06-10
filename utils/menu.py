from typing import Callable
import os
from xml.dom.minidom import Element
from utils.sistema import esperar, limpar
from utils.tui.efeitos import CorAlvo, Cores1B
from utils.tui.render.elementos import Coluna, Elemento, Tabela, Texto


class Opcao():
    texto: Coluna
    codigo: Callable[[], None]
    def __init__(self, texto: Coluna, codigo: Callable[[], None]) -> None:
        self.texto = texto
        self.codigo = codigo

def centralizar(conteudo: str, separador: str = "-"):
    largura = os.get_terminal_size().columns
            
    largura -= len(conteudo)
    if largura % 2 != 0:
        largura -=2
    print(separador * int(largura / 2), conteudo, separador * int(largura / 2),  flush=True)
            



def menu(titulo: str, opcoes: list[Opcao], colunas: int = 3, top: Callable[[], Elemento] = lambda : Texto("")):
    selecionado = 0
    
    # def selecionar(i :int, e: Elemento) -> Elemento:
    #     if i == selecionado:
    #         e.efeitos = [Cores1B.ROXO.value.efeito(CorAlvo.TEXTO)]
    #         return e
    #     else:
    #         e.efeitos = []
    #         return e
    while True:
        print(Coluna([Texto(titulo)]).renderizar())
        print(top().renderizar())
        print(Coluna([
            
            Tabela(colunas, list(map(lambda x: x.texto,opcoes)))
        ]).renderizar())
        # print("\n")
        try:
            
            selecionado = int(input("escolha: "))
            limpar()
            if selecionado > 0 and selecionado <= len(opcoes):
                selecionado -= 1
                break
            else:
                print("opção invalida")
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt()
            limpar()
            print("valor invalido")
    
    opcoes[selecionado].codigo()
        
