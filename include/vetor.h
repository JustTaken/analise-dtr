#pragma once

#include <stdio.h>
#include <stdlib.h>

// Macro para definir a estrutura do vetor para um tipo.
#define VETOR(tipo) \
typedef struct{     \
    int capacidade; \
    int quantidade; \
    tipo *item;     \
} Vetor_##tipo;

// Macro para declaração de todas as funções do vetor;
#define VETOR_DECLARACAO(tipo) \
VETOR(tipo);                   \
Vetor_##tipo vetor_iniciar_##tipo(int capacidade);                       \
void         vetor_realocar_##tipo(Vetor_##tipo *vetor, int capacidade); \
void         vetor_adicionar_##tipo(Vetor_##tipo *vetor, tipo item);     \
void         vetor_liberar_##tipo(Vetor_##tipo *vetor);                  \
void         vetor_definir_##tipo(Vetor_##tipo *vetor, int indice, tipo item); \
void         vetor_imprimir_##tipo(Vetor_##tipo *vetor, const char *formato);

VETOR_DECLARACAO(char);
VETOR_DECLARACAO(int);
VETOR_DECLARACAO(float);
VETOR_DECLARACAO(double);
