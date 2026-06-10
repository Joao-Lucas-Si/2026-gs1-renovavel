from typing import Callable

from utils.sistema import esperar
from utils.tui.render.elementos import Elemento


def animarEscrita(conteudo: Elemento):
    caracteres = conteudo.renderizar().split(" ")
    
    for caractere in caracteres:
        print(caractere + " ", end="", flush=False)
        esperar(0.002)
        
def animarValor(inicial: int, final: int, passos: int, conteudo: Callable[[int], None]):
    atual = inicial
    while atual < final:
        conteudo(atual)
        
        atual+=passos