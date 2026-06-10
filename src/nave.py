from typing import Optional

from src.partes import Bateria, Gerador, Propulsor, bateria_avancada, bateria_basica, bateria_media, bateria_reserva, bateria_velha, propulsor_basico, propulsor_hiper, propulsor_luz
from utils.arquivos import ler_arquivo


class Nave:
    propulsor: Propulsor = propulsor_hiper
    gerador: Optional[Gerador]
    bateria: Bateria = bateria_basica
    
    @property
    def partes(self):
        return [
            self.propulsor,
            self.gerador,
            self.bateria
        ]

    def __init__(
        self,
        propulsor: Propulsor = propulsor_hiper,
        bateria: Bateria = bateria_avancada,
        gerador: Optional[Gerador] = None,
    ) -> None:
        self.propulsor = propulsor
        self.bateria = bateria
        self.gerador = gerador


def printarNave(nave: Nave):
    fogute_base = ler_arquivo("recursos/ascii/naves/foguete_grande.txt")

    propulsor: str = ""

    match (nave.propulsor.nome):
        case propulsor_hiper.nome:
            propulsor = ler_arquivo("recursos/ascii/naves/propulsores/avancado.txt")
        case propulsor_basico.nome:
            propulsor = ler_arquivo("recursos/ascii/naves/propulsores/basico.txt")
        case propulsor_luz.nome:
            propulsor = ler_arquivo("recursos/ascii/naves/propulsores/medio.txt")
    bateria = ""
    match (nave.bateria.nome):
        case bateria_avancada.nome:
            bateria = ler_arquivo("recursos/ascii/naves/bateria/avancado.txt")
        case bateria_reserva.nome | bateria_media.nome:
            bateria = ler_arquivo("recursos/ascii/naves/bateria/simples.txt")
        case bateria_basica.nome | bateria_velha.nome:
            bateria = ler_arquivo("recursos/ascii/naves/bateria/medio.txt")

    return fogute_base + "\n" + bateria + "\n" + propulsor