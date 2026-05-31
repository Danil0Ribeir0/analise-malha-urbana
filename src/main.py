from util.config import Config
from infra.repositorio import RepositorioJSON
from service.analises import GerenciadorAnalises
from view.cli import CLI
from view.visualizador import VisualizadorMapa

def main():
    CLI.exibir_cabecalho()
    
    bairros = [
        "Edson Queiroz, Fortaleza, Ceará, Brasil",
        "Guararapes, Fortaleza, Ceará, Brasil",
        "Cocó, Fortaleza, Ceará, Brasil"
    ]
    
    # 1. INFRAESTRUTURA: Processamento de dados de entrada
    print("A carregar base de dados da infraestrutura viária...")
    grafo = RepositorioJSON.carregar_grafo(
        str(Config.CAMINHO_NOS), 
        str(Config.CAMINHO_ARESTAS), 
        bairros
    )
    
    # 2. SERVIÇOS: Inicialização do motor lógico de regras de negócio
    analisador = GerenciadorAnalises(grafo)
    
    # 3. APRESENTAÇÃO CLI: Execução de análises estruturais e logs de console
    dados_conectividade = analisador.analisar_conectividade()
    CLI.exibir_resultado_conectividade(dados_conectividade)
    
    dados_gargalos = analisador.analisar_gargalos(top_n=5)
    CLI.exibir_resultado_gargalos(dados_gargalos)
    
    dados_resiliencia = None
    if grafo.vertices:
        pontos_validos = list(grafo.vertices.keys())
        origem_teste = pontos_validos[0]
        destino_teste = pontos_validos[-1]
        
        # Armazena o retorno para uso compartilhado (CLI e Mapa)
        dados_resiliencia = analisador.analisar_resiliencia(origem_teste, destino_teste)
        CLI.exibir_resultado_resiliencia(dados_resiliencia)
        
        dados_cobertura = analisador.analisar_cobertura_zona(origem_teste)
        CLI.exibir_resultado_cobertura(dados_cobertura)

    # 4. APRESENTAÇÃO MAPA: Geração condicional da camada geoespacial
    print("\n--- CAMADA VISUAL VERIFICAÇÃO ---")
    if not Config.CAMINHO_MAPA.exists():
        if dados_resiliencia:
            VisualizadorMapa.gerar_mapa(grafo, dados_resiliencia, str(Config.CAMINHO_MAPA))
        else:
            print("Não foi possível gerar o mapa: dados de simulação indisponíveis.")
    else:
        print(f"O arquivo '{Config.CAMINHO_MAPA.name}' já se encontra gerado no diretório. Geração automática pulada.")

    CLI.exibir_rodape()

if __name__ == "__main__":
    main()