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
    ├── .git/                       # Estrutura do git     
    ├── analises/                   # Arquivos de análises e algoritmos de análises
        ├── analise*.py                    # Arquivos de compilação de dados das análises    
        ├── .env                    # Configuração do banco PostgreSQL  
        ├── db.py                   # Inserção dos dados no banco PostgreSQL  
        ├── estruturas.py           # Script Python de análise da criação das estruturas
        ├── sql.py                  # Utilitário para testes de conexão e consulta de dados
        └── *.png                   # Arquivos de plotagem de dados
    ├── build/                      # Binários  
        ├── test_cria_vetores       # Executável para criar e medir vetores
        ├── test_cria_encadeadas    # Executável para criar e medir listas encadeadas
        └── exec                    # Binário principal (dependendo do Makefile)           
    ├── buscas/                     # Arquivos de entrada (.txt) com dados para buscas (10 e 1000)
        └── *.txt                   # Arquivos de entrada de buscas
    ├── data/                       # Arquivos de entrada (.txt) com dados 
        └── *.txt                   # Arquivos de entrada de 100k até 1kk em intervalos de 100k
    ├── include/                    # Arquivos de entrada (.txt) com dados para buscas (10 e 1000)
        └── funcoes.h               # Declarações de Metricas, Node e protótipos das funções de carga, busca e cálculo      
    ├── output/                     # Arquivos de saídas
        ├── le*.py                  # Arquivos de compilação de dados das análises     
        ├── *.txt                   # Arquivos de saída de métricas 
        └── *.csv                   # Arquivos de saída de métricas    
    ├── src/                        # Implementações C das estruturas e algoritmos  
        ├── funcoes.c               # Implementação de carregar_dados, buscas e cálculo de métricas
        ├── main.c                  # Programa principal que consolida criação e busca (test_cria_vetores/test_cria_encadeadas)
        ├── test_cria_vetores.c     # Teste de criação de vetores (ordenado e não ordenado) e testes
        └── test_cria_encadeadas.c  # Teste de criação de listas encadeadas (ordenada e não ordenada) e testes
    ├── .gitignore                  # Configurado com o arquivos de uso exclusivo para testes   
    ├── Artigo_EDAA.pdf             # Artigo
    ├── Artigo_EDAA_latex           # Fontes do artigo
    ├── avaliacao_1.pdf             # Descrição do trabalho
    ├── gerador_randon.py           # Gerados de dados para testes   
    ├── Makefile                    # Automatiza toda a etapa de compilação (Opcional)    
    ├── README.md                   # Este arquivo aqui
    ├── rodar_cria_encadeadas.sh    # Roda teste total de criação de estrutura e testes em encadeadas
    └── rodar_cria_vetores.sh       # Roda teste total de criação de estrutura e testes em vetores


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

### 5. Geração dos Dados de Teste

Antes de compilar e executar os testes em C, você pode gerar automaticamente os cenários de entrada (100 k, 200 k, …, 1 000 k) e os arquivos de buscas existentes/inexistentes com o script Python `gerador_randon.py`.

#### Pré-requisitos

- **Python 3.6+**  
- (opcional) um ambiente virtual Python (`venv`, `conda`, etc.)

> **Não há dependências externas** além da biblioteca padrão (`random`, `os`).

#### Como usar

1. **Certifique-se de estar na raiz do projeto** (`test_algoritmos/`):

   ```bash
   cd path/to/test_algoritmos  

2. **Execute o gerador**:

   ```bash
   python gerador_randon.py     

- Isso vai criar duas pastas (caso ainda não existam):
  - data/ — arquivos `dados100k.txt`, `dados200k.txt`, `…`, `dados1000k.txt`
  - buscas/ — arquivos de chaves existentes (`buscas_existentes_*.txt)` e inexistentes (`buscas_inexistentes_*.txt`)

3. **Verifique que os arquivos foram gerados**:

    ```bash  
    data/
    ├── dados100k.txt
    ├── dados200k.txt
    └── … 
    buscas/
    ├── buscas_existentes_100k.txt
    ├── buscas_inexistentes_100k.txt
    └── …

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
    
    
    # Torna os scripts executáveis (se ainda não estiverem)
    chmod +x rodar_cria_vetores.sh rodar_cria_encadeadas.sh

    # Executa todos os testes de criação de vetores
    ./rodar_cria_vetores.sh

    # Executa todos os testes de criação de listas encadeadas
    ./rodar_cria_encadeadas.sh

## Scripts de Consolidação de Métricas

Dois scripts em Python foram incluídos para leitura automática das saídas geradas pelos testes em C e organização das métricas em tabelas:

### `le_vetor.py`
Este script percorre os arquivos `saida_cria_vetores_*k.txt` na pasta especificada e extrai as métricas de busca em vetores ordenados e não ordenados. Para cada entrada, ele identifica:

- Tipo de vetor (ordenado ou não ordenado)
- Tipo de busca (sequencial, otimizada, com sentinela ou binária)
- Tempo médio de execução
- Número médio de comparações
- Memória utilizada

Os dados extraídos são organizados em um `DataFrame` do `pandas` e exportados em dois formatos:

- `tabela_busca_completa_vetor.csv`
- `tabela_busca_completa_vetor.xlsx`

### `le_lista.py`
Esse script realiza função similar ao anterior, mas para os arquivos `saida_encadeada_dados*k.txt`, extraindo informações de listas encadeadas ordenadas e não ordenadas. Ele identifica:

- Tipo de lista (ordenada ou não ordenada)
- Tipo de busca (existente ou inexistente)
- Algoritmo (sempre busca sequencial)
- Tempo médio, comparações e uso de memória

Os resultados são exportados para:

- `tabela_busca_completa_lista_encadeada.csv`
- `tabela_busca_completa_lista_encadeada.xlsx`

> Ambos os scripts devem ser executados com o diretório correto informado (pode ser `output/` ou outro), dependendo da organização dos seus arquivos de saída.

### Scripts de Análise Gráfica

Dois scripts Python são responsáveis por gerar os gráficos de desempenho a partir dos arquivos `.csv` criados pelas extrações anteriores:

#### `analise_vetores.py`
- Carrega os dados do arquivo `tabela_busca_completa_vetor.csv`
- Gera gráficos para cada métrica (tempo, comparações, memória), separados por tipo de busca:
  - **1000 EXISTENTES**
  - **10 INEXISTENTES**
- Cada gráfico compara os algoritmos aplicados sobre vetores:
  - Busca Sequencial
  - Sequencial Otimizada
  - Com Sentinela
  - Binária
- Salva os gráficos como PNG (`tempo_existente_por_algoritmo.png`, etc.)
- Exibe no terminal as **médias agrupadas por algoritmo**

#### `analise_listas.py`
- Lê o arquivo `tabela_busca_completa_lista_encadeada.csv`
- Gera gráficos por tipo de lista:
  - Lista Encadeada Ordenada
  - Lista Encadeada Não Ordenada
- Também separa por cenário de busca (existente e inexistente)
- Salva os gráficos como PNG (`tempo_existente_listas_encadeadas.png`, etc.)
- Exibe no terminal as **médias agrupadas por tipo de lista**

> Ambos os scripts geram gráficos com estilo customizado (cores, marcadores e linhas) e salvam os arquivos no diretório atual.

### Scripts de Análise com Desvio Padrão

Dois novos scripts foram incluídos para complementar a análise com a visualização do **desvio padrão** das métricas de tempo de execução e número de comparações:

#### `analise_vetores_desvio.py`
Este script analisa os dados de busca em **vetores**, especificamente para casos com **1000 chaves existentes**, e gera gráficos que incluem:

- Apenas desvio padrão (tempo e comparações)
- Média e desvio padrão no mesmo gráfico

São gerados arquivos `.png` com os seguintes nomes:

- `vetor_desvio_tempo_(s)_existente.png`
- `vetor_media_desvio_tempo_(s)_existente.png`
- `vetor_desvio_comparações_existente.png`
- `vetor_media_desvio_comparações_existente.png`

#### `analise_listas_desvio.py`
Este script realiza a mesma análise para **listas encadeadas** com **1000 chaves existentes**, gerando os gráficos:

- `lista_desvio_tempo_(s)_existente.png`
- `lista_media_desvio_tempo_(s)_existente.png`
- `lista_desvio_comparações_existente.png`
- `lista_media_desvio_comparações_existente.png`

#### Como Executar

Execute cada script com:

```bash
python analises/analise_vetores_desvio.py
python analises/analise_listas_desvio.py

## Licença
Este projeto é de uso acadêmico/educacional, sem fins comerciais e o seu uso implica na citação do mesmo.