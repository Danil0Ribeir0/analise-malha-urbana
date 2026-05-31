# Em: src/util/config.py
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    PASTA_DATA = BASE_DIR / 'data'
    
    CAMINHO_NOS = PASTA_DATA / 'nos.json'
    CAMINHO_ARESTAS = PASTA_DATA / 'arestas.json'

    CAMINHO_MAPA = BASE_DIR / 'visualizacao_analitica.html'