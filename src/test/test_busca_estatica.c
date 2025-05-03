#include <stdio.h>
#include <stdlib.h>
#include "funcoes.h"

void executar_testes(const char* nome_algoritmo, Metricas (*func)(int*, int, int), int* vetor, int tamanho, int* chaves, int total_chaves) {
    Metricas* resultados = malloc(total_chaves * sizeof(Metricas));
    for (int i = 0; i < total_chaves; i++) {
        resultados[i] = func(vetor, tamanho, chaves[i]);
    }
    calcular_metricas(resultados, total_chaves, nome_algoritmo);
    free(resultados);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Uso: %s <arquivo_dados> <arquivo_buscas_existentes> <arquivo_buscas_inexistentes>\n", argv[0]);
        return 1;
    }

    int tam_vetor;
    int* vetor = carregar_dados(argv[1], &tam_vetor);

    int tam_exist;
    int* chaves_exist = carregar_chaves(argv[2], &tam_exist);

    int tam_inexist;
    int* chaves_inexist = carregar_chaves(argv[3], &tam_inexist);

    printf("\n🔵 Buscas com 1000 chaves EXISTENTES:\n");
    executar_testes("Sequencial", busca_sequencial, vetor, tam_vetor, chaves_exist, tam_exist);
    executar_testes("Sequencial Otimizada", busca_sequencial_otimizada, vetor, tam_vetor, chaves_exist, tam_exist);
    executar_testes("Binária", busca_binaria, vetor, tam_vetor, chaves_exist, tam_exist);

    printf("\n🔴 Buscas com 10 chaves INEXISTENTES:\n");
    executar_testes("Sequencial", busca_sequencial, vetor, tam_vetor, chaves_inexist, tam_inexist);
    executar_testes("Sequencial Otimizada", busca_sequencial_otimizada, vetor, tam_vetor, chaves_inexist, tam_inexist);
    executar_testes("Binária", busca_binaria, vetor, tam_vetor, chaves_inexist, tam_inexist);

    free(vetor);
    free(chaves_exist);
    free(chaves_inexist);
    return 0;
}
