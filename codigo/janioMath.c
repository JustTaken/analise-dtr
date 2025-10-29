#include <janioMath.h>

float integra_concentracao(Vetor_float lista, float intervalo){
    float s = 0.0;

    for (int i = 0; i < lista.quantidade + 1; i++) {
        float atual = lista.items[i];
        float proximo = lista.items[i + 1];

        s += (atual + proximo) * intervalo / 2.0;
    }

    return s;
}

Vetor_float normaliza_concentracao(Vetor_float lista, float resultado_integral){
    float s = 0.0;
    Vetor_float lista_e = vetor_iniciar_float(lista.quantidade);

    for (int i = 0; i < lista.quantidade; i++) {
        float valor = lista.items[i];
        vetor_adicionar_float(&lista_e, valor / resultado_integral);
    }

    return lista_e;
}
