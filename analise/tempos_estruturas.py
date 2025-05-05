import pandas as pd
import matplotlib.pyplot as plt

# Dados da tabela
dados = {
    "tamanho_k": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    "M_LNO": [5.15, 8.57, 14.18, 17.27, 20.92, 24.0, 26.32, 29.41, 32.76, 36.02],
    "M_LO": [8.36, 14.75, 23.19, 29.37, 36.07, 42.29, 47.68, 53.76, 60.33, 66.76],
    "M_VNO": [3.2, 2.42, 4.67, 4.22, 4.06, 5.25, 4.62, 5.17, 4.99, 5.66],
    "M_VO": [4.54, 3.42, 5.7, 6.0, 5.92, 7.54, 7.52, 8.25, 8.76, 9.52],
    "T_LNO": [0.004017, 0.005236, 0.0077, 0.010646, 0.012714, 0.015024, 0.017573, 0.019859, 0.025558, 0.025482],
    "T_LO": [27.299703, 140.253383, 600.419646, 1491.131559, 2718.436103, 4047.750093, 6065.198683, 8430.430791, 10834.548501, 14065.202890],
    "T_VNO": [0.016604, 0.031061, 0.047635, 0.063409, 0.079125, 0.093145, 0.109876, 0.127907, 0.134108, 0.15775],
    "T_VO": [11.993436, 48.408307, 109.451685, 194.498081, 304.815260, 446.462121, 599.378837, 784.143006, 993.540382, 1229.069183]
}

df = pd.DataFrame(dados)

# Gráfico de linhas para TEMPO
plt.figure(figsize=(10, 5))

plt.plot(df["tamanho_k"], df["T_LNO"], label="lista_não_ordenada", marker='o', linestyle='-')
plt.plot(df["tamanho_k"], df["T_LO"], label="lista_ordenada", marker='s', linestyle='--')
plt.plot(df["tamanho_k"], df["T_VNO"], label="vetor_não_ordenado", marker='^', linestyle='-.')
plt.plot(df["tamanho_k"], df["T_VO"], label="vetor_ordenado", marker='d', linestyle=':')

plt.xlabel("Tamanho (k elementos)")
plt.ylabel("Tempo (s)")
plt.title("Comparativo de Tempo (s): vetor vs lista")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparativo_tempo_linha.png")
plt.close()

# Gráfico de linhas para MEMÓRIA
plt.figure(figsize=(10, 5))
plt.plot(df["tamanho_k"], df["M_LNO"], label="lista_não_ordenada")
plt.plot(df["tamanho_k"], df["M_LO"], label="lista_ordenada")
plt.plot(df["tamanho_k"], df["M_VNO"], label="vetor_não_ordenado")
plt.plot(df["tamanho_k"], df["M_VO"], label="vetor_ordenado")
plt.xlabel("Tamanho (k elementos)")
plt.ylabel("Memória (MB)")
plt.title("Comparativo de Memória (MB): vetor vs lista")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparativo_memoria_linha.png")
plt.close()

# Gráfico de barras - Tempo
plt.figure(figsize=(12, 6))
plt.bar(df['tamanho_k'] - 15, df['T_LNO'], width=7, label='Lista Não Ordenada')
plt.bar(df['tamanho_k'] - 5, df['T_LO'], width=7, label='Lista Ordenada')
plt.bar(df['tamanho_k'] + 5, df['T_VNO'], width=7, label='Vetor Não Ordenado')
plt.bar(df['tamanho_k'] + 15, df['T_VO'], width=7, label='Vetor Ordenado')
plt.xlabel('Tamanho (k elementos)')
plt.ylabel('Tempo (s)')
plt.title('Comparativo de Tempo (s): vetor vs lista')
plt.legend()
plt.tight_layout()
plt.savefig('comparativo_tempo_barras.png')
plt.close()

# Gráfico de barras - Memória
plt.figure(figsize=(12, 6))
plt.bar(df['tamanho_k'] - 15, df['M_LNO'], width=7, label='Lista Não Ordenada')
plt.bar(df['tamanho_k'] - 5, df['M_LO'], width=7, label='Lista Ordenada')
plt.bar(df['tamanho_k'] + 5, df['M_VNO'], width=7, label='Vetor Não Ordenado')
plt.bar(df['tamanho_k'] + 15, df['M_VO'], width=7, label='Vetor Ordenado')
plt.xlabel('Tamanho (k elementos)')
plt.ylabel('Memória (MB)')
plt.title('Comparativo de Memória (MB): vetor vs lista')
plt.legend()
plt.tight_layout()
plt.savefig('comparativo_memoria_barras.png')
plt.close()
