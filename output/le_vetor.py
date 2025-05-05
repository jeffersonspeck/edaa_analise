import pandas as pd
import re
import glob
import os

def parse_metrics(directory):
    pattern = os.path.join(directory, "saida_cria_vetores_*k.txt")
    filenames = sorted(glob.glob(pattern),
                       key=lambda x: int(re.search(r'_(\d+)k', x).group(1)))
    records = []
    for fname in filenames:
        size = re.search(r'_(\d+)k', fname).group(1) + 'k'
        with open(fname, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        for i, line in enumerate(lines):
            if line.lower().startswith('vetor'):
                vec = "Vetor não ordenado" if "não ordenado" in line.lower() else "Vetor ordenado"
                tipo = "Existente" if "EXISTENTES" in line.upper() else "Inexistente"
                alg_line = lines[i+1]
                if "sentinela" in alg_line.lower():
                    alg = "Sentinela"
                elif "binária" in alg_line.lower():
                    alg = "Binária"
                elif "otimizada" in alg_line.lower():
                    alg = "Sequencial Otimizada"
                else:
                    alg = "Sequencial"
                m1 = re.search(r"([\d\.]+)\s*s\s*\(±\s*([\d\.]+)\s*s\)", lines[i+2])
                m2 = re.search(r"([\d\.]+)\s*\(±\s*([\d\.]+)\)", lines[i+3])
                m3 = re.search(r"([\d\.]+)\s*MB", lines[i+4])
                records.append({
                    "Vetor": vec,
                    "Tipo": tipo,
                    "Algoritmo": alg,
                    "Tempo (s)": float(m1.group(1)),
                    "±Tempo (s)": f"±{float(m1.group(2)):.6f}",
                    "Comparações": float(m2.group(1)),
                    "±Comparações": f"±{float(m2.group(2)):.2f}",
                    "Memória (MB)": float(m3.group(1)),
                    "Tamanho": size
                })
    df = pd.DataFrame(records)
    return df

# Altere o caminho conforme necessário
diretorio = ""
df = parse_metrics(diretorio)

# Exporta os arquivos
df.to_csv(os.path.join(diretorio, "tabela_busca_completa_vetor.csv"), index=False)
df.to_excel(os.path.join(diretorio, "tabela_busca_completa_vetor.xlsx"), index=False)

print("Arquivos CSV e Excel gerados com sucesso.")