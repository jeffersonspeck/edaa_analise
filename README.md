# Projeto: Análise de Algoritmos de Busca e Estruturas de Dados

## Introdução

Neste projeto da disciplina **Estruturas de Dados e Análise de Algoritmos (EDAA)**, avaliamos e comparamos a eficiência de diferentes métodos de busca sobre duas classes de estruturas de dados:

1. **Arranjos estáticos**  
   - Busca sequencial (padrão e otimizada)  
   - Busca binária  

2. **Listas encadeadas**  
   - Busca sequencial em lista não ordenada  
   - Busca sequencial em lista ordenada  

O objetivo é medir, para cada abordagem, o tempo de criação das estruturas, o número de comparações durante a busca, o tempo total de execução (criação + busca) e o consumo de memória. Para isso, geramos cenários de teste variando o tamanho do conjunto de chaves de **100 000** até **1 000 000** elementos (incrementos de 100k) e avaliamos tanto o **pior caso** (10 buscas de chaves inexistentes) quanto **casos aleatórios** (1 000 buscas de chaves existentes).  
Esta atividade é a **Avaliação 1 – Algoritmos de Busca**.

## Estrutura do Projeto
    test_algoritmos/
    │
    ├── data/                                  # Arquivos de entrada (.txt) com dados e chaves de busca  
    ├── output/                                # Saída de execução com métricas extraídas  
    ├── src/                                   # Implementações C das estruturas e algoritmos  
    ├── build/                                 # Binaries gerados  
    ├── .env                                   # Configuração do banco PostgreSQL  
    ├── estruturas.py                          # Script Python de análise da criação das estruturas  
    ├── salva_dados.py                         # Inserção dos dados no banco PostgreSQL  
    ├── *.txt                                  # Arquivos de saída de métricas
    └── Avaliacao_1_-_Algoritmos_de_Busca.pdf  # Descrição do trabalho    


## Funcionalidades

### 1. Criação de Estruturas
- **Vetores ordenados e não ordenados**
- **Listas encadeadas ordenadas e não ordenadas**
- Mede e armazena:
  - Tempo de criação (segundos)
  - Uso de memória (MB)

### 2. Execução de Testes de Busca
- Busca em:
  - Vetor: sequencial, otimizada, binária
  - Lista: sequencial
- Casos:
  - 1000 chaves existentes
  - 10 chaves inexistentes

### 3. Armazenamento em Banco de Dados
- Banco **PostgreSQL**
- Tabelas:
  - `creation_metrics`: armazena tempo e memória de criação
  - `resultados_encadeadas`: resultados de execução e comparações

### 4. Análise e Visualização
- Geração de gráficos:
  - Tempo vs tamanho
  - Memória vs tamanho
  - Comparativo vetor × lista
- Geração de tabelas visuais:
  - Comparativas (tempo e memória)
  - Métricas individuais por tamanho (`100k`, `200k`, `300k`, `400k`, `500k`,`600k`,`700k`,`800k`,`900k`,`1kk`.)

## Exemplos de gráficos gerados
- `metricas_100k.png`, `metricas_200k.png`, ...
- `tabela_metricas_criacao.png`
- `comparativo_tempo_vetor_lista.png`

## Requisitos
- Python 3.10+
- PostgreSQL configurado com `.env`
- Bibliotecas Python:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `sqlalchemy`
  - `psycopg2`
  - `python-dotenv`

## Execução
1. **Compilar os testes (C):**
   ```bash
   make build/test_cria_encadeadas

2. Executar testes e gerar saídas:
    ```bash
    ./build/test_cria_encadeadas data/dados100k.txt buscas/buscas_existentes_100k.txt buscas/buscas_inexistentes_100k.txt

3. Salvar os dados no banco:
    ```bash
    python salva_dados.py

4. Gerar análises e gráficos:
    ```bash
    python estruturas.py

## Scripts de Execução Automática
Além dos binários em C, incluímos dois _shell scripts_ que gerenciam toda a geração de métricas de criação de estruturas:

- **`rodar_cria_vetores.sh`**  
Roda o programa `test_cria_vetores` para tamanhos de 100 k até 1 000 k (passo de 100 k), medindo tempo de criação de vetores ordenados e não ordenados e consumo de memória. Os resultados são extraídos do `stdout` e das informações do `/usr/bin/time -v` e salvos em  
`output/metricas_cria_vetores.csv` :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.

- **`rodar_cria_encadeadas.sh`**  
Faz o mesmo para `test_cria_encadeadas`, gerando métricas de criação de listas encadeadas ordenadas e não ordenadas nos mesmos tamanhos, e grava em  
`output/metricas_cria_encadeadas.csv` :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}.

### Como usar
    
    ```bash
    # Torna os scripts executáveis (se ainda não estiverem)
    chmod +x rodar_cria_vetores.sh rodar_cria_encadeadas.sh

    # Executa todos os testes de criação de vetores
    ./rodar_cria_vetores.sh

    # Executa todos os testes de criação de listas encadeadas
    ./rodar_cria_encadeadas.sh

## Licença
Este projeto é de uso acadêmico/educacional, sem fins comerciais e o seu uso implica na citação do mesmo.