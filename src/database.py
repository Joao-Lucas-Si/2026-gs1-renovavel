# class Parametro():
#     valor: int


from enum import Enum
import random
from typing import Optional, Tuple, Type

from src.nave import Nave
from src.partes import Parte
from src.custos import Caracteristica


class Tendencia:
    intervalo: Tuple[int, int]
    duracao: int
    nome: str
    atividade = 0

    def __init__(self, nome: str, intervalo: Tuple[int, int], duracao: int) -> None:
        self.nome = nome
        self.intervalo = intervalo
        self.duracao = duracao

    def novo(self, duracao: int):
        instancia = Tendencia(self.nome, self.intervalo, duracao)
        instancia.atividade = 0
        return instancia

    def aplicar(self):
        return random.randint(self.intervalo[0], self.intervalo[1])


class Tendencias(Enum):
    CRITICO = Tendencia("critico", (20, 30), 2)
    ATENCAO = Tendencia("atencao", (10, 20), 2)
    ESTAVEL = Tendencia("estavel", (5, 10), 2)


class TendenciaParametro:
    caracteristica: Caracteristica
    tendencia: Tendencia

    def __init__(self, caracteristica: Caracteristica, tendencia: Tendencia) -> None:
        self.caracteristica = caracteristica
        self.tendencia = tendencia


class Database:
    energia = 10000
    temperatura = 40
    oxigenio = 100
    poluicao = 0
    modulo = 100
    comunicacao = 100
    tendencias: list[TendenciaParametro] = [
        TendenciaParametro(
            Caracteristica.TEMPERATURA, Tendencias.ESTAVEL.value.novo(1)
        ),
        TendenciaParametro(
            Caracteristica.COMUNICACAO, Tendencias.ESTAVEL.value.novo(1)
        ),
        TendenciaParametro(Caracteristica.MODULO, Tendencias.ESTAVEL.value.novo(1)),
        TendenciaParametro(Caracteristica.OXIGENIO, Tendencias.ESTAVEL.value.novo(1)),
    ]
    custo_temperatura = 20
    custo_oxigenio = 20
    custo_modulo = 20
    custo_comunicacao = 20

    tempo = random.randint(12, 20)
    atual = 1
    nave: Nave = Nave()

    @property
    def orcamento(self):
        return self.tempo * 500

    def gastos(self, excluir: Optional[Type] = None):
        return sum(
            map(
                lambda x: x.preco,
                [
                    parte
                    for parte in self.nave.partes
                    if (excluir and not isinstance(parte, excluir)) or not excluir
                ],
            )
        )

    @staticmethod
    def instancia():
        return db


a = Database
db = Database()
