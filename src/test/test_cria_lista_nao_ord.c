#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "funcoes.h"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Uso: %s <arquivo_dados>\n", argv[0]);
        return 1;
    }

    int tamanho;
    int* vetor = carregar_dados(argv[1], &tamanho);

    clock_t inicio = clock();
    Node* lista = NULL;
    for (int i = 0; i < tamanho; i++) {
        lista = inserir_na_lista(lista, vetor[i]);
    }
    clock_t fim = clock();

    printf("Tempo de criação da lista NÃO ordenada: %.6f s\n", (double)(fim - inicio) / CLOCKS_PER_SEC);

    while (lista) {
        Node* temp = lista;
        lista = lista->prox;
        free(temp);
    }

    free(vetor);
    return 0;
}
