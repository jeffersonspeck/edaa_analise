#include <stdio.h>
#include <stdlib.h>
#include "funcoes.h"

void executar_testes_lista(const char* nome_algoritmo, Metricas (*func)(Node*, int), Node* lista, int* chaves, int total_chaves) {
    Metricas* resultados = malloc(total_chaves * sizeof(Metricas));
    for (int i = 0; i < total_chaves; i++) {
        resultados[i] = func(lista, chaves[i]);
    }
    calcular_metricas(resultados, total_chaves, nome_algoritmo);
    free(resultados);
}

Node* construir_lista(int* vetor, int tamanho, int ordenada) {
    Node* lista = NULL;
    for (int i = 0; i < tamanho; i++) {
        if (ordenada)
            lista = inserir_ordenado(lista, vetor[i]);
        else
            lista = inserir_na_lista(lista, vetor[i]);
    }
    return lista;
}

void liberar_lista(Node* lista) {
    while (lista) {
        Node* tmp = lista;
        lista = lista->prox;
        free(tmp);
    }
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

    // Lista NÃO ordenada
    printf("\n🔵 Lista NÃO ordenada (1000 chaves EXISTENTES):\n");
    Node* lista_nao = construir_lista(vetor, tam_vetor, 0);
    executar_testes_lista("Lista NÃO ordenada", busca_lista, lista_nao, chaves_exist, tam_exist);
    liberar_lista(lista_nao);

    printf("\n🔴 Lista NÃO ordenada (10 chaves INEXISTENTES):\n");
    lista_nao = construir_lista(vetor, tam_vetor, 0);
    executar_testes_lista("Lista NÃO ordenada", busca_lista, lista_nao, chaves_inexist, tam_inexist);
    liberar_lista(lista_nao);

    // Lista ordenada
    printf("\n🔵 Lista ORDENADA (1000 chaves EXISTENTES):\n");
    Node* lista_ord = construir_lista(vetor, tam_vetor, 1);
    executar_testes_lista("Lista ORDENADA", busca_lista, lista_ord, chaves_exist, tam_exist);
    liberar_lista(lista_ord);

    printf("\n🔴 Lista ORDENADA (10 chaves INEXISTENTES):\n");
    lista_ord = construir_lista(vetor, tam_vetor, 1);
    executar_testes_lista("Lista ORDENADA", busca_lista, lista_ord, chaves_inexist, tam_inexist);
    liberar_lista(lista_ord);

    free(vetor);
    free(chaves_exist);
    free(chaves_inexist);
    return 0;
}
