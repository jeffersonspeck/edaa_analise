import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV
df = pd.read_csv("../output/tabela_busca_completa_vetor.csv")
df["Tamanho_num"] = df["Tamanho"].str.replace("k", "").astype(int)

# Estilo visual para cada algoritmo
estilos = {
    "Sequencial": {"marker": "o", "linestyle": "-", "linewidth": 2},
    "Sentinela": {"marker": "s", "linestyle": "--", "linewidth": 2},
    "Sequencial Otimizada": {"marker": "D", "linestyle": "-.", "linewidth": 2},
    "Binária": {"marker": "^", "linestyle": ":", "linewidth": 2},
}

# Função para plotar
def plot_metric(metric, ylabel, title_prefix, tipo):
    plt.figure(figsize=(12, 7))
    for alg in df["Algoritmo"].unique():
        subset = df[(df["Tipo"] == tipo) & (df["Algoritmo"] == alg)].sort_values("Tamanho_num")
        estilo = estilos.get(alg, {"marker": "o", "linestyle": "-", "linewidth": 2})
        plt.plot(subset["Tamanho_num"], subset[metric],
                 marker=estilo["marker"],
                 linestyle=estilo["linestyle"],
                 linewidth=estilo["linewidth"],
                 markersize=7,
                 label=alg)
    plt.title(f"{title_prefix} ({tipo}) por Algoritmo", fontsize=14)
    plt.xlabel("Tamanho do Vetor (k)", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    fname = f"{metric.replace(' ', '_')}_{tipo.lower()}_por_algoritmo.png"
    plt.savefig(fname)
    plt.close()

# Gera os gráficos para ambos os cenários
for tipo in ["Existente", "Inexistente"]:
    plot_metric("Tempo (s)", "Tempo Médio (s)", "Tempo de Busca", tipo)
    plot_metric("Comparações", "Comparações Médias", "Comparações na Busca", tipo)
    plot_metric("Memória (MB)", "Memória (MB)", "Uso de Memória", tipo)

# Comparativo de médias
for tipo in ["Existente", "Inexistente"]:
    media = df[df["Tipo"] == tipo].groupby("Algoritmo")[["Tempo (s)", "Comparações", "Memória (MB)"]].mean()
    print(f"\n==== MÉDIA - {tipo} ====")
    print(media.sort_values("Tempo (s)"))