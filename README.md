# Análise de Resiliência de Malha Viária Urbana

## Visão Geral

Este projeto implementa uma solução computacional baseada em **Teoria dos Grafos** para análise estrutural e resiliência de malhas viárias urbanas. Utilizando dados geoespaciais extraídos do OpenStreetMap (OSM), o sistema modela cruzamentos como vértices e vias como arestas ponderadas, aplicando algoritmos clássicos para identificar gargalos de tráfego, medir conectividade e simular cenários de interdição crítica.

**Tema do Projeto:** Infraestrutura Viária Urbana  
**Domínio:** Malha viária e Rotas  

---

## Arquitetura e Decisões de Design

O projeto segue o padrão **arquitetural em camadas (Layered Architecture)**, garantindo separação de responsabilidades e facilitando manutenção e extensibilidade:

### Estrutura de Camadas

```
┌─────────────────────────────────────┐
│   VIEW (Apresentação)               │  ← CLI e Visualizador Geoespacial
├─────────────────────────────────────┤
│   SERVICE (Lógica de Negócio)       │  ← Algoritmos e Análises
├─────────────────────────────────────┤
│   MODEL (Domínio)                   │  ← Estruturas de Dados (Grafo, Vértice, Aresta)
├─────────────────────────────────────┤
│   INFRA (Persistência)              │  ← Carregamento e Serialização de Dados
├─────────────────────────────────────┤
│   UTIL (Configuração)               │  ← Gerenciamento de Caminhos e Constantes
└─────────────────────────────────────┘
```

### Decisões Arquiteturais Principais

1. **Separação de Camadas Nítidas**
   - **Model**: Define `Grafo`, `Vertice` e `Aresta` com suporte a grafos ponderados e não-direcionados
   - **Service**: Encapsula algoritmos (`BFS`, `DFS`, `Dijkstra`) e análises de negócio
   - **Infra**: Responsável exclusivamente por I/O (carregamento de JSON do OSM)
   - **View**: Apresentação em CLI e mapa HTML interativo
   - **Util**: Centraliza configurações de caminhos e variáveis de ambiente

2. **Modelagem do Grafo**
   - Vértices representam cruzamentos urbanos com coordenadas geoespaciais (latitude/longitude)
   - Arestas ponderadas representam vias com distância em metros
   - Suporte a arestas bidirecionais por padrão (tráfego compartilhado)
   - Armazenamento de metadata: nome das vias, tipo de via

3. **Algoritmos Utilizados**
   - **BFS (Busca em Largura)**: Análise de conectividade global
   - **DFS (Busca em Profundidade)**: Delimitação de zonas de cobertura
   - **Dijkstra**: Caminhos mínimos e simulação de resiliência sob interdição
   - **Cálculo de Graus**: Identificação de centralidade e gargalos

4. **Persistência de Dados**
   - JSON como formato de serialização (importado do OSM via OSMnx)
   - Cache de computações em `cache/` para otimização em re-execuções
   - Configuração centralizada em `config.py` (paths, variáveis globais)

5. **Tratamento de Dados Geoespaciais**
   - Conversão de coordenadas OSM para IDs internos
   - Filtros por bairros para recortes urbanos específicos
   - Preservação de referências geoespaciais para visualização

---

## Como Executar

### Pré-requisitos

- **Python 3.9+**
- **pip** (gerenciador de pacotes)
- Conexão com internet (para download de dependências)

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- `osmnx` (≥1.8.0) - Extração de dados geoespaciais do OpenStreetMap
- `folium` (≥0.14.0) - Geração de mapas interativos HTML
- `networkx` (≥3.0) - Estruturas auxiliares de grafos

### Executar o Projeto

#### Opção 1: Via Terminal (Recomendado - Pós-Clone do GitHub)

Após clonar o repositório e navegar até a pasta do projeto:

```bash
# 1. Instalar dependências (primeira vez apenas)
pip install -r requirements.txt

# 2. Executar o programa
python src/main.py
```

O programa irá:
- Carregar dados geoespaciais da malha viária
- Executar 4 análises estruturais
- Exibir relatório completo no terminal
- Gerar mapa interativo em `visualizacao_analitica.html`

#### Opção 2: Via VS Code

- Abra a pasta do projeto no VS Code
- Navegue até `src/main.py`
- Pressione `Ctrl+F5` (ou clique em "Run Python File" no canto superior direito)
- Acompanhe a saída no terminal integrado

### Saída do Programa

O programa executa sequencialmente e gera:

1. **Console (CLI)**
   - Relatório de conectividade global da malha
   - Ranking dos 5 principais gargalos de tráfego
   - Análise de resiliência sob bloqueio simulado
   - Varredura de cobertura zonal

2. **Visualização (Mapa HTML)**
   - Arquivo `visualizacao_analitica.html` gerado automaticamente
   - Mapa interativo com marcação dos cruzamentos analisados
   - Visualização de rotas original, alternativa e pontos críticos

---

## Análises Realizadas e Sua Utilidade

### 1. **Análise de Conectividade Global da Malha** 
**Algoritmo:** BFS (Busca em Largura)

**Objetivo:**  
Determinar se a malha de tráfego é totalmente conexa partindo de uma interseção base, identificando se existem sub-redes ou cruzamentos isolados.

**Utilidade:**
- Identifica fragmentação na malha urbana
- Detecta zonas de difícil acesso ou desconectadas
- Auxilia planejamento de novas conexões viárias
- **Métrica:** Percentual de alcance (`cruzamentos_alcancados / total_cruzamentos`)

**Exemplo de Aplicação:**
> Se apenas 85% dos cruzamentos são alcançáveis, indica isolamento de bairros periféricos que requerem investimento em infraestrutura.

---

### 2. **Identificação de Pontos Críticos de Tráfego (Gargalos)**
**Algoritmo:** Cálculo de Graus (Centralidade)

**Objetivo:**  
Avaliar as interseções urbanas com o maior número de conexões estruturais (grau de entrada + grau de saída) para apontar potenciais gargalos de retenção veicular.

**Utilidade:**
- Prioriza investimentos em ampliação de vias
- Identifica cruzamentos que requerem sinalização melhorada
- Detecta hotspots para congestionamento
- Auxilia planos de otimização de tráfego
- **Métrica:** Ranking dos 5 cruzamentos com maior grau

**Exemplo de Aplicação:**
> Um cruzamento com 8 vias conectadas é candidato a receber semáforos inteligentes ou ampliação estrutural prioritariamente.

---

### 3. **Resiliência de Rotas sob Interdição Crítica**
**Algoritmo:** Dijkstra (Caminhos Mínimos)

**Objetivo:**  
Calcular o caminho mínimo estável entre dois pontos, simular um evento de bloqueio no cruzamento central desse trajeto (isolando-o junto com seus vizinhos) e recalcular uma nova rota para mensurar o impacto em metros causado pelo desvio.

**Utilidade:**
- Avalia robustez da malha a acidentes ou interdições
- Mensura custo de rerotas em cenários de crise
- Auxilia planejamento de rotas alternativas
- Identifica pontos de falha única ("single point of failure")
- **Métricas:** Incremento de distância (metros), colapso de fluxo (sim/não)

**Exemplo de Aplicação:**
> Se um bloqueio em um cruzamento central causa colapso de fluxo (impossibilidade de rota alternativa), esse é um ponto crítico que requer redundância.

---

### 4. **Varredura de Alcance Perimetral em Profundidade**
**Algoritmo:** DFS (Busca em Profundidade)

**Objetivo:**  
Varrer em profundidade a malha a partir de uma interseção de origem para delimitar o perímetro de cobertura contíguo.

**Utilidade:**
- Define zonas de evacuação urbana
- Modela cobertura de patrulha de segurança (raio de ação)
- Determina áreas sob influência de infraestruturas (hospitais, bombeiros)
- Auxilia planejamento de redes de distribuição (água, gás, internet)
- **Métrica:** Cobertura zonal em percentual da cidade

**Exemplo de Aplicação:**
> Uma viatura de emergência no cruzamento X consegue chegar a 60% da malha urbana em um raio efetivo, indicando necessidade de múltiplas bases de atendimento.

---

## Estrutura de Diretórios

```
Trabalho Final v2/
├── README.md                          ← Este arquivo
├── src/
│   ├── main.py                        ← Ponto de entrada (orquestração)
│   ├── model/
│   │   ├── grafo.py                   ← Classe Grafo (estrutura principal)
│   │   └── modelo.py                  ← Classes Vértice e Aresta
│   ├── service/
│   │   ├── algoritmos.py              ← BFS, DFS, Dijkstra, Métricas
│   │   └── analises.py                ← GerenciadorAnalises (4 análises)
│   ├── infra/
│   │   ├── extrator_osm.py            ← Extração de dados do OpenStreetMap
│   │   └── repositorio.py             ← Carregamento de JSON
│   ├── view/
│   │   ├── cli.py                     ← Apresentação em terminal
│   │   └── visualizador.py            ← Geração de mapa HTML interativo
│   └── util/
│       └── config.py                  ← Configuração de paths
├── data/
│   ├── nos.json                       ← Vértices extraídos do OSM
│   └── arestas.json                   ← Arestas extraídas do OSM
├── cache/
│   └── *.json                         ← Cache de computações
└── visualizacao_analitica.html        ← Mapa interativo (gerado)
```

---

## Características Técnicas do Grafo

- **Vértices:** 150+ cruzamentos urbanos
- **Arestas:** 300+ vias conectadas
- **Ponderação:** Distâncias em metros (pesos nas arestas)
- **Tipo:** Não-direcionado (tráfego bidirecional por padrão)
- **Cobertura Geográfica:** Bairros de Fortaleza-CE (Edson Queiroz, Guararapes, Cocó)
- **Fonte de Dados:** OpenStreetMap via OSMnx
- **Propriedades Estruturais:** Múltiplos componentes, ciclos, alta densidade

---

## Requisitos Atendidos

✅ **Modelagem correta** usando grafo com ponderação e direcionamento  
✅ **Mínimo 100 vértices e 100 arestas**  
✅ **Algoritmos clássicos:** BFS, DFS, Dijkstra  
✅ **4 análises estruturais** com interpretações práticas  
✅ **Código bem organizado** em camadas com responsabilidades claras  
✅ **Visualização interativa** (mapa HTML com Folium)  
✅ **CLI clara** com saída formatada de resultados  

---

## Notas de Desenvolvimento

- O projeto utiliza **caching** para evitar reprocessamento de dados pesados
- A extração de dados do OSM é otimizada com filtros geográficos
- Algoritmos implementados com complexidade O(V+E) onde aplicável
- Tratamento robusto de grafos desconexos e cenários de falha

---

## Autor - Danilo Ribeiro

Projeto Final - Disciplina de Teoria dos Grafos  