#pragma once

#include <stdlib.h>

void* vetor_realloc(void*, int, int);

#define VETOR(tipo) typedef struct {\
    int quantidade; \
    int capacidade; \
    tipo *items ;\
} Vetor_##tipo; \

#define VETOR_DECLARACAO(tipo) \
VETOR(tipo); \
Vetor_##tipo vetor_iniciar_##tipo(int); \
void vetor_adicionar_##tipo(Vetor_##tipo*, tipo); \

#define VETOR_IMPLEMENTACAO(tipo) \
Vetor_##tipo vetor_iniciar_##tipo(int capacidade) {\
    Vetor_##tipo vetor = {0, capacidade, malloc(sizeof(tipo) * capacidade) }; \
    return vetor; \
}\
void vetor_adicionar_##tipo(Vetor_##tipo *vetor, tipo item) {\
    if (vetor->capacidade <= vetor->quantidade) {\
        vetor->capacidade = vetor->capacidade * 2; \
        vetor_realloc(&vetor->items, sizeof(tipo), vetor->capacidade); \
    }\
    vetor->items[vetor->quantidade] = item; \
    vetor->quantidade += 1; \
}

VETOR_DECLARACAO(int);
VETOR_DECLARACAO(float);
