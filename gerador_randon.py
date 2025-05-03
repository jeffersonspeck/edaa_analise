import random
import os

def gerar_dados_e_buscas():
    os.makedirs("data", exist_ok=True)
    os.makedirs("buscas", exist_ok=True)

    for tamanho in range(100_000, 1_000_001, 100_000):
        dados = random.sample(range(1, 10_000_000), tamanho)
        nome_arquivo_dados = f"data/dados{tamanho//1000}k.txt"
        with open(nome_arquivo_dados, "w") as f:
            for numero in dados:
                f.write(f"{numero}\n")
        print(f"Arquivo '{nome_arquivo_dados}' gerado com {tamanho} elementos.")

        # 🔹 Gera 1000 buscas aleatórias existentes
        buscas_existentes = random.choices(dados, k=1000)
        nome_buscas_ok = f"buscas/buscas_existentes_{tamanho//1000}k.txt"
        with open(nome_buscas_ok, "w") as f:
            for chave in buscas_existentes:
                f.write(f"{chave}\n")
        print(f"1000 buscas aleatórias existentes geradas: {nome_buscas_ok}")

        # 🔹 Gera 10 chaves inexistentes (acima do maior valor presente)
        maior_valor = max(dados)
        buscas_inexistentes = [maior_valor + i + 1 for i in range(10)]
        nome_buscas_fail = f"buscas/buscas_inexistentes_{tamanho//1000}k.txt"
        with open(nome_buscas_fail, "w") as f:
            for chave in buscas_inexistentes:
                f.write(f"{chave}\n")
        print(f"10 buscas inexistentes (pior caso) geradas: {nome_buscas_fail}")

if __name__ == "__main__":
    gerar_dados_e_buscas()
