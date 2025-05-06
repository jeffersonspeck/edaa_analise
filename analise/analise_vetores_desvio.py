import pandas as pd
import matplotlib.pyplot as plt

# === 1. Carregamento e preparo dos dados ===
df = pd.read_csv("../output/tabela_busca_completa_vetor.csv")  # ajuste o caminho se necessário
df["Tamanho_num"] = df["Tamanho"].str.replace("k", "").astype(int)

# Conversão robusta para float nas métricas
for col in ["Tempo (s)", "±Tempo (s)", "Comparações", "±Comparações"]:
    df[col] = df[col].astype(str).str.replace(",", ".").str.extract(r"([\d\.eE+-]+)")[0].astype(float)

# Filtrar somente buscas com chave existente
df_existente = df[df["Tipo"] == "Existente"].copy()

# === 2. Funções de plotagem ===

# Apenas desvio padrão
def plot_desvio_linhas(df, nome_col, metric):
    plt.figure(figsize=(10, 5))
    for nome in df[nome_col].unique():
        subset = df[df[nome_col] == nome].sort_values("Tamanho_num")
        plt.plot(subset["Tamanho_num"], subset[f"±{metric}"], label=f"{nome} - ±{metric}")
    plt.title(f"Desvio Padrão de {metric} (Existente) - Vetores")
    plt.xlabel("Tamanho (k)")
    plt.ylabel(f"±{metric}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"vetor_desvio_{metric.replace(' ', '_').lower()}_existente.png")
    plt.close()

# Média e desvio no mesmo gráfico
def plot_media_desvio_linhas(df, nome_col, metric):
    plt.figure(figsize=(10, 5))
    for nome in df[nome_col].unique():
        subset = df[df[nome_col] == nome].sort_values("Tamanho_num")
        plt.plot(subset["Tamanho_num"], subset[metric], label=f"{nome} - Média", linestyle='-')
        plt.plot(subset["Tamanho_num"], subset[f"±{metric}"], label=f"{nome} - Desvio", linestyle='--')
    plt.title(f"Média e Desvio de {metric} (Existente) - Vetores")
    plt.xlabel("Tamanho (k)")
    plt.ylabel(metric)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"vetor_media_desvio_{metric.replace(' ', '_').lower()}_existente.png")
    plt.close()

# === 3. Execução dos gráficos ===
plot_desvio_linhas(df_existente, "Algoritmo", "Tempo (s)")
plot_media_desvio_linhas(df_existente, "Algoritmo", "Tempo (s)")
plot_desvio_linhas(df_existente, "Algoritmo", "Comparações")
plot_media_desvio_linhas(df_existente, "Algoritmo", "Comparações")