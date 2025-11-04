#include <vetor.h>

// Macro para a implementação de todas as funções do vetor;
#define VETOR_IMPLEMENTACAO(tipo) \
Vetor_##tipo vetor_iniciar_##tipo(int capacidade){  \
    Vetor_##tipo vetor;                             \
    vetor.capacidade = capacidade;                  \
    vetor.quantidade = 0;                           \
    vetor.item = malloc(capacidade * sizeof(tipo)); \
    if(!vetor.item){                                \
        fprintf(stderr, "Erro: Falha ao alocar memoria!\n");\
        exit(EXIT_FAILURE);                         \
    }                                               \
    return vetor;                                   \
} \
void vetor_realocar_##tipo(Vetor_##tipo *vetor, int nova_capacidade){   \
    tipo *temp = realloc(vetor->item, nova_capacidade * sizeof(tipo));  \
    if (!temp){                                                         \
        fprintf(stderr, "Erro: Falha ao realocar memoria!\n");          \
        exit(EXIT_FAILURE);                                             \
    }                                                                   \
    vetor->item = temp;                                                 \
    vetor->capacidade = nova_capacidade;                                \
} \
void vetor_adicionar_##tipo(Vetor_##tipo *vetor, tipo item){    \
    if(vetor->quantidade >= vetor->capacidade){                 \
        int nova_capacidade = vetor->capacidade * 2;            \
        vetor_realocar_##tipo(vetor, nova_capacidade);          \
    }                                                           \
    vetor->item[vetor->quantidade] = item;                      \
    vetor->quantidade++;                                        \
} \
void vetor_liberar_##tipo(Vetor_##tipo *vetor){ \
    free(vetor->item);                          \
    vetor->item = NULL;                         \
    vetor->capacidade = 0;                      \
    vetor->quantidade = 0;                      \
} \
void vetor_definir_##tipo(Vetor_##tipo *vetor, int indice, tipo item){  \
    if(indice >= 0 && indice < vetor->quantidade){                      \
        vetor->item[indice] = item;                                     \
    } \
} \
void vetor_imprimir_##tipo(Vetor_##tipo *vetor, const char *formato){ \
    printf("[");                                                      \
    for(int i = 0; i < vetor->quantidade; i++){                       \
        printf(formato, vetor->item[i]);                              \
        if(i < vetor->quantidade - 1) printf(", ");                   \
    }                                                                 \
    printf("]\n");                                                    \
}

// Implementa as funções para os tipos declarados no .h
VETOR_IMPLEMENTACAO(char);
VETOR_IMPLEMENTACAO(int);
VETOR_IMPLEMENTACAO(float);
VETOR_IMPLEMENTACAO(double);