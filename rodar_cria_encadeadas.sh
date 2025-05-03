#!/bin/bash

mkdir -p output

echo "estrutura,tamanho_k,etapa,tempo_s,memoria_mb" > output/metricas_cria_encadeadas.csv

for k in {100..1000..100}
do
  DADOS="data/dados${k}k.txt"
  EXIST="buscas/buscas_existentes_${k}k.txt"
  INEXIST="buscas/buscas_inexistentes_${k}k.txt"
  OUTTXT="output/saida_cria_encadeadas_${k}k.txt"

  echo "Executando listas encadeadas para ${k}k elementos..."
  /usr/bin/time -v ./build/test_cria_encadeadas "$DADOS" "$EXIST" "$INEXIST" > "$OUTTXT" 2>&1

  # Extrai tempo e memória da criação ORDENADA (linha impressa pelo programa)
  TEMPO_TOTAL=$(grep "Tempo de criação da lista ORDENADA" "$OUTTXT" | grep -oP '[0-9]+\.[0-9]+')
  MEM_USO=$(grep "Memória após criação da lista ORDENADA" "$OUTTXT" | grep -oP '[0-9]+\.[0-9]+')

  echo "cria_encadeadas,${k},criação_total,${TEMPO_TOTAL},${MEM_USO}" >> output/metricas_cria_encadeadas.csv
done
