#include <stdlib.h>
#include "lista.h"

float integra_concentracao(Nodo *lista, float intervalo){
    if(!lista){
        printf("LISTA VAZIA PARA INTEGRACAO, RETORNANDO 0");
        return 0.0;
    }

    float s = 0.0;
    Nodo *atual = lista;
    Nodo *proximo = lista->proximo;

    while (proximo != NULL){
        s += (atual->valor_conc + proximo->valor_conc) * intervalo / 2.0;
        atual = proximo;
        proximo = proximo->proximo;
    }
    return s;
}



float normaliza_concentracao(Nodo *lista, float resultado_integral){
    if(!lista){
        printf("LISTA VAZIA PARA NORMALIZACAO, RETORNANDO 0");
        return 0.0;
    }

    float s = 0.0;
    Nodo *atual = lista;
    Nodo *proximo = lista->proximo;

    while (proximo != NULL){
        s += (atual->valor_conc/resultado_integral);
        atual = proximo;
        proximo = proximo->proximo;
    }
    return s;
}
