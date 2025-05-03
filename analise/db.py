import os
import re
import psycopg2 # type: ignore
from psycopg2 import sql # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables from the .env file
load_dotenv()

# === CONFIGURAÇÃO DO BANCO POSTGRES ===
db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

#!/usr/bin/env python3
# importar_resultados_completos.py

import os
import re
import psycopg2

# === CONFIGURAÇÃO ===
DATA_DIR = "../output"  # ajuste para onde estão os .txt

# === PADRÕES DE EXTRAÇÃO ===

VETOR_CREATION = {
    "vetor_não_ordenado": [
        r"Tempo de criação do vetor NÃO ordenado:\s*([\d.]+) s",
        r"Memória após criação do vetor NÃO ordenado:\s*([\d.]+) MB"
    ],
    "vetor_ordenado": [
        r"Tempo de criação do vetor ORDENADO:\s*([\d.]+) s",
        r"Memória após criação do vetor ORDENADO:\s*([\d.]+) MB"
    ]
}

LISTA_CREATION = {
    "lista_não_ordenada": [
        r"Tempo de criação da lista NÃO ordenada:\s*([\d.]+) s",
        r"Memória após criação da lista NÃO ordenada:\s*([\d.]+) MB"
    ],
    "lista_ordenada": [
        r"Tempo de criação da lista ORDENADA:\s*([\d.]+) s",
        r"Memória após criação da lista ORDENADA:\s*([\d.]+) MB"
    ]
}

VETOR_SEARCH_PATTERN = re.compile(
    r"Vetor (NÃO ordenado|ORDENADO) \((\d+) (EXISTENTES|INEXISTENTES)\)\s*"
    r"\[([^\]]+)\]\s*"
    r"Tempo médio:\s*([\d.]+)s \(± ([\d.]+)s\)\s*"
    r"Comparações médias:\s*([\d.]+) \(± ([\d.]+)\)\s*"
    r"Memória após [^\:]+:\s*([\d.]+) MB",
    re.MULTILINE
)

LISTA_SEARCH_PATTERN = re.compile(
    r"\[Lista Encadeada - (NÃO ordenada|ORDENADA) \((\d+) (EXISTENTES|INEXISTENTES)\)\]\s*"
    r"Tempo médio:\s*([\d.]+)s \(± ([\d.]+)s\)\s*"
    r"Comparações médias:\s*([\d.]+) \(± ([\d.]+)\)\s*"
    r"Memória após [^\:]+:\s*([\d.]+) MB",
    re.MULTILINE
)

# === FUNÇÕES ===

def create_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS creation_metrics (
      estrutura TEXT,
      tamanho_k INT,
      tempo_s FLOAT,
      memoria_mb FLOAT,
      PRIMARY KEY (estrutura, tamanho_k)
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS search_metrics (
      estrutura TEXT,
      algoritmo TEXT,
      cenario TEXT,
      tamanho_k INT,
      tempo_medio FLOAT,
      desvio_tempo FLOAT,
      comparacoes_media FLOAT,
      desvio_comparacoes FLOAT,
      memoria_mb FLOAT,
      PRIMARY KEY (estrutura, algoritmo, cenario, tamanho_k)
    );
    """)

def parse_creation(text, patterns, k):
    rows = []
    for estrutura, (pat_t, pat_m) in patterns.items():
        m_t = re.search(pat_t, text)
        m_m = re.search(pat_m, text)
        if m_t and m_m:
            rows.append({
                'estrutura':  estrutura,
                'tamanho_k':  k,
                'tempo_s':    float(m_t.group(1)),
                'memoria_mb': float(m_m.group(1))
            })
    return rows

def parse_search_vector(text, k):
    rows = []
    for m in VETOR_SEARCH_PATTERN.finditer(text):
        order, num, kind, alg, t_avg, t_dev, c_avg, c_dev, mem = m.groups()
        estrutura = f"vetor_{order.lower().replace(' ', '_')}"
        cenario   = f"{num}_{kind.lower()}"
        rows.append({
            'estrutura':          estrutura,
            'algoritmo':          alg.strip(),
            'cenario':            cenario,
            'tamanho_k':          k,
            'tempo_medio':        float(t_avg),
            'desvio_tempo':       float(t_dev),
            'comparacoes_media':  float(c_avg),
            'desvio_comparacoes': float(c_dev),
            'memoria_mb':         float(mem)
        })
    return rows

def parse_search_list(text, k):
    rows = []
    for m in LISTA_SEARCH_PATTERN.finditer(text):
        order, num, kind, t_avg, t_dev, c_avg, c_dev, mem = m.groups()
        estrutura = f"lista_{order.lower().replace(' ', '_')}"
        cenario   = f"{num}_{kind.lower()}"
        rows.append({
            'estrutura':          estrutura,
            'algoritmo':          'busca_sequencial_lista',
            'cenario':            cenario,
            'tamanho_k':          k,
            'tempo_medio':        float(t_avg),
            'desvio_tempo':       float(t_dev),
            'comparacoes_media':  float(c_avg),
            'desvio_comparacoes': float(c_dev),
            'memoria_mb':         float(mem)
        })
    return rows

# === MAIN ===

def main():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    create_tables(cur)

    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)
        # identifica tamanho k
        m_k = re.search(r'(\d+)k', fname)
        if not m_k: 
            continue
        k = int(m_k.group(1))

        text = open(path, 'r', encoding='utf-8').read()

        # criação
        if fname.startswith("saida_cria_vetores_"):
            rows_c = parse_creation(text, VETOR_CREATION, k)
        elif fname.startswith("saida_encadeada_dados"):
            rows_c = parse_creation(text, LISTA_CREATION, k)
        else:
            rows_c = []
        for r in rows_c:
            cur.execute("""
                INSERT INTO creation_metrics
                (estrutura, tamanho_k, tempo_s, memoria_mb)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (r['estrutura'], r['tamanho_k'], r['tempo_s'], r['memoria_mb']))

        # busca
        if fname.startswith("saida_cria_vetores_"):
            rows_s = parse_search_vector(text, k)
        elif fname.startswith("saida_encadeada_dados"):
            rows_s = parse_search_list(text, k)
        else:
            rows_s = []
        for r in rows_s:
            cur.execute("""
                INSERT INTO search_metrics
                (estrutura, algoritmo, cenario, tamanho_k,
                 tempo_medio, desvio_tempo,
                 comparacoes_media, desvio_comparacoes,
                 memoria_mb)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (
                r['estrutura'], r['algoritmo'], r['cenario'], r['tamanho_k'],
                r['tempo_medio'], r['desvio_tempo'],
                r['comparacoes_media'], r['desvio_comparacoes'],
                r['memoria_mb']
            ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Todos os dados foram salvos no banco.")

if __name__ == "__main__":
    main()
