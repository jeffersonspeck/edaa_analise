import pandas as pd
import re
import glob
import os

def parse_linked_list_metrics(directory):
    pattern = os.path.join(directory, "saida_encadeada_dados*k.txt")
    filenames = sorted(glob.glob(pattern),
                       key=lambda x: int(re.search(r'dados(\d+)k', x).group(1)))
    
    records = []
    for fname in filenames:
        size = re.search(r'dados(\d+)k', fname).group(1) + 'k'
        with open(fname, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        
        for i, line in enumerate(lines):
            if line.startswith("[Lista Encadeada"):
                ordem = "Ordenada" if "ORDENADA" in line else "Não ordenada"
                tipo = "Existente" if "EXISTENTES" in line else "Inexistente"
                alg = "Sequencial"
                m1 = re.search(r"Tempo médio:\s*([\d\.]+)s\s*\(±\s*([\d\.]+)s\)", lines[i+1])
                m2 = re.search(r"Comparações médias:\s*([\d\.]+)\s*\(±\s*([\d\.]+)\)", lines[i+2])
                m3 = re.search(r"Memória após .*:\s*([\d\.]+)\s*MB", lines[i+3])
                records.append({
                    "Lista": f"Lista Encadeada - {ordem}",
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
    df.to_csv(os.path.join(directory, "tabela_busca_completa_lista_encadeada.csv"), index=False)
    df.to_excel(os.path.join(directory, "tabela_busca_completa_lista_encadeada.xlsx"), index=False)
    print("Tabelas exportadas com sucesso!")

# Altere abaixo para o diretório onde estão os arquivos
parse_linked_list_metrics("")
