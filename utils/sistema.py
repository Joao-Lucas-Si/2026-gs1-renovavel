import os
from threading import Thread
from time import sleep

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar(tempo: float):
    sleep(tempo)

def pausar():
    input()
    limpar()    
