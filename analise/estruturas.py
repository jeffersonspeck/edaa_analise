#!/usr/bin/env python3
# estruturas.py

import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

load_dotenv()

DB_NAME     = os.getenv('DB_NAME')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST     = os.getenv('DB_HOST')
DB_PORT     = os.getenv('DB_PORT', '5432')

# Conexão com o banco
url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(url)

def load_data():
    df = pd.read_sql_table('creation_metrics', con=engine)
    df['estrutura'] = df['estrutura'].str.strip()
    df['tamanho_k'] = df['tamanho_k'].astype(int)
    df['tipo'] = df['estrutura'].apply(lambda s: 'vetor' if 'vetor' in s else 'lista')
    return df

def salvar_tabela(df, fname='tabela_metricas_criacao.png'):
    import matplotlib.pyplot as plt

    pivot = df.pivot_table(
        index='tamanho_k',
        columns='estrutura',
        values=['tempo_s', 'memoria_mb']
    )

    abreviacoes = {
        'vetor_ordenado': 'VO',
        'vetor_não_ordenado': 'VNO',
        'lista_ordenada': 'LO',
        'lista_não_ordenada': 'LNO',
        'tempo_s': 'T',
        'memoria_mb': 'M'
    }

    # Formatação personalizada
    def formatar_valor(metric, val):
        if pd.isnull(val): return ""
        return f"{val:.2f}" if metric == "memoria_mb" else f"{val:.6f}"

    cell_text = [
        [
            formatar_valor(metric, pivot.iloc[i][metric, estrutura])
            for metric, estrutura in pivot.columns
        ]
        for i in range(pivot.shape[0])
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    table = ax.table(
        cellText=cell_text,
        rowLabels=pivot.index,
        colLabels=[f"{abreviacoes[metric]}_{abreviacoes[col]}" for metric, col in pivot.columns],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.3)

    plt.subplots_adjust(top=0.86, bottom=0.12)
    plt.title("Tempo (s) e Memória (MB) por Estrutura e Tamanho", fontsize=13, pad=10)
    legenda = "Legenda: T = Tempo (s), M = Memória (MB), VO = Vetor Ordenado, VNO = Vetor Não Ordenado, LO = Lista Ordenada, LNO = Lista Não Ordenada"
    plt.figtext(0.5, 0.04, legenda, wrap=True, ha='center', fontsize=9)

    plt.savefig(fname)
    plt.close()

def graficos_por_tamanho(df):
    estruturas = [
        'lista_não_ordenada', 'lista_ordenada',
        'vetor_não_ordenado', 'vetor_ordenado'
    ]

    # Gráficos agregados com pivot
    pivot_tempo = df.pivot_table(
        index='tamanho_k',
        columns='estrutura',
        values='tempo_s'
    ).reindex(columns=estruturas)

    pivot_memoria = df.pivot_table(
        index='tamanho_k',
        columns='estrutura',
        values='memoria_mb'
    ).reindex(columns=estruturas)

    # Plot Tempo
    pivot_tempo.plot(kind='bar', figsize=(14, 6))
    plt.title("Tempo de Criação por Estrutura e Tamanho")
    plt.xlabel("Tamanho (k)")
    plt.ylabel("Tempo (s)")
    plt.xticks(rotation=0)
    plt.legend(title='Estrutura')
    plt.tight_layout()
    plt.savefig("tempo_por_tamanho.png")
    plt.show()

    # Plot Memória
    pivot_memoria.plot(kind='bar', figsize=(14, 6))
    plt.title("Uso de Memória por Estrutura e Tamanho")
    plt.xlabel("Tamanho (k)")
    plt.ylabel("Memória (MB)")
    plt.xticks(rotation=0)
    plt.legend(title='Estrutura')
    plt.tight_layout()
    plt.savefig("memoria_por_tamanho.png")
    plt.show()

    # Gráficos individuais por tamanho
    for k in sorted(df['tamanho_k'].unique()):
        dados = df[df['tamanho_k'] == k].copy()

        # Garante que todas as 4 estruturas estejam presentes
        completo = pd.DataFrame({'estrutura': estruturas})
        completo['tamanho_k'] = k
        dados = pd.merge(completo, dados, on=['tamanho_k', 'estrutura'], how='left')

        dados['estrutura'] = pd.Categorical(dados['estrutura'], categories=estruturas, ordered=True)
        dados = dados.sort_values('estrutura')

        plt.figure(figsize=(12, 5))

        # Subplot 1: Tempo
        plt.subplot(1, 2, 1)
        sns.barplot(data=dados, x='estrutura', y='tempo_s', palette='Blues_d')
        plt.title(f"{k}k - Tempo (s)")
        plt.xticks(rotation=15)

        # Subplot 2: Memória
        plt.subplot(1, 2, 2)
        sns.barplot(data=dados, x='estrutura', y='memoria_mb', palette='Greens_d')
        plt.title(f"{k}k - Memória (MB)")
        plt.xticks(rotation=15)

        plt.suptitle(f"Métricas para {k}k Elementos", fontsize=14)
        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(f"metricas_{k}k.png")
        plt.close()

def salvar_tabela_comparativa(df, nome_arquivo="tabela_comparativa.png"):
    """
    Gera uma imagem com os dados de tempo e memória para lista/vetor, ordenado e não ordenado,
    agrupados por tamanho_k.
    """
    import matplotlib.pyplot as plt

    # Filtra e ordena os dados
    df = df.copy()
    df = df.sort_values(by=["tamanho_k", "estrutura"])

    # Cria uma tabela customizada com colunas específicas
    linhas = []
    for k in sorted(df["tamanho_k"].unique()):
        linha_ordenada = [f"{k}k - ORDENADO"]
        linha_nao_ordenado = [f"{k}k - NÃO ORDENADO"]

        for tipo in ["vetor", "lista"]:
            est_ord = df[(df["tamanho_k"] == k) & (df["estrutura"].str.contains(tipo)) & (df["estrutura"].str.contains("ordenado"))]
            est_nao = df[(df["tamanho_k"] == k) & (df["estrutura"].str.contains(tipo)) & (df["estrutura"].str.contains("não_ordenado"))]

            if not est_ord.empty:
                t = f'{est_ord["tempo_s"].values[0]:.3f}s'
                m = f'{est_ord["memoria_mb"].values[0]:.2f}MB'
                linha_ordenada.append(f"{t} / {m}")
            else:
                linha_ordenada.append("N/A")

            if not est_nao.empty:
                t = f'{est_nao["tempo_s"].values[0]:.3f}s'
                m = f'{est_nao["memoria_mb"].values[0]:.2f}MB'
                linha_nao_ordenado.append(f"{t} / {m}")
            else:
                linha_nao_ordenado.append("N/A")

        linhas.append(linha_ordenada)
        linhas.append(linha_nao_ordenado)

    colunas = ["Tamanho / Tipo", "Vetor", "Lista"]

    # Plota tabela
    fig, ax = plt.subplots(figsize=(10, len(linhas) * 0.5 + 1))
    ax.axis("off")
    table = ax.table(
        cellText=linhas,
        colLabels=colunas,
        loc="center",
        cellLoc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    plt.title("Tempo (s) / Memória (MB) - Comparação por Estrutura e Ordenação", fontsize=12)
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"📄 Tabela comparativa salva em {nome_arquivo}")        

def main():
    sns.set(style="whitegrid")
    df = load_data()

    print("\n=== Dados de Criação de Estruturas ===")
    print(df.sort_values(['tamanho_k', 'estrutura']).to_string(index=False))

    print("\n=== Estatísticas Gerais ===")
    print(df[['tempo_s', 'memoria_mb']].describe().round(3))

    print("\n=== Estatísticas por Tipo ===")
    print(df.groupby('tipo')[['tempo_s', 'memoria_mb']].agg(['mean','std','min','max','median']).round(3))

    # 1) Tabela geral com tempo/memória por estrutura
    salvar_tabela(df)

    # 2) Gráficos por grupo 100k, 200k, ...
    graficos_por_tamanho(df)

    # salvar_tabela_comparativa(df)

    # 3) Comparações agregadas (como antes)
    for y, ylabel, fname in [
        ('tempo_s', 'Tempo (s)', 'comparativo_tempo_por_estrutura.png'),
        ('memoria_mb', 'Memória (MB)', 'comparativo_memoria_por_estrutura.png')
    ]:
        pivot = df.pivot_table(index='tamanho_k', columns='estrutura', values=y)
        pivot.plot(kind='bar', figsize=(10, 6))
        plt.title(f"Comparativo de {ylabel}: vetor vs lista")
        plt.xlabel("Tamanho (k elementos)")
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()

    print("\n✅ Tabela e gráficos salvos com sucesso.")

if __name__ == "__main__":
    main()
