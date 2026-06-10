from abc import ABC, abstractmethod
from typing import Optional



class Cursor(ABC):
    
    @abstractmethod
    def escrever(self, y: int, x: int, content: str):
        pass
    
class Linha():
    y: int
    x: int
    char: str

# class CursesCursor(Cursor):
    
#     def __init__(self, janela: Optional[curses.window] = None) -> None:
#         super().__init__()
#         if janela:
#             self.janela = janela
    
#     def escrever(self, y: int, x: int, content: str):
#         self.janela.addstr(y, x, content)
#         self.janela.refresh()
    
#     @staticmethod
#     def iniciar():
#         def instanciar(janela: curses.window):
#             global curse
#             curse = CursesCursor(janela)
            
#             max = janela.getmaxyx()
#             for i in range(max[0] - 2):
#                 for j in range(max[1]):
#                     curse.escrever(i, j, " ")
#         curses.wrapper(instanciar)
        
#     @property
#     def instancia(self) -> Cursor:
#         return curse

# curse: CursesCursor

class PrintCursos(Cursor):
    linhas: list[Linha]
    linhaAtual: int = 0
    colunaAtual: int = 0
    def escrever(self, y: int, x: int, content: str):
        print(f"\033[{y}{x}f")
        # if self.linhaAtual != y:
        #     if y > self.linhaAtual:
        #         print(f"\033[{y - self.linhaAtual}B", end="")
        #     else:
        #         print(f"\033[{self.linhaAtual - y}A")
        # if self.colunaAtual != x:
        #     if x > self.colunaAtual:
        #         print(f"\033[{x - self.colunaAtual}C", end="")
        #     else:
        #         print(f"\033[{self.colunaAtual - y}D")
        
        print(f"{content}", end="")
        self.colunaAtual += len(content) - 1
        # if 
        # for i, char in enumerate(content):
        #     linha = next(linha for linha in self.linhas if linha.x == x + i and linha.y == y)
            
        #     if linha:
        #         linha.char = char
        #     else:
        #         self.linhas.append
        # return super().escrever(y, x, content)