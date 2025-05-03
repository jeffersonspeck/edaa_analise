#!/bin/bash

mkdir -p output

echo "estrutura,tamanho_k,etapa,tempo_s,memoria_mb" > output/metricas_cria_vetores.csv

for k in {100..1000..100}
do
  DADOS="data/dados${k}k.txt"
  EXIST="buscas/buscas_existentes_${k}k.txt"
  INEXIST="buscas/buscas_inexistentes_${k}k.txt"
  OUTTXT="output/saida_cria_vetores_${k}k.txt"

  echo "Executando para ${k}k elementos..."
  /usr/bin/time -v ./build/test_cria_vetores "$DADOS" "$EXIST" "$INEXIST" > "$OUTTXT" 2>&1

  # Extração simplificada para tempo total e memória máxima (ru_maxrss via getrusage já está no .txt)
  TEMPO_TOTAL=$(grep "Tempo de criação do vetor ORDENADO" "$OUTTXT" | grep -oP '[0-9]+\.[0-9]+')
  MEM_USO=$(grep "Memória após criação do vetor ORDENADO" "$OUTTXT" | grep -oP '[0-9]+\.[0-9]+')

  echo "cria_vetores,${k},criação_total,${TEMPO_TOTAL},${MEM_USO}" >> output/metricas_cria_vetores.csv
done
