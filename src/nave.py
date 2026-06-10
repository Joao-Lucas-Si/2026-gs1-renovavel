from typing import Optional

from src.partes import Bateria, Gerador, Parte, Propulsor, bateria_avancada, bateria_basica, bateria_media,  bateria_velha, propulsor_basico, propulsor_hiper, propulsor_luz
from utils.arquivos import ler_arquivo


class Nave:
    propulsor: Propulsor = propulsor_basico
    gerador: Optional[Gerador]
    bateria: Bateria = bateria_basica
    
    @property
    def partes(self) -> list[Parte]:
        partes = [
            self.propulsor,
           
            self.bateria
        ]
        if  self.gerador:
            partes.append(self.gerador)
            
        return partes

    def __init__(
        self,
        propulsor: Propulsor = propulsor_basico,
        bateria: Bateria = bateria_basica,
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
        case bateria_media.nome:
            bateria = ler_arquivo("recursos/ascii/naves/bateria/medio.txt")
        case bateria_basica.nome | bateria_velha.nome:
            bateria = ler_arquivo("recursos/ascii/naves/bateria/simples.txt")

    return fogute_base + "\n" + bateria + "\n" + propulsor