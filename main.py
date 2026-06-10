import atexit

from src.construcao import construir_nave
from src.nave import printarNave
from utils.input import CapturaInput


def main():
    CapturaInput.iniciar()
    # print(construir_nave())
    construir_nave()
    
def sair():
    CapturaInput.finalizar()

if __name__ == "__main__":
    atexit.register(sair)
    main()