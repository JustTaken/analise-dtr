#ifndef LISTA_H_INCLUDED
#define LISTA_H_INCLUDED

#include <stdio.h>

typedef struct nodo{
    float valor_conc; // Valor da concentração
    struct nodo *proximo; // Ponteiro para o próximo espaço
} Nodo;

void inserir_nodo(Nodo **lista, float num);
void imprimir_lista(Nodo *lista);
void liberar_lista(Nodo *lista);

#endif // LISTA_H_INCLUDED
