#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
#include "funcoes.h"

// Função de ordenação simples (bubble sort)
void ordenar(int* v, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (v[j] > v[j + 1]) {
                int tmp = v[j];
                v[j] = v[j + 1];
                v[j + 1] = tmp;
            }
        }
    }
}

void imprimir_memoria(const char* etapa) {
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    printf("Memória após %s: %.2f MB\n", etapa, r.ru_maxrss / 1024.0);
}

void executar_testes(const char* contexto, Metricas (*func)(int*, int, int), int* vetor, int tamanho, int* chaves, int total_chaves, const char* nome_algoritmo) {
    Metricas* resultados = malloc(total_chaves * sizeof(Metricas));
    for (int i = 0; i < total_chaves; i++) {
        resultados[i] = func(vetor, tamanho, chaves[i]);
    }
    printf("\n %s\n", contexto);
    calcular_metricas(resultados, total_chaves, nome_algoritmo);
    free(resultados);
    imprimir_memoria(contexto);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Uso: %s <arquivo_dados> <arquivo_chaves_existentes> <arquivo_chaves_inexistentes>\n", argv[0]);
        return 1;
    }

    int tam;
    clock_t inicio = clock();
    int* vetor_nao_ordenado = carregar_dados(argv[1], &tam);
    clock_t fim = clock();
    printf("Tempo de criação do vetor NÃO ordenado: %.6f s\n", (double)(fim - inicio) / CLOCKS_PER_SEC);
    imprimir_memoria("criação do vetor NÃO ordenado");

    int* vetor_ordenado = malloc(tam * sizeof(int));
    for (int i = 0; i < tam; i++) vetor_ordenado[i] = vetor_nao_ordenado[i];

    inicio = clock();
    ordenar(vetor_ordenado, tam);
    fim = clock();
    printf("Tempo de criação do vetor ORDENADO: %.6f s\n", (double)(fim - inicio) / CLOCKS_PER_SEC);
    imprimir_memoria("criação do vetor ORDENADO");

    int tam_exist, tam_inexist;
    int* chaves_exist = carregar_chaves(argv[2], &tam_exist);
    int* chaves_inexist = carregar_chaves(argv[3], &tam_inexist);

    // ================= Vetor NÃO ordenado =================
    executar_testes("Vetor NÃO ordenado (1000 EXISTENTES)", busca_sequencial, vetor_nao_ordenado, tam, chaves_exist, tam_exist, "Sequencial");
    executar_testes("Vetor NÃO ordenado (10 INEXISTENTES)", busca_sequencial, vetor_nao_ordenado, tam, chaves_inexist, tam_inexist, "Sequencial");

    executar_testes("Vetor NÃO ordenado (1000 EXISTENTES)", busca_sequencial_sentinela, vetor_nao_ordenado, tam, chaves_exist, tam_exist, "Sequencial com Sentinela");
    executar_testes("Vetor NÃO ordenado (10 INEXISTENTES)", busca_sequencial_sentinela, vetor_nao_ordenado, tam, chaves_inexist, tam_inexist, "Sequencial com Sentinela");    

    // ================= Vetor ORDENADO =================
    executar_testes("Vetor ORDENADO (1000 EXISTENTES)", busca_sequencial, vetor_ordenado, tam, chaves_exist, tam_exist, "Sequencial");
    executar_testes("Vetor ORDENADO (10 INEXISTENTES)", busca_sequencial, vetor_ordenado, tam, chaves_inexist, tam_inexist, "Sequencial");

    executar_testes("Vetor ORDENADO (1000 EXISTENTES)", busca_sequencial_otimizada, vetor_ordenado, tam, chaves_exist, tam_exist, "Sequencial Otimizada");
    executar_testes("Vetor ORDENADO (10 INEXISTENTES)", busca_sequencial_otimizada, vetor_ordenado, tam, chaves_inexist, tam_inexist, "Sequencial Otimizada");

    executar_testes("Vetor ORDENADO (1000 EXISTENTES)", busca_binaria, vetor_ordenado, tam, chaves_exist, tam_exist, "Binária");
    executar_testes("Vetor ORDENADO (10 INEXISTENTES)", busca_binaria, vetor_ordenado, tam, chaves_inexist, tam_inexist, "Binária");    

    free(vetor_nao_ordenado);
    free(vetor_ordenado);
    free(chaves_exist);
    free(chaves_inexist);
    return 0;
}
