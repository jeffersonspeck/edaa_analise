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
    clock_t inicio = clock();
    int* vetor = carregar_dados(argv[1], &tamanho);
        // Bubble sort
    for (int i = 0; i < tamanho - 1; i++) {
        for (int j = 0; j < tamanho - i - 1; j++) {
            if (vetor[j] > vetor[j + 1]) {
                int tmp = vetor[j];
                vetor[j] = vetor[j + 1];
                vetor[j + 1] = tmp;
            }
        }
    }
    clock_t fim = clock();

    printf("Tempo de criação do vetor ordenado: %.6f s\n", (double)(fim - inicio) / CLOCKS_PER_SEC);
    free(vetor);
    return 0;
}
