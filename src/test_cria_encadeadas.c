#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <sys/resource.h>
#include "funcoes.h"

void imprimir_memoria(const char* etapa, FILE* ftxt, FILE* fcsv) {
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    double mem = r.ru_maxrss / 1024.0;
    fprintf(stdout, "Memória após %s: %.2f MB\n", etapa, mem);
    if (ftxt) fprintf(ftxt, "Memória após %s: %.2f MB\n", etapa, mem);
    if (fcsv) fprintf(fcsv, ",%.2f", mem);
}

void executar_testes_lista(const char* contexto, Node* head, int* chaves, int total_chaves, const char* nome_algoritmo, FILE* ftxt, FILE* fcsv) {
    Metricas* resultados = malloc(total_chaves * sizeof(Metricas));
    for (int i = 0; i < total_chaves; i++) {
        resultados[i] = busca_lista(head, chaves[i]);
    }

    double soma_tempo = 0, soma_comp = 0;
    for (int i = 0; i < total_chaves; i++) {
        soma_tempo += resultados[i].tempo_execucao;
        soma_comp += resultados[i].comparacoes;
    }
    double media_tempo = soma_tempo / total_chaves;
    double media_comp = soma_comp / total_chaves;

    double desvio_tempo = 0, desvio_comp = 0;
    for (int i = 0; i < total_chaves; i++) {
        desvio_tempo += pow(resultados[i].tempo_execucao - media_tempo, 2);
        desvio_comp += pow(resultados[i].comparacoes - media_comp, 2);
    }
    desvio_tempo = sqrt(desvio_tempo / total_chaves);
    desvio_comp = sqrt(desvio_comp / total_chaves);

    fprintf(stdout, "\n[%s - %s]\n", nome_algoritmo, contexto);
    fprintf(stdout, "Tempo médio: %.6fs (± %.6fs)\n", media_tempo, desvio_tempo);
    fprintf(stdout, "Comparações médias: %.2f (± %.2f)\n", media_comp, desvio_comp);

    if (ftxt) {
        fprintf(ftxt, "\n[%s - %s]\n", nome_algoritmo, contexto);
        fprintf(ftxt, "Tempo médio: %.6fs (± %.6fs)\n", media_tempo, desvio_tempo);
        fprintf(ftxt, "Comparações médias: %.2f (± %.2f)\n", media_comp, desvio_comp);
    }

    if (fcsv)
        fprintf(fcsv, "\n%s,%s,%.6f,%.6f,%.2f,%.2f", nome_algoritmo, contexto, media_tempo, desvio_tempo, media_comp, desvio_comp);

    free(resultados);
    imprimir_memoria(contexto, ftxt, fcsv);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Uso: %s <arquivo_dados> <arquivo_chaves_existentes> <arquivo_chaves_inexistentes>\n", argv[0]);
        return 1;
    }

    char* arq_dados = argv[1];
    int tam;
    int* vetor = carregar_dados(arq_dados, &tam);

    // Extrai o nome base sem caminho nem extensão
    const char* base = strrchr(arq_dados, '/') ? strrchr(arq_dados, '/') + 1 : arq_dados;
    char nome_base[64];
    strncpy(nome_base, base, sizeof(nome_base) - 1);
    nome_base[sizeof(nome_base) - 1] = '\0';
    nome_base[strcspn(nome_base, ".")] = '\0';  // remove extensão

    char csv_saida[128], txt_saida[128];
    snprintf(csv_saida, sizeof(csv_saida), "output/resultados_encadeada_%s.csv", nome_base);
    snprintf(txt_saida, sizeof(txt_saida), "output/saida_encadeada_%s.txt", nome_base);

    FILE* fcsv = fopen(csv_saida, "w");
    FILE* ftxt = fopen(txt_saida, "w");
    if (!fcsv || !ftxt) {
        perror("Erro ao abrir arquivos de saída");
        return 1;
    }

    fprintf(fcsv, "algoritmo,cenario,tempo_medio,desvio_tempo,comparacoes_medio,desvio_comp,memoria_MB");

    clock_t inicio = clock();
    Node* lista_nao_ord = NULL;
    for (int i = 0; i < tam; i++)
        lista_nao_ord = inserir_na_lista(lista_nao_ord, vetor[i]);
    clock_t fim = clock();
    double tempo_nao_ord = (double)(fim - inicio) / CLOCKS_PER_SEC;
    fprintf(stdout, "Tempo de criação da lista NÃO ordenada: %.6f s\n", tempo_nao_ord);
    fprintf(ftxt, "Tempo de criação da lista NÃO ordenada: %.6f s\n", tempo_nao_ord);
    imprimir_memoria("criação da lista NÃO ordenada", ftxt, fcsv);

    inicio = clock();
    Node* lista_ord = NULL;
    for (int i = 0; i < tam; i++)
        lista_ord = inserir_ordenado(lista_ord, vetor[i]);
    fim = clock();
    double tempo_ord = (double)(fim - inicio) / CLOCKS_PER_SEC;
    fprintf(stdout, "Tempo de criação da lista ORDENADA: %.6f s\n", tempo_ord);
    fprintf(ftxt, "Tempo de criação da lista ORDENADA: %.6f s\n", tempo_ord);
    imprimir_memoria("criação da lista ORDENADA", ftxt, fcsv);

    int tam_exist, tam_inexist;
    int* chaves_exist = carregar_chaves(argv[2], &tam_exist);
    int* chaves_inexist = carregar_chaves(argv[3], &tam_inexist);

    executar_testes_lista("NÃO ordenada (1000 EXISTENTES)", lista_nao_ord, chaves_exist, tam_exist, "Lista Encadeada", ftxt, fcsv);
    executar_testes_lista("NÃO ordenada (10 INEXISTENTES)", lista_nao_ord, chaves_inexist, tam_inexist, "Lista Encadeada", ftxt, fcsv);

    executar_testes_lista("ORDENADA (1000 EXISTENTES)", lista_ord, chaves_exist, tam_exist, "Lista Encadeada", ftxt, fcsv);
    executar_testes_lista("ORDENADA (10 INEXISTENTES)", lista_ord, chaves_inexist, tam_inexist, "Lista Encadeada", ftxt, fcsv);

    free(vetor);
    free(chaves_exist);
    free(chaves_inexist);
    fclose(ftxt);
    fclose(fcsv);
    return 0;
}
