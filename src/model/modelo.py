from typing import List

class Aresta:
    def __init__(self, origem: int, destino: int, peso: float, nome: str = "Desconhecido", mao_unica: bool = False):
        self.origem = origem
        self.destino = destino
        self.peso = peso
        self.nome = nome
        self.mao_unica = mao_unica

class Vertice:
    def __init__(self, id_vertice: int, lat: float, lon: float):
        self.id = id_vertice
        self.lat = lat
        self.lon = lon
        self.arestas: List['Aresta'] = []

    def adicionar_aresta(self, aresta: 'Aresta') -> None:
        self.arestas.append(aresta)