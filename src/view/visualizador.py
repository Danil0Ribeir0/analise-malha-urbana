import folium
from typing import Dict, Any

class VisualizadorMapa:
    """
    Camada de Apresentação (View).
    Responsável exclusivamente por renderizar camadas geográficas no mapa 
    utilizando os dados gerados pela camada de serviços.
    """
    
    @staticmethod
    def gerar_mapa(grafo, dados_resiliencia: Dict[str, Any], caminho_saida: str) -> None:
        # Validação prévia para garantir consistência estrutural
        if not getattr(grafo, 'vertices', None) or not dados_resiliencia.get('sucesso', False):
            print("Aviso: Não foi possível gerar o mapa devido a falhas na rota base ou grafo vazio.")
            return

        print("A renderizar camadas analíticas no mapa (Folium)...")
        
        # Extração de dados puros retornados pelo serviço de análise
        rota_orig = dados_resiliencia['rota_original']['caminho']
        area_bloqueada = set(dados_resiliencia['simulacao_bloqueio']['lista_bloqueados'])
        rota_nova = dados_resiliencia['rota_alternativa']['caminho']
        colapso_de_fluxo = dados_resiliencia['rota_alternativa']['colapso_de_fluxo']
        
        id_origem = rota_orig[0]
        id_destino = rota_orig[-1]
        
        # Inicialização do mapa centrado na origem selecionada
        inicio = grafo.vertices[id_origem]
        mapa = folium.Map(location=[inicio.lat, inicio.lon], zoom_start=14, tiles="CartoDB positron")

        # Definição dos FeatureGroups (Camadas de visualização controláveis)
        fg_base = folium.FeatureGroup(name="Malha Viária Base", show=True)
        fg_bloqueio = folium.FeatureGroup(name="Área Interditada (Nó Central + Vizinhos)", show=True)
        fg_rota_original = folium.FeatureGroup(name="Rota Original", show=False) # Oculta por padrão para evitar poluição visual
        fg_rota_nova = folium.FeatureGroup(name="Rota de Desvio (Resiliência)", show=True)

        # 1. Camada Base: Desenha todas as ruas carregadas no grafo
        for id_v, vertice in grafo.vertices.items():
            coord_origem = (vertice.lat, vertice.lon)
            for aresta in vertice.arestas:
                if aresta.destino in grafo.vertices:
                    coord_destino = (grafo.vertices[aresta.destino].lat, grafo.vertices[aresta.destino].lon)
                    folium.PolyLine([coord_origem, coord_destino], color="gray", weight=1, opacity=0.3).add_to(fg_base)

        # 2. Camada Rota Original: Traçado tracejado em azul
        if rota_orig:
            coords_originais = [(grafo.vertices[no].lat, grafo.vertices[no].lon) for no in rota_orig if no in grafo.vertices]
            folium.PolyLine(coords_originais, color="blue", weight=4, opacity=0.8, dash_array="10").add_to(fg_rota_original)

        # 3. Camada Bloqueio: Marcadores circulares vermelhos simulando a zona afetada
        for no_id in area_bloqueada:
            if no_id in grafo.vertices:
                v = grafo.vertices[no_id]
                folium.CircleMarker(location=(v.lat, v.lon), radius=6, color='red', fill=True, fill_opacity=0.9).add_to(fg_bloqueio)

        # 4. Camada Rota de Desvio: Traçado contínuo em verde (apenas se houver caminho viável)
        if rota_nova and not colapso_de_fluxo:
            coords_novas = [(grafo.vertices[no].lat, grafo.vertices[no].lon) for no in rota_nova if no in grafo.vertices]
            folium.PolyLine(coords_novas, color="green", weight=5, opacity=1).add_to(fg_rota_nova)

        # Adiciona marcadores de importância operacional (Origem e Destino fixos)
        folium.Marker([inicio.lat, inicio.lon], popup="Ponto de Origem", icon=folium.Icon(color="green")).add_to(mapa)
        
        if id_destino in grafo.vertices:
            fim = grafo.vertices[id_destino]
            folium.Marker([fim.lat, fim.lon], popup="Ponto de Destino", icon=folium.Icon(color="black")).add_to(mapa)

        # Montagem hierárquica das camadas no mapa base
        fg_base.add_to(mapa)
        fg_bloqueio.add_to(mapa)
        fg_rota_original.add_to(mapa)
        fg_rota_nova.add_to(mapa)
        
        # Controle de alternância de camadas na interface visual do mapa
        folium.LayerControl().add_to(mapa)

        # Salvamento físico do arquivo de saída
        mapa.save(caminho_saida)
        print(f"Mapa interativo gerado com sucesso em: {caminho_saida}")