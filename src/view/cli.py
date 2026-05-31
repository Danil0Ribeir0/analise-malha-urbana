import os
from typing import Dict, Any

class CLI:
    """
    Camada de Apresentação (View).
    Responsável unicamente por formatar e exibir os dados no terminal.
    """

    @staticmethod
    def limpar_ecra():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def exibir_cabecalho():
        CLI.limpar_ecra()
        print("====================================================")
        print("  SISTEMA DE ANÁLISE DE TRÁFEGO E RESILIÊNCIA URBANA  ")
        print("====================================================")

    @staticmethod
    def exibir_resultado_conectividade(dados: Dict[str, Any]):
        print(f"\n--- ANÁLISE 1: {dados['analise'].upper()} ---")
        print(f"Motor Algorítmico: {dados['algoritmo']}")
        
        if dados['is_conexo']:
            print(f"Resultado: A malha viária é totalmente conexa!")
            print(f"Todos os {dados['total_cruzamentos']} cruzamentos cadastrados estão interligados.")
        else:
            print(f"Resultado: ATENÇÃO! A malha possui áreas isoladas estruturalmente.")
            print(f"Foram alcançados apenas {dados['cruzamentos_alcancados']} de um total de {dados['total_cruzamentos']} cruzamentos ({dados['percentual_alcance']}%).")

    @staticmethod
    def exibir_resultado_gargalos(dados: Dict[str, Any]):
        print(f"\n--- ANÁLISE 2: {dados['analise'].upper()} ---")
        print(f"Motor Algorítmico: {dados['algoritmo']}")
        
        for i, gargalo in enumerate(dados['gargalos'], 1):
            print(f"{i}º Lugar -> Cruzamento ID: {gargalo['id_cruzamento']} | Vias Conectadas: {gargalo['vias_conectadas']}")

    @staticmethod
    def exibir_resultado_resiliencia(dados: Dict[str, Any]):
        print(f"\n--- ANÁLISE 3: {dados['analise'].upper()} ---")
        print(f"Motor Algorítmico: {dados['algoritmo']}")
        
        if not dados.get('sucesso', False):
            print(f"Erro Crítico: {dados['erro']}")
            return

        rota_orig = dados['rota_original']
        print(f"1. Rota Original estável: {rota_orig['distancia_metros']} metros ({rota_orig['total_cruzamentos']} cruzamentos).")
        
        simulacao = dados['simulacao_bloqueio']
        print(f"2. Simulação: Evento crítico bloqueou o nó {simulacao['no_central_bloqueado']} e arredores ({simulacao['total_cruzamentos_afetados']} cruzamentos fechados).")
        
        rota_alt = dados['rota_alternativa']
        if rota_alt['colapso_de_fluxo']:
            print("-> Impacto: COLAPSO DE FLUXO. A zona interditada isolou a origem do destino.")
        else:
            print(f"3. Rota Alternativa traçada: {rota_alt['distancia_metros']} metros.")
            print(f"-> Impacto: O trajeto sofreu um acréscimo de {rota_alt['acrescimo_metros']} metros devido ao desvio.")

    @staticmethod
    def exibir_resultado_cobertura(dados: Dict[str, Any]):
        print(f"\n--- ANÁLISE 4: {dados['analise'].upper()} ---")
        print(f"Motor Algorítmico: {dados['algoritmo']}")
        
        if not dados.get('sucesso', False):
            print(f"Erro Crítico: {dados['erro']}")
            return
            
        print(f"1. Origem da Varredura: Cruzamento {dados['id_origem']}")
        print(f"2. Alcance Perimetral: {dados['total_zona_alcancada']} cruzamentos atingidos a partir da origem.")
        print(f"3. Cobertura da Cidade: {dados['cobertura_da_cidade_percentual']}% da infraestrutura viária abrangida pela zona.")

    @staticmethod
    def exibir_rodape():
        print("\n====================================================")
        print("          Análises concluídas com sucesso.          ")
        print("====================================================")