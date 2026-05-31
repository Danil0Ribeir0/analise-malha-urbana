from typing import Dict, List, Tuple, Set, Any, Optional
from .algoritmos import BFS, DFS, Dijkstra, MetricasGrafo

class GerenciadorAnalises:
    def __init__(self, grafo):
        self.grafo = grafo
        self.dijkstra = Dijkstra(grafo)

    def analisar_conectividade(self) -> Dict[str, Any]:
        """
        ANÁLISE 1: Conectividade Global da Malha Viária (Usa BFS).
        Determina se a malha de tráfego é totalmente conexa partindo de uma 
        interseção base, identificando se existem sub-redes ou cruzamentos isolados.
        """
        is_conexo, alcancados, total = BFS.bfs(self.grafo)
        percentual = (alcancados / total * 100) if total > 0 else 0.0
        
        return {
            "analise": "Conectividade Global da Malha",
            "algoritmo": "Busca em Largura (BFS)",
            "is_conexo": is_conexo,
            "cruzamentos_alcancados": alcancados,
            "total_cruzamentos": total,
            "percentual_alcance": round(percentual, 2)
        }

    def analisar_gargalos(self, top_n: int = 5) -> Dict[str, Any]:
        """
        ANÁLISE 2: Identificação de Pontos Críticos de Tráfego (Usa Cálculo de Graus).
        Avalia as interseções urbanas com o maior número de conexões estruturais 
        (grau de entrada + grau de saída) para apontar potenciais gargalos de retenção veicular.
        """
        top_cruzamentos = MetricasGrafo.calcular_graus(self.grafo, top_n=top_n)
        
        gargalos_formatados = [
            {"id_cruzamento": id_v, "vias_conectadas": grau} 
            for id_v, grau in top_cruzamentos
        ]
        
        return {
            "analise": f"Top {top_n} Pontos de Gargalo",
            "algoritmo": "Métricas de Centralidade de Grau",
            "top_n": top_n,
            "gargalos": gargalos_formatados
        }

    def analisar_resiliencia(self, id_origem: int, id_destino: int) -> Dict[str, Any]:
        """
        ANÁLISE 3: Resiliência de Rotas sob Interdição Crítica (Usa Dijkstra).
        Calcula o caminho mínimo estável entre dois pontos, simula um evento de bloqueio 
        no cruzamento central desse trajeto (isolando-o junto com seus vizinhos) e recalcula 
        uma nova rota para mensurar o impacto em metros causado pelo desvio.
        """
        caminho_original, dist_original = self.dijkstra.dijkstra(id_origem, id_destino)
        
        if not caminho_original or dist_original == float('inf'):
            return {
                "analise": "Resiliência sob Interdição",
                "algoritmo": "Algoritmo de Dijkstra",
                "sucesso": False,
                "erro": "Não foi possível estabelecer uma rota base entre os cruzamentos informados."
            }
            
        meio = len(caminho_original) // 2
        no_critico = caminho_original[meio]
        
        area_bloqueada = {no_critico}
        if no_critico in self.grafo.vertices:
            for aresta in self.grafo.vertices[no_critico].arestas:
                area_bloqueada.add(aresta.destino)
            
        caminho_novo, dist_nova = self.dijkstra.dijkstra(id_origem, id_destino, nos_ignorados=area_bloqueada)
        colapso_fluxo = (not caminho_novo or dist_nova == float('inf'))
        
        return {
            "analise": "Resiliência sob Interdição",
            "algoritmo": "Algoritmo de Dijkstra",
            "sucesso": True,
            "rota_original": {
                "caminho": caminho_original,
                "distancia_metros": round(dist_original, 2),
                "total_cruzamentos": len(caminho_original)
            },
            "simulacao_bloqueio": {
                "no_central_bloqueado": no_critico,
                "total_cruzamentos_afetados": len(area_bloqueada),
                "lista_bloqueados": list(area_bloqueada)
            },
            "rota_alternativa": {
                "colapso_de_fluxo": colapso_fluxo,
                "caminho": caminho_novo if not colapso_fluxo else [],
                "distancia_metros": round(dist_nova, 2) if not colapso_fluxo else float('inf'),
                "acrescimo_metros": round(dist_nova - dist_original, 2) if not colapso_fluxo else 0.0
            }
        }

    def analisar_cobertura_zona(self, id_origem: int) -> Dict[str, Any]:
        """
        ANÁLISE 4: Varredura de Alcance Perimetral em Profundidade (Usa DFS).
        Varre em profundidade a malha a partir de uma interseção de origem para delimitar 
        o perímetro de cobertura contíguo. Útil para modelar zonas de evacuação, cobertura 
        de rádio-patrulha ou delimitação de áreas sob influência de infraestruturas locais.
        """
        if id_origem not in self.grafo.vertices:
            return {
                "analise": "Varredura de Alcance de Zona",
                "algoritmo": "Busca em Profundidade (DFS)",
                "sucesso": False,
                "erro": "O cruzamento de origem fornecido não foi encontrado no grafo viário."
            }
            
        cruzamentos_alcancados = DFS.dfs(self.grafo, id_origem)
        total_sistema = len(self.grafo.vertices)
        percentual_cobertura = (len(cruzamentos_alcancados) / total_sistema * 100) if total_sistema > 0 else 0.0
        
        return {
            "analise": "Varredura de Alcance de Zona",
            "algoritmo": "Busca em Profundidade (DFS)",
            "sucesso": True,
            "id_origem": id_origem,
            "total_zona_alcancada": len(cruzamentos_alcancados),
            "lista_cruzamentos_zona": list(cruzamentos_alcancados),
            "cobertura_da_cidade_percentual": round(percentual_cobertura, 2)
        }