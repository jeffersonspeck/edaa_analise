#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "funcoes.h"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Uso: %s <arquivo_dados> <arquivo_buscas>\n", argv[0]);
        return 1;
    }

    const char* arquivo_dados = argv[1];
    const char* arquivo_buscas = argv[2];

    int tamanho_vetor;
    int* vetor = carregar_dados(arquivo_dados, &tamanho_vetor);

    Node* lista = NULL;
    for (int i = tamanho_vetor - 1; i >= 0; i--) {
        lista = inserir_na_lista(lista, vetor[i]);
    }

    int total_chaves;
    int* chaves = carregar_chaves(arquivo_buscas, &total_chaves);

    if (strstr(arquivo_buscas, "inexistentes"))
        printf("🛑 Executando PIOR CASO: %s\n", arquivo_buscas);
    else
        printf("✅ Executando busca normal: %s\n", arquivo_buscas);

    testar_com_buscas(vetor, tamanho_vetor, chaves, total_chaves, lista);

    free(vetor);
    free(chaves);
    return 0;
}
