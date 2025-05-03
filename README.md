# Projeto: Análise de Algoritmos de Busca e Estruturas de Dados

Este projeto realiza a **criação**, **execução de buscas** e **análise comparativa de desempenho** de estruturas de dados do tipo **vetor estático** e **lista encadeada**, com foco em **tempo de criação**, **uso de memória** e **eficiência de busca**.

## Estrutura do Projeto
    ```bash
    test_algoritmos/
    │
    ├── data/                    # Arquivos de entrada (.txt) com dados e chaves de busca  
    ├── output/                  # Saída de execução com métricas extraídas  
    ├── src/                     # Implementações C das estruturas e algoritmos  
    ├── build/                   # Binaries gerados  
    ├── .env                     # Configuração do banco PostgreSQL  
    ├── estruturas.py            # Script Python de análise da criação das estruturas  
    ├── salva_dados.py           # Inserção dos dados no banco PostgreSQL  
    └── *.txt                    # Arquivos de saída de métricas  

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

## Licença
Este projeto é de uso acadêmico/educacional, sem fins comerciais e o seu uso implica na citação do mesmo.