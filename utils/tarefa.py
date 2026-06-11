
import multiprocessing

import os
if os.name == "nt":
    multiprocessing.set_start_method('spawn')

class InputTarefa():
    
    def __init__(self) -> None:
        self.pressionado = False
    pressionado = False
    processo: multiprocessing.Process

    def input(self):
        try:
            stdin = open(0)
            stdin.readline()
        except: 
            pass
        # print("pressionado", self.pressionado)
        # InputTarefa.pressionado = True
        # print(self.pressionado)

    def iniciar(self):
        try:
            def inp():
                self.input()
            self.process = multiprocessing.Process(target = inp)
            self.process.start()
        except:
            self.pressionado = True
    def terminar(self):
        try:
            if not self.process.is_alive():
                self.pressionado = True
            self.process.terminate()
            self.process.join()
        except: 
            self.pressionado = True