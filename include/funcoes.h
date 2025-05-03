#ifndef FUNCOES_H
#define FUNCOES_H

typedef struct {
    int comparacoes;
    double tempo_execucao;
} Metricas;

typedef struct Node {
    int valor;
    struct Node* prox;
} Node;

int* carregar_dados(const char* nome_arquivo, int* tamanho);
int* carregar_chaves(const char* nome_arquivo, int* total);
Node* inserir_na_lista(Node* head, int valor);
Node* inserir_ordenado(Node* head, int valor);

Metricas busca_sequencial(int* vetor, int tamanho, int chave);
Metricas busca_sequencial_otimizada(int* vetor, int tamanho, int chave);
Metricas busca_binaria(int* vetor, int tamanho, int chave);
Metricas busca_lista(Node* head, int chave);
Metricas busca_sequencial_sentinela(int* vetor, int tamanho, int chave);

void calcular_metricas(Metricas* resultados, int total, const char* nome_algoritmo);

#endif
