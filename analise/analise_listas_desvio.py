import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados
df = pd.read_csv("../output/tabela_busca_completa_lista_encadeada.csv")
df["Tamanho_num"] = df["Tamanho"].str.replace("k", "").astype(int)

# Converte todas as métricas e desvios para float
for col in ["Tempo (s)", "±Tempo (s)", "Comparações", "±Comparações"]:
    df[col] = df[col].astype(str).str.replace(",", ".").str.extract(r"([\d\.eE+-]+)")[0].astype(float)

# Filtra casos existentes
df_existente = df[df["Tipo"] == "Existente"].copy()

# Funções atualizadas com salvamento
def plot_desvio_linhas(df, nome_col, metric):
    plt.figure(figsize=(10, 5))
    for nome in df[nome_col].unique():
        subset = df[df[nome_col] == nome].sort_values("Tamanho_num")
        plt.plot(subset["Tamanho_num"], subset[f"±{metric}"], label=f"{nome} - ±{metric}")
    plt.title(f"Desvio Padrão de {metric} (Existente)")
    plt.xlabel("Tamanho (k)")
    plt.ylabel(f"±{metric}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"lista_desvio_{metric.replace(' ', '_').lower()}_existente.png")
    plt.close()

def plot_media_desvio_linhas(df, nome_col, metric):
    plt.figure(figsize=(10, 5))
    for nome in df[nome_col].unique():
        subset = df[df[nome_col] == nome].sort_values("Tamanho_num")
        plt.plot(subset["Tamanho_num"], subset[metric], label=f"{nome} - Média", linestyle='-')
        plt.plot(subset["Tamanho_num"], subset[f"±{metric}"], label=f"{nome} - Desvio", linestyle='--')
    plt.title(f"Média e Desvio de {metric} (Existente)")
    plt.xlabel("Tamanho (k)")
    plt.ylabel(metric)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"lista_media_desvio_{metric.replace(' ', '_').lower()}_existente.png")
    plt.close()

# Geração dos gráficos corrigidos
plot_desvio_linhas(df_existente, "Lista", "Tempo (s)")
plot_media_desvio_linhas(df_existente, "Lista", "Tempo (s)")
plot_desvio_linhas(df_existente, "Lista", "Comparações")
plot_media_desvio_linhas(df_existente, "Lista", "Comparações")
