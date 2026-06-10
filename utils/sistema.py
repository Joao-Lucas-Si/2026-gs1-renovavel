import os
from time import sleep

from utils.input import CapturaInput, estaPressionado


def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar(tempo: float):
    sleep(tempo)

def pausar():

    # print("\nPressione Enter para continuar")
    esperar(0.5)
    while True:
        if estaPressionado("\n"):
            break
        esperar(0.5)
    limpar()    
