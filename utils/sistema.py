import multiprocessing
import os
from threading import Thread
from time import sleep

# def takeinput():
#     stdin = open(0)
#     print("give it up:", end = "", flush = 1)
#     x = stdin.readline()
#     print(x)
# if __name__ == "__main__":
#     process = multiprocessing.Process(target = takeinput)
#     process.start()
#     time.sleep(5)
#     process.terminate()
#     process.join()
#     print("\nalright, times up!")



class InputTarefa():
    
    def __init__(self) -> None:
        self.pressionado = False
    pressionado = False
    processo: multiprocessing.Process

    def input(self):
        stdin = open(0)
        stdin.readline()
        # print("pressionado", self.pressionado)
        # InputTarefa.pressionado = True
        # print(self.pressionado)

    def iniciar(self):
        def inp():
            self.input()
        self.process = multiprocessing.Process(target = inp)
        self.process.start()

    def terminar(self):
        if not self.process.is_alive():
            self.pressionado = True
        self.process.terminate()
        self.process.join()

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar(tempo: float):
    sleep(tempo)

def pausar():
    print("pressione enter para continuar")
    input()
    limpar()    
