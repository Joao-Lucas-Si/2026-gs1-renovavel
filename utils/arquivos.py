from abc import ABC, abstractmethod
import json
from pathlib import Path


def ler_arquivo(caminho: str):
    with open(caminho, 'r', encoding="utf-8") as arquivo:
        return arquivo.read()
    
def ler_json(caminho: str):
    puro = ler_arquivo(caminho)
    
    return json.loads(puro)

def escrever_arquivo(caminho: str, data: str):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        arquivo.write(data)

def arquivo_existe(caminho: str):
    arquivo = Path(caminho)
    return arquivo.exists()
    
def escrever_json(caminho: str, data: dict):
    escrever_arquivo(caminho, json.dumps(data))
    
class Database(ABC):
    @property
    @abstractmethod
    def caminho(self) -> str:
        pass
    
    @property
    @abstractmethod
    def json(self) -> dict:
        pass
    
    def salvar(self): 
        escrever_json(self.caminho, self.json)
    
    def iniciar(self):
        if arquivo_existe(self.caminho):
            json = ler_json(self.caminho)
            self.instanciar(json)
        else:
            self.padrao()
    
    @abstractmethod
    def padrao(self) -> None:
        pass
    @abstractmethod
    def instanciar(self, json: dict) -> None:
        pass