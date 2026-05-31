import osmnx as ox
import os
import json
from util.config import Config

def extrair_dados_malha_viaria(locais):
    print(f"Baixando dados da malha viária para: {locais}...")
    
    G = ox.graph_from_place(locais, network_type='drive')
    
    print("Processando nós (cruzamentos) e arestas (ruas)...")
    
    nos = []
    for no_id, dados in G.nodes(data=True):
        nos.append({
            "id": no_id,
            "lat": dados['y'],
            "lon": dados['x']
        })
        
    arestas = []
    for origem, destino, dados in G.edges(data=True):
        arestas.append({
            "origem": origem,
            "destino": destino,
            "distancia": round(dados.get('length', 0.0), 2),
            "mao_unica": dados.get('oneway', False),
            "nome": dados.get('name', 'Desconhecido')
        })
        
    os.makedirs('data', exist_ok=True)

    with open(Config.CAMINHO_NOS, 'w', encoding='utf-8') as f:
        json.dump(nos, f, ensure_ascii=False, indent=4)
        
    with open(Config.CAMINHO_ARESTAS, 'w', encoding='utf-8') as f:
        json.dump(arestas, f, ensure_ascii=False, indent=4)
        
    print(f"Extração concluída! {len(nos)} nós e {len(arestas)} arestas salvos.")