from collections import deque
from typing import Dict
from .modelo import Vertice, Aresta

class Grafo:
    def __init__(self):
        self.vertices: Dict[int, Vertice] = {}

    def adicionar_vertice(self, vertice: Vertice) -> None:
        if vertice.id not in self.vertices:
            self.vertices[vertice.id] = vertice

    def adicionar_aresta(self, origem: int, destino: int, peso: float, nome: str = "Desconhecido", mao_unica: bool = False) -> None:
        if origem in self.vertices and destino in self.vertices:
            aresta = Aresta(origem, destino, peso, nome, mao_unica)
            self.vertices[origem].adicionar_aresta(aresta)
            
            if not mao_unica:
                aresta_inversa = Aresta(destino, origem, peso, nome, mao_unica)
                self.vertices[destino].adicionar_aresta(aresta_inversa)