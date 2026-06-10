from enum import Enum
from typing import overload, override


class Efeito:
    @property
    def valor(self) -> str:
        return ""


class CorAlvo(Enum):
    TEXTO = 30
    FUNDO = 40
    TEXTO_PERSONALIZADO = 38
    FUNDO_PERSONALIZADO = 48
    TEXTO_CLARO = 90
    FUNDO_CLARO = 100


class CorEfeito(Efeito):
    alvo: CorAlvo
    cor: int

    def __init__(self, alvo: CorAlvo, cor: int) -> None:
        self.alvo = alvo
        self.cor = cor

    @property
    @override
    def valor(self):
        return (
            f"{self.alvo.value};{self.cor}"
            if self.alvo == CorAlvo.TEXTO_PERSONALIZADO
            or self.alvo == CorAlvo.FUNDO_PERSONALIZADO
            else f"{self.alvo.value + self.cor}"
        )


class Cor:
    def efeito(self, alvo: CorAlvo):
        return CorEfeito(alvo, self.valor)

    def __init__(self, valor: int) -> None:
        self.valor = valor


class Cores1B(Enum):
    VERMELHO = Cor(1)
    PRETO = Cor(0)
    VERDE = Cor(2)
    AMARELo = Cor(3)
    AZUL = Cor(4)
    ROXO = Cor(5)
    CIANO = Cor(6)
    BRANCO = Cor(7)


class CorConfig:
    primario: Cor
    secundario: Cor

    @staticmethod
    def iniciar(primario: Cor, secundario: Cor):
        corConfig.primario = primario
        corConfig.secundario = secundario


corConfig = CorConfig()


def ativarEfeitos(efeitos: list[Efeito]):
    print(aplicarEfeitos(efeitos))

def aplicarEfeitos(efeitos: list[Efeito]):
    return f"\033[{";".join(map( lambda x: x.valor, efeitos))}m"    

def desaplicarEfeitos():
    return "\033[0m"

def desativarEfeitos():
    print(desaplicarEfeitos())