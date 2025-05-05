import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados da lista encadeada
df = pd.read_csv("../output/tabela_busca_completa_lista_encadeada.csv")
df["Tamanho_num"] = df["Tamanho"].str.replace("k", "").astype(int)

# Estilo visual para cada tipo de lista (ordenação)
estilos = {
    "Lista Encadeada - Ordenada": {"marker": "s", "linestyle": "--", "linewidth": 2},
    "Lista Encadeada - Não ordenada": {"marker": "o", "linestyle": "-", "linewidth": 2},
}

# Função para plotar gráficos por tipo (existente/inexistente)
def plot_metric(metric, ylabel, title_prefix, tipo):
    plt.figure(figsize=(12, 7))
    for lista in df["Lista"].unique():
        subset = df[(df["Tipo"] == tipo) & (df["Lista"] == lista)].sort_values("Tamanho_num")
        estilo = estilos.get(lista, {"marker": "o", "linestyle": "-", "linewidth": 2})
        plt.plot(subset["Tamanho_num"], subset[metric],
                 marker=estilo["marker"],
                 linestyle=estilo["linestyle"],
                 linewidth=estilo["linewidth"],
                 markersize=7,
                 label=lista)
    plt.title(f"{title_prefix} ({tipo}) - Listas Encadeadas", fontsize=14)
    plt.xlabel("Tamanho da Lista (k)", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    fname = f"{metric.replace(' ', '_')}_{tipo.lower()}_listas_encadeadas.png"
    plt.savefig(fname)
    plt.close()

# Gera os gráficos para ambos os cenários
for tipo in ["Existente", "Inexistente"]:
    plot_metric("Tempo (s)", "Tempo Médio (s)", "Tempo de Busca", tipo)
    plot_metric("Comparações", "Comparações Médias", "Comparações na Busca", tipo)
    plot_metric("Memória (MB)", "Memória (MB)", "Uso de Memória", tipo)

# Comparativo de médias por tipo de lista
for tipo in ["Existente", "Inexistente"]:
    media = df[df["Tipo"] == tipo].groupby("Lista")[["Tempo (s)", "Comparações", "Memória (MB)"]].mean()
    print(f"\n==== MÉDIA - {tipo} ====")
    print(media.sort_values("Tempo (s)"))