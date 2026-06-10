from typing import Callable
import os
from xml.dom.minidom import Element

from utils.input import CapturaInput, Pressionado, estaPressionado, tarefa
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
    print(separador * int(largura / 2), conteudo, separador * int(largura / 2))
            



def menu(titulo: str, opcoes: list[Opcao], colunas: int = 3, top: Callable[[], Elemento] = lambda : Texto("")):
    selecionado = 0
    
    def selecionar(i :int, e: Elemento) -> Elemento:
        if i == selecionado:
            e.efeitos = [Cores1B.ROXO.value.efeito(CorAlvo.TEXTO)]
            return e
        else:
            e.efeitos = []
            return e
    while True:
        limpar()
        if estaPressionado("a") and selecionado > 0:
            selecionado-=1
        elif estaPressionado("w") and selecionado > colunas - 1:
            selecionado-=colunas
            
        elif estaPressionado("d") and selecionado < len(opcoes) - 1:
            selecionado+=1
        elif estaPressionado("s") and selecionado + colunas <= len(opcoes) - 1:
            selecionado+=colunas
        if estaPressionado("\n"):
            break
        print(Coluna([Texto(titulo),
            Texto("use w para subir uma opção, s para descer, a para ir a esquerda, d para a direita, e enter para escolher"),]).renderizar())
        print(top().renderizar())
        print(Coluna([
            
            Tabela(colunas, list(map(lambda x: selecionar(x[0], x[1].texto), enumerate(opcoes))))
        ]).renderizar())
        # print("\n")
        
        esperar(0.5)
    opcoes[selecionado].codigo()
        # def renderizar():
        #     limpar()       
            
        #     for i, opcao in enumerate(opcoes):
        #         if i == selecionado:
                   
        #         else:
        #             print(opcao.texto.ren) 
        #         print(("-> " if i == selecionado else "   ") + f"{opcao.texto}")
        #     largura = os.get_terminal_size().columns
        #     print("-" * largura)
        # renderizar()
        
