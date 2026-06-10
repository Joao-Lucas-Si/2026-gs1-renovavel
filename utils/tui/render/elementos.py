from abc import ABC, abstractmethod
from enum import Enum
import math
from os import get_terminal_size
import re
from sys import stderr
from typing import Callable, Optional, overload, override

from utils.arquivos import ler_arquivo
from utils.input import obterTecla
from utils.tui.efeitos import Efeito, aplicarEfeitos, desaplicarEfeitos
from utils.tui.render.cursor import Cursor, PrintCursos


class Elemento(ABC):
    largura_disponivel: int
    altura_disponivel: int
    efeitos: list[Efeito] = []
    x: int = 0
    y: int = 0


    def escrever(self, janela: Cursor) -> None:
        pass

    def __init__(self, efeitos: Optional[list[Efeito]] = None) -> None:
        tamanho = get_terminal_size()
        self.largura_disponivel = tamanho.columns 
        self.altura_disponivel = tamanho.lines - 7
        if efeitos:
            self.efeitos = efeitos

    @property
    def tamanho(self) -> int:
        return 0

    @property
    def altura_dinamica(self) -> int:
        return 0

    def renderizar(self) -> str:
        return ""

    def estilizar(self, conteudo: str) -> str:
        return aplicarEfeitos(self.efeitos) + conteudo + desaplicarEfeitos()


class ContainerUnico(Elemento, ABC):
    filho: Elemento

    def __init__(self, filho: Elemento, largura: Optional[int] = None) -> None:
        super().__init__()
        self.filho = filho
        if largura:
            self.largura_disponivel = largura


class Container(Elemento, ABC):

    filhos: list[Elemento]

    def definir_largura(self, largura_disponivel: int):
        for filho in self.filhos:
            filho.largura_disponivel = largura_disponivel

    @property
    def tamanho_filhos(self):
        return sum(map(lambda x: x.tamanho, self.filhos))

    def renderizar_filhos(self):
        return "".join([filho.renderizar() for filho in self.filhos])

    def __init__(self, filhos: list[Elemento], largura: Optional[int] = None, efeitos: Optional[list[Efeito]] = None) -> None:
        super().__init__(efeitos)
        self.filhos = filhos
        if largura:
            self.largura_disponivel = largura
        self.definir_largura(self.largura_disponivel)


class EspacamentoVertical(Container):

    def escrever(self, janela: Cursor):

        return super().escrever(janela)

    @override
    def renderizar(self) -> str:
        return "\n" + super().renderizar() + "\n"

class Esquerda(ContainerUnico):
     
    def escrever(self, janela: Cursor) -> None:
        return super().escrever(janela)
    
    @property
    def tamanho(self) -> int:
        return self.largura_disponivel

    def renderizar(self) -> str:
        linhas: list[str] = []
        conteudo = self.filho.renderizar().split("\n")
        
        largura_parcial = self.largura_disponivel - self.filho.tamanho
        for linha in conteudo:
            linhas.append(linha + " " * largura_parcial)
        return "\n".join(linhas)

class Direita(ContainerUnico):
    
    def escrever(self, janela: Cursor) -> None:
        return super().escrever(janela)
    
    @property
    def tamanho(self) -> int:
        return self.largura_disponivel

    def renderizar(self) -> str:
        linhas: list[str] = []
        conteudo = self.filho.renderizar().split("\n")
        
        largura_parcial = self.largura_disponivel - self.filho.tamanho
        for linha in conteudo:
            linhas.append(" " * largura_parcial + linha)
        return "\n".join(linhas)

class Centralizado(Container):

    @property
    @override
    def tamanho(self) -> int:
        return self.largura_disponivel

    def escrever(self, janela: Cursor):
        largura_parcial = self.largura_disponivel - self.tamanho_filhos
        janela.escrever(self.x + largura_parcial, self.y, self.renderizar_filhos())

    @override
    def renderizar(self) -> str:
        largura_parcial = int((self.largura_disponivel - self.tamanho_filhos) / 2)
        espacos = " " * largura_parcial

        return espacos + self.renderizar_filhos() + espacos


def centralizarTopo(tamanho: int):
    altura = int((get_terminal_size().lines - tamanho) / 2)

    print("\n" * altura, end="")


class CentralizarVertical(ContainerUnico):

    def escrever(self, janela: Cursor):
        altura_filho = self.filho.altura_dinamica

        altura_parcial = int((self.altura_disponivel - altura_filho) / 2)

        self.filho.y = self.y + altura_parcial

        self.filho.escrever(janela)

    def renderizar(self) -> str:
        # altura = get_terminal_size().lines

        # conteudo = self.renderizar_filhos().split("\n")

        # for filho
        return super().renderizar()


class Alinhamento(Enum):
    CENTRO = 0
    ESQUERDA = 1
    DIREITA = 2


class Limites(ContainerUnico):
    largura: float
    
    def escrever(self, janela: Cursor) -> None:
        return super().escrever(janela)
    
    @property
    def tamanho(self) -> int:
        return int(self.largura_disponivel * self.largura)
    
    def __init__(self, filho: Elemento, porcento: float, largura: int | None = None) -> None:
        super().__init__(filho, largura)
        self.largura = porcento
 
    
    def renderizar(self) -> str:
        self.filho.largura_disponivel = self.tamanho
        return self.filho.renderizar()

def lenEstilizado(string: str):
    regexp = r"\\033\[.+m"
    
    return len(re.sub(regexp, "", string))

class Coluna(Container):
    alinhamento: Alinhamento

    def escrever(self, janela: Cursor) -> None:
        self.definir_largura(self.largura_disponivel)
        linhas: list[str] = []
        largura_disponivel = int(self.largura_disponivel * 0.9)
        x = int(self.largura_disponivel * 0.05)
        y = 0
       
        for filho in self.filhos:
            if isinstance(filho, Texto):
                for quebra in filho.conteudo.split("\n"):
                    if quebra:
                        for linha in self.quebrarLinhas(quebra):
                            janela.escrever(self.y + y, self.x + x,linha)
                            y += 1
            elif isinstance(filho, Ascii) or isinstance(filho, AsciiAnimado):
                filho.x = self.x + x
                filho.y = self.y + y
                filho.escrever(janela)
                y += filho.altura_dinamica
            else:
                filho.x = self.x + x
                filho.y = self.y + y
                filho.escrever(janela)
                y += filho.altura_dinamica
        return super().escrever(janela)

    @property
    def tamanho(self) -> int:
        return self.largura_disponivel

    def __init__(
        self,
        filhos: list[Elemento],
        alinhamento: Alinhamento = Alinhamento.CENTRO,
        largura: int | None = None,
        efeitos: Optional[list[Efeito]] = None
    ) -> None:
        super().__init__(filhos, largura, efeitos)
        self.alinhamento = alinhamento

    def quebrarLinhas(self, texto: str) -> list[str]:
        linhas: list[str] = [""]
        palavras = texto.split(" ")
        largura_disponivel = int(self.largura_disponivel * 0.9)
        atual = 0
        for palavra in palavras:
            if lenEstilizado(palavra) + lenEstilizado(linhas[atual]) > largura_disponivel:
                atual += 1
                linhas.append(palavra)
            else:

                linhas[atual] += " " + palavra

        return linhas

    def renderizar(self) -> str:
        self.definir_largura(self.largura_disponivel)
        linhas: list[str] = []
        largura_disponivel = int(self.largura_disponivel * 0.9)
        for filho in self.filhos:
            if isinstance(filho, Texto):
                for quebra in filho.conteudo.split("\n"):
                
                    linhas.extend(self.quebrarLinhas(quebra))
                    
            elif isinstance(filho, Ascii):
                linhas.extend(filho.renderizar().split("\n"))
            elif isinstance(filho, AsciiAnimado):
                linhas.extend(filho.renderizar().split("\n"))
            else:
                # for quebra in filho.renderizar():
                #     linhas.append(quebra)
                linhas.extend(filho.renderizar().split("\n"))

        for atual in range(len(linhas)):
            espacos_restantes = (
                self.largura_disponivel
                - lenEstilizado(linhas[atual])
               
            )
            if espacos_restantes > 0:
                if self.alinhamento == Alinhamento.CENTRO:

                    espaco_parcial = int(espacos_restantes / 2)
                    em_branco = espacos_restantes - (espaco_parcial * 2)
                    espacos = " " * espaco_parcial
                    linhas[atual] = (
                        espacos + linhas[atual] + espacos + (" " * em_branco)
                    )
                elif self.alinhamento == Alinhamento.DIREITA:
                    espaco_parcial = " " * espacos_restantes

                    linhas[atual] = espaco_parcial + linhas[atual]
                else:
                    espaco_parcial = " " * espacos_restantes

                    linhas[atual] = linhas[atual] + espaco_parcial
            if lenEstilizado(linhas[atual]) < largura_disponivel:
                linhas[atual] += " "
        return "\n".join([self.estilizar(linha) for linha in linhas])


class Texto(Elemento):
    conteudo: str

    def __init__(self, texto: str) -> None:
        self.conteudo = texto
        super().__init__()

    @property
    def altura_dinamica(self) -> int:
        return 1

    def escrever(self, janela: Cursor) -> None:
        janela.escrever(self.y, self.x, self.conteudo)

    @property
    @override
    def tamanho(self) -> int:
        return lenEstilizado(self.conteudo)

    @override
    def renderizar(self) -> str:
        return self.conteudo


class Linha(Container):

    @property
    def tamanho(self) -> int:
        
        return self.tamanho_filhos + len(self.filhos) - 1

    def escrever(self, janela: Cursor) -> None:
        x = 0
        for filho in self.filhos:
            filho.x = self.x + x
            filho.y = self.y
            filho.escrever(janela)
            x += filho.tamanho
            
    def renderizar_filhos(self):
        return super().renderizar_filhos()

    @override
    def renderizar(self) -> str:
        resultado = list(map(lambda filho:  filho.renderizar(), self.filhos))
        espaco_restante = self.largura_disponivel - self.tamanho_filhos - 1
        # print(' '.join(resultado))
        return f"{' '.join(resultado)}"


class AsciiAnimado(Elemento):
    caminho: str
    conteudo: str
    atual: int
    altura: int

    @property
    def altura_dinamica(self) -> int:
        return len(self.conteudo.split("\n"))

    @property
    def tamanho(self) -> int:
        return max(map(lambda x: lenEstilizado(x), self.conteudo.split("\n")))

    def escrever(self, janela: Cursor) -> None:
        linhas = self.conteudo.split("\n")[
            self.atual * self.altura : (self.atual + 1) * self.altura
        ]

        for i, linha in enumerate(linhas):
            janela.escrever(self.y + i, self.x, linha)

    def renderizar(self) -> str:
        linhas = self.conteudo.split("\n")[
                self.atual * self.altura : (self.atual + 1) * self.altura
            ]
        if len(self.efeitos) > 0:
            for i, linha in enumerate(linhas):
                linhas[i] = self.estilizar(linha)
        return "\n".join(
            linhas
        )

    def __init__(self, caminho: str, atual: int, altura: int, efeitos: list[Efeito] = []) -> None:
        self.caminho = caminho

        self.conteudo = ler_arquivo(caminho)
        self.altura = altura
        self.atual = atual % int(len(self.conteudo.split("\n")) / self.altura)
        super().__init__(efeitos=efeitos)


class Ascii(Elemento):
    caminho: str
    conteudo: str

    @property
    def altura_dinamica(self) -> int:
        return len(self.conteudo.split("\n"))

    def escrever(self, janela: Cursor) -> None:
        linhas = self.conteudo.split("\n")

        for i, linha in enumerate(linhas):
            janela.escrever(self.y + i, self.x, linha)

    @property
    def tamanho(self) -> int:
        return max(map(lambda x: lenEstilizado(x), self.conteudo.split("\n")))

    def renderizar(self) -> str:
        linhas = self.conteudo.split("\n")
        if len(self.efeitos) > 0:
            for i, linha in enumerate(linhas):
                linhas[i] = self.estilizar(linha)
        return '\n'.join(linhas)

    def __init__(self, caminho: str, efeitos: list[Efeito] = []) -> None:
        self.caminho = caminho
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            self.conteudo = arquivo.read()
        super().__init__(efeitos=efeitos)


class Tabela(Container):

    colunas: int
    divisoes: Optional[list[float]] = None
    largura_parcial: list[int]

    def definir_largura_filhos(self, largura_disponivel: list[int]):
        coluna = 0
        for filho in self.filhos:
            filho.largura_disponivel = largura_disponivel[coluna]
            if coluna == (self.colunas - 1):
                coluna = 0
            else:
                coluna += 1

    def escrever(self, janela: Cursor) -> None:
        self.largura_parcial = list(
            map(lambda x: int(self.largura_disponivel * x), self.divisoes)
            if self.divisoes
            else map(
                lambda x: (
                    self.largura_disponivel
                    if self.colunas == 1
                    else math.floor(
                        (self.largura_disponivel - self.colunas + 1) / self.colunas
                    )
                ),
                range(self.colunas),
            )
        )
        self.definir_largura_filhos(self.largura_parcial)
        #resultado: list[list[str]] = []

        coluna = 0
        max = 0
        maxAtual = 1
        for filho in self.filhos:
            c = filho.altura_dinamica
            
            # r = max + c
            filho.y = self.y + max + 1
            filho.x = self.x + (sum(self.largura_parcial[:coluna])) + (coluna + 1)
            filho.escrever(janela)
            
            if c > maxAtual:
                maxAtual = c
            
            # linhas = filho.renderizar().split("\n")
            # for c, linha in enumerate(linhas):
            #     r = max + c

            #     # while r >= len(resultado):
            #     #     resultado.append(list(map(lambda x: "", range(self.colunas))))
            #     if c > maxAtual:
            #         maxAtual = c
            #     filho.y = self.y + r
            #     filho.x = self.x + (coluna * self.largura_parcial[coluna]) + (coluna + 1)
            #     filho.escrever(janela)
            #     #resultado[r][coluna] = filho.estilizar(linha)
            if coluna == (self.colunas - 1):
                coluna = 0
                max += maxAtual + 1
                maxAtual = 1
            else:
                coluna += 1

        # for i, linha in enumerate(resultado):
        #     for j, coluna in enumerate(linha):
        #         if len(coluna) == 0:
        #             resultado[i][j] = " " * self.largura_parcial[j % self.colunas]

    @property
    def tamanho(self) -> int:
        return self.largura_disponivel

    def renderizar(self) -> str:
        self.largura_parcial = list(
            map(lambda x: int(self.largura_disponivel * x), self.divisoes)
            if self.divisoes
            else map(
                lambda x: (
                    self.largura_disponivel
                    if self.colunas == 1
                    else math.floor(
                        (self.largura_disponivel - self.colunas + 1) / self.colunas
                    )
                ),
                range(self.colunas),
            )
        )
        self.definir_largura_filhos(self.largura_parcial)
        resultado: list[list[str]] = []

        coluna = 0
        max = 0
        maxAtual = 1
        for filho in self.filhos:
            linhas = filho.renderizar().split("\n")
            for c, linha in enumerate(linhas):
                r = max + c

                while r >= len(resultado):
                    resultado.append(list(map(lambda x: "", range(self.colunas))))
                if c > maxAtual:
                    maxAtual = c
                resultado[r][coluna] = filho.estilizar(linha)
            if coluna == (self.colunas - 1):
                coluna = 0
                max += maxAtual + 1
                maxAtual = 1
            else:
                coluna += 1

        for i, linha in enumerate(resultado):
            for j, coluna in enumerate(linha):
                if len(coluna) == 0 or not coluna:
                    resultado[i][j] = " " * (self.largura_parcial[j % self.colunas])
        return (
            "\n".join(map(("|" if self.mostrar_divisoes else " ").join, resultado))
            + "\n"
        )

    def __init__(
        self,
        colunas: int,
        filhos: list[Elemento],
        divisoes: Optional[list[float]] = None,
        mostrar_divisoes=True,
    ) -> None:
        self.colunas = colunas
        self.divisoes = divisoes
        self.mostrar_divisoes = mostrar_divisoes
        super().__init__(filhos)
        self.largura_parcial = list(
            map(lambda x: int(self.largura_disponivel * x), divisoes)
            if divisoes
            else map(
                lambda x: (
                    self.largura_disponivel
                    if colunas == 1
                    else math.floor((self.largura_disponivel - colunas + 1) / colunas)
                ),
                range(colunas),
            )
        )
        self.definir_largura_filhos(self.largura_parcial)


class Preencher(Elemento):
    conteudo: str


    def __init__(self, conteudo: str, efeitos: list[Efeito] | None = None) -> None:
        super().__init__(efeitos)
        self.conteudo = conteudo

    def renderizar(self) -> str:
        return self.conteudo * self.largura_disponivel


# class Area(Container):


class Borda(ContainerUnico):

    borda_vertical: str
    borda_horizontal: str
    
    @property
    def altura_dinamica(self) -> int:
        return self.altura_disponivel

    def escrever(self, janela: Cursor) -> None:
        # print("escrevendo")
        largura_disponivel = self.largura_disponivel - (len(self.borda_vertical) * 2)
        janela.escrever(self.y, self.x, self.borda_horizontal * self.largura_disponivel)
        for y in range(1, self.altura_disponivel + 1):
            pass
            # print(self.y + y, self.x, self.borda_vertical)
            janela.escrever(self.y + y, self.x, self.borda_vertical)
            janela.escrever(
                self.y + y, self.x + self.largura_disponivel , self.borda_vertical
            )
        janela.escrever(
            self.y + self.altura_disponivel,
            self.x + 1,
            self.borda_horizontal * largura_disponivel,
        )
        self.filho.x = self.x + 1
        self.filho.y = self.y + 1
        self.filho.escrever(janela)

    def __init__(
        self,
        borda_vertical: str,
        borda_horizontal: str,
        filhos: Elemento,
        largura: int | None = None,
        altura: Optional[int] = None,
    ) -> None:
        super().__init__(
            filhos, largura - (len(borda_vertical) * 2) if largura else largura
        )
        self.largura_disponivel = self.largura_disponivel - (len(borda_vertical) * 2)
        self.altura_disponivel -= 2
        self.filho.largura_disponivel = self.largura_disponivel
        self.filho.altura_disponivel = self.altura_disponivel
        # self.definir_largura(self.largura_disponivel)
        self.borda_horizontal = borda_horizontal
        self.borda_vertical = borda_vertical
        if altura:
            self.altura_disponivel = altura

    def renderizar(self) -> str:
        self.largura_disponivel = self.largura_disponivel - (
            len(self.borda_vertical) * 2
        )
        self.filho.largura_disponivel = self.largura_disponivel
        self.filho.altura_disponivel = self.altura_disponivel
        # self.definir_largura(self.largura_disponivel)
        linhas = [self.borda_horizontal * self.largura_disponivel]
        conteudo = self.filho.renderizar().split("\n")
        linhas.extend(
            map(lambda x: self.borda_vertical + x + self.borda_vertical, conteudo)
        )
        linhas.extend(
            map(
                lambda x: self.borda_vertical
                + (" " * (self.largura_disponivel - 1))
                + self.borda_vertical,
                range(self.altura_disponivel - len(conteudo)),
            )
        )
        linhas.append(
            self.borda_vertical
            + self.borda_horizontal * (self.largura_disponivel - 1)
            + self.borda_vertical
        )
        return "\n".join(linhas)


class Scroll(ContainerUnico):
    atual: int

    def escrever(self, janela: Cursor) -> None:
        return super().escrever(janela)

    def __init__(
        self, atual: int, filhos: Elemento, largura: int | None = None
    ) -> None:
        super().__init__(filhos, largura)
        self.atual = atual

    def renderizar(self) -> str:
        self.filho.largura_disponivel = self.largura_disponivel
        # return ""
        linhas = self.filho.renderizar().split("\n")
        
        area = linhas[self.atual:self.atual+self.altura_disponivel]
        #return ""
        return '\n'.join(area)



class Input(Elemento):
    valor: str
    mudarValor: Callable[[str], None]
    
    def __init__(self, valor: str, mudarValor: Callable[[str], None], efeitos: list[Efeito] | None = None) -> None:
        super().__init__(efeitos)
        self.valor = valor
        self.mudarValor = mudarValor
    
    @property
    def tamanho(self) -> int:
        return len(self.valor)

    def escrever(self, janela: Cursor) -> None:
        self.obterEscrita()
        janela.escrever(self.y, self.x, self.valor )

    def obterEscrita(self):
        char = obterTecla()
        if char == "\x7f":
            # print("p", self.valor, self.valor[:-2])
            self.mudarValor(self.valor[:-1])
            
        elif char != "" and type(char) == str:
            self.mudarValor(self.valor + char)

    def renderizar(self) -> str:
        self.obterEscrita()
        return "v:" + self.valor


# janela: window


def escrever(elemento: Elemento):
    pass
    # print(CursesCursor().instancia.janela)
    # elemento.escrever(CursesCursor().instancia)
    # janela.refresh()

# def iniciar_escrita():
    
#     def obterJanela(stdscr: window):
#         global janela
#         # stdscr.addstr(3,0, "OBTENDO")
#         # stdscr.addstr(4,0, f"{get_terminal_size().lines}")
#         # stdscr.refresh()
#         janela = stdscr

#     curses.wrapper(obterJanela)
