#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "funcoes.h"

int* carregar_dados(const char* nome_arquivo, int* tamanho) {
    FILE* f = fopen(nome_arquivo, "r");
    if (!f) { perror("Erro ao abrir arquivo"); exit(1); }
    int* vetor = malloc(1000000 * sizeof(int));
    int valor, i = 0;
    while (fscanf(f, "%d", &valor) != EOF) vetor[i++] = valor;
    *tamanho = i;
    fclose(f);
    return vetor;
}

int* carregar_chaves(const char* nome_arquivo, int* total) {
    FILE* f = fopen(nome_arquivo, "r");
    if (!f) { perror("Erro ao abrir chaves"); exit(1); }
    int* chaves = malloc(10000 * sizeof(int));
    int valor, i = 0;
    while (fscanf(f, "%d", &valor) != EOF) chaves[i++] = valor;
    *total = i;
    fclose(f);
    return chaves;
}

Node* inserir_na_lista(Node* head, int valor) {
    Node* novo = malloc(sizeof(Node));
    novo->valor = valor;
    novo->prox = head;
    return novo;
}

Node* inserir_ordenado(Node* head, int valor) {
    Node* novo = malloc(sizeof(Node));
    novo->valor = valor;
    if (!head || valor < head->valor) {
        novo->prox = head;
        return novo;
    }
    Node* atual = head;
    while (atual->prox && atual->prox->valor < valor) {
        atual = atual->prox;
    }
    novo->prox = atual->prox;
    atual->prox = novo;
    return head;
}

Metricas busca_sequencial(int* vetor, int tamanho, int chave) {
    Metricas m = {0, 0.0};
    clock_t inicio = clock();
    for (int i = 0; i < tamanho; i++) {
        m.comparacoes++;
        if (vetor[i] == chave) break;
    }
    m.tempo_execucao = (double)(clock() - inicio) / CLOCKS_PER_SEC;
    return m;
}

Metricas busca_sequencial_otimizada(int* vetor, int tamanho, int chave) {
    Metricas m = {0, 0.0};
    clock_t inicio = clock();
    for (int i = 0; i < tamanho; i++) {
        m.comparacoes++;
        if (vetor[i] >= chave) {
            if (vetor[i] == chave) break;
            else break;
        }
    }
    m.tempo_execucao = (double)(clock() - inicio) / CLOCKS_PER_SEC;
    return m;
}

Metricas busca_sequencial_sentinela(int* vetor, int tamanho, int chave) {
    Metricas m = {0, 0.0};
    clock_t inicio = clock();

    int ultimo = vetor[tamanho - 1];
    vetor[tamanho - 1] = chave;  // sentinela

    int i = 0;
    while (vetor[i] != chave) {
        i++;
        m.comparacoes++;
    }

    vetor[tamanho - 1] = ultimo;  // restaura

    m.tempo_execucao = (double)(clock() - inicio) / CLOCKS_PER_SEC;
    return m;
}

Metricas busca_binaria(int* vetor, int tamanho, int chave) {
    Metricas m = {0, 0.0};
    int esq = 0, dir = tamanho - 1, meio;
    clock_t inicio = clock();
    while (esq <= dir) {
        m.comparacoes++;
        meio = (esq + dir) / 2;
        if (vetor[meio] == chave) break;
        else if (vetor[meio] < chave) esq = meio + 1;
        else dir = meio - 1;
    }
    m.tempo_execucao = (double)(clock() - inicio) / CLOCKS_PER_SEC;
    return m;
}

Metricas busca_lista(Node* head, int chave) {
    Metricas m = {0, 0.0};
    clock_t inicio = clock();
    Node* atual = head;
    while (atual) {
        m.comparacoes++;
        if (atual->valor == chave) break;
        atual = atual->prox;
    }
    m.tempo_execucao = (double)(clock() - inicio) / CLOCKS_PER_SEC;
    return m;
}

void calcular_metricas(Metricas* resultados, int total, const char* nome_algoritmo) {
    double soma_tempo = 0, soma_comp = 0;
    for (int i = 0; i < total; i++) {
        soma_tempo += resultados[i].tempo_execucao;
        soma_comp += resultados[i].comparacoes;
    }
    double media_tempo = soma_tempo / total;
    double media_comp = soma_comp / total;
    double desvio_tempo = 0, desvio_comp = 0;
    for (int i = 0; i < total; i++) {
        desvio_tempo += pow(resultados[i].tempo_execucao - media_tempo, 2);
        desvio_comp += pow(resultados[i].comparacoes - media_comp, 2);
    }
    desvio_tempo = sqrt(desvio_tempo / total);
    desvio_comp = sqrt(desvio_comp / total);
    printf("\n[%s]\n", nome_algoritmo);
    printf("Tempo médio: %.6fs (± %.6fs)\n", media_tempo, desvio_tempo);
    printf("Comparações médias: %.2f (± %.2f)\n", media_comp, desvio_comp);
}