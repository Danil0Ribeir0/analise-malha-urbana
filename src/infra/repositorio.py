import json
import os
from typing import List, Optional
from model.grafo import Grafo
from model.modelo import Vertice
from .extrator_osm import extrair_dados_malha_viaria

class LeituraDadosError(Exception):
    """Exceção customizada lançada quando há falhas críticas na leitura ou extração de dados."""
    pass

class RepositorioJSON:
    @staticmethod
    def carregar_grafo(caminho_nos: str, caminho_arestas: str, bairros_alvo: Optional[List[str]] = None) -> Grafo:
        if not os.path.exists(caminho_nos) or not os.path.exists(caminho_arestas):
            print("Arquivos de dados não encontrados localmente.")
            print("Iniciando extracao automatica via API do OpenStreetMap...")
            
            try:
                os.makedirs(os.path.dirname(caminho_nos), exist_ok=True)
                if not bairros_alvo:
                    bairros_alvo = ["Edson Queiroz, Fortaleza, Ceará, Brasil"]
                extrair_dados_malha_viaria(bairros_alvo)
            except Exception as e:
                raise LeituraDadosError(f"Falha na comunicação com o OpenStreetMap ao tentar baixar os bairros: {e}")

        grafo = Grafo()

        try:
            with open(caminho_nos, 'r', encoding='utf-8') as f:
                nos = json.load(f)
                for no in nos:
                    vertice = Vertice(no['id'], no['lat'], no['lon'])
                    grafo.adicionar_vertice(vertice)

            with open(caminho_arestas, 'r', encoding='utf-8') as f:
                arestas = json.load(f)
                for aresta in arestas:
                    grafo.adicionar_aresta(
                        origem=aresta['origem'],
                        destino=aresta['destino'],
                        peso=aresta.get('distancia', 1.0),
                        nome=aresta.get('nome', 'Desconhecido'),
                        mao_unica=aresta.get('mao_unica', False)
                    )
            
            return grafo

        except FileNotFoundError:
            raise LeituraDadosError(f"Arquivo não pôde ser aberto mesmo após a verificação de existência.")
        except json.JSONDecodeError:
            raise LeituraDadosError("Os arquivos .json estão corrompidos ou mal formatados.")
        except KeyError as e:
            raise LeituraDadosError(f"A estrutura do JSON é inválida. Chave obrigatória ausente: {e}")
        except Exception as e:
            raise LeituraDadosError(f"Erro inesperado ao montar o grafo: {e}")