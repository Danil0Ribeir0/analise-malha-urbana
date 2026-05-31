import heapq
from collections import deque
from typing import List, Tuple, Set, Optional

class BFS:    
    @staticmethod
    def bfs(grafo) -> Tuple[bool, int, int]:
        if not getattr(grafo, 'vertices', None):
            return False, 0, 0
            
        origem = list(grafo.vertices.keys())[0]
        
        visitados = {origem}
        fila = deque([origem])
        
        while fila:
            u = fila.popleft()
            for aresta in grafo.vertices[u].arestas:
                v = aresta.destino
                if v not in visitados:
                    visitados.add(v)
                    fila.append(v)
                    
        total_vertices = len(grafo.vertices)
        total_alcancado = len(visitados)
        
        is_conexo = (total_alcancado == total_vertices)
        return is_conexo, total_alcancado, total_vertices


class DFS:    
    @staticmethod
    def dfs(grafo, origem: int) -> Set[int]:
        visitados = set()
        
        def dfs_recursiva(u):
            visitados.add(u)
            for aresta in grafo.vertices[u].arestas:
                if aresta.destino not in visitados:
                    dfs_recursiva(aresta.destino)
                    
        dfs_recursiva(origem)
        return visitados


class Dijkstra:    
    def __init__(self, grafo):
        self.grafo = grafo

    def dijkstra(self, id_origem: int, id_destino: int, nos_ignorados: Optional[Set[int]] = None) -> Tuple[List[int], float]:
        if nos_ignorados is None:
            nos_ignorados = set()
            
        distancias = {v: float('inf') for v in self.grafo.vertices}
        distancias[id_origem] = 0
        
        pq = [(0, id_origem)]
        predecessores = {v: None for v in self.grafo.vertices}
        visitados = set()
        
        while pq:
            dist_atual, u = heapq.heappop(pq)
            
            if u == id_destino:
                break
                
            if u in visitados:
                continue
                
            visitados.add(u)
            
            for aresta in self.grafo.vertices[u].arestas:
                v = aresta.destino
                
                if v in nos_ignorados or v in visitados:
                    continue
                    
                nova_dist = dist_atual + aresta.peso
                
                if nova_dist < distancias[v]:
                    distancias[v] = nova_dist
                    predecessores[v] = u
                    heapq.heappush(pq, (nova_dist, v))
                    
        if distancias[id_destino] == float('inf'):
            return [], float('inf')
            
        caminho = []
        atual = id_destino
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
            
        return caminho[::-1], distancias[id_destino]


class MetricasGrafo:    
    @staticmethod
    def calcular_graus(grafo, top_n: int = 5) -> List[Tuple[int, int]]:
        graus = {v_id: 0 for v_id in grafo.vertices}
        
        for v_id, vertice in grafo.vertices.items():
            graus[v_id] += len(vertice.arestas)
            
            for aresta in vertice.arestas:
                if aresta.destino in graus:
                    graus[aresta.destino] += 1
                    
        top_vertices = sorted(graus.items(), key=lambda item: item[1], reverse=True)
        return top_vertices[:top_n]