#include <stdio.h>
#include <stdlib.h>
#include <lista.h>

void inserir_nodo(Nodo **lista, float num){
    Nodo *aux, *novo = malloc(sizeof(Nodo));

    if(novo){
        novo->valor_conc = num;
        novo->proximo = NULL;

        if(*lista == NULL)
            *lista = novo;
        else{
            aux = *lista;
            while (aux->proximo)
                aux = aux->proximo;
            aux->proximo = novo;
        }
    }
    else
        printf("Erro de alocação de memoria!\n");
}
void imprimir_lista(Nodo *lista){
    printf("\n\tLista: ");
    while(lista){
        printf("%f ", lista->valor_conc);
        lista = lista->proximo;
    }
    printf("\n\n");
}

void liberar_lista(Nodo *lista){
    Nodo *aux;
    while(lista != NULL){
        aux = lista;
        lista = lista->proximo;
        free(aux);
    }
}
