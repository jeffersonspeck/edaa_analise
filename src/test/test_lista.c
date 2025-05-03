#include <stdio.h>
#include <stdlib.h>
#include "funcoes.h"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Uso: %s <arquivo_dados> <arquivo_buscas>\n", argv[0]);
        return 1;
    }

    int tamanho_vetor;
    int* vetor = carregar_dados(argv[1], &tamanho_vetor);

    int total_chaves;
    int* chaves = carregar_chaves(argv[2], &total_chaves);

    for (int i = 0; i < total_chaves; i++) {
        busca_lista(vetor, tamanho_vetor, chaves[i]);
    }

    free(vetor);
    free(chaves);
    return 0;
}
