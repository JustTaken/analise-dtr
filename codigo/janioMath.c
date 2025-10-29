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
    Vetor_float lista_e = vetor_iniciar_float(lista.quantidade);

    for (int i = 0; i < lista.quantidade; i++) {
        float valor = lista.items[i];
        vetor_adicionar_float(&lista_e, valor / resultado_integral);
    }

    return lista_e;
}

Vetor_float T_vezes_concentracao_normalizada(Vetor_float lista_e){
    Vetor_float lista_te = vetor_iniciar_float(lista_e.quantidade);
    
    for (int i = 0; i < lista_e.quantidade; i++){
        float valor = lista_e.items[i];
        vetor_adicionar_float(&lista_te, valor * i);
    }
    
    return lista_te;
}

float integral_T_vezes_e(Vetor_float lista_te){
    float s = 0.0;

    for (int i = 0; i < lista_te.quantidade; i++){
        float atual = lista_te.items[i];
        float proximo = lista_te.items[i+1];

        s += (atual + proximo)/2.0;
    }
    
    return s;
}

Vetor_float E_vezes_T_menos_Tmquadrado(Vetor_float lista_e, float integral_t_vezes_e){
    Vetor_float lista_ite = vetor_iniciar_float(lista_e.quantidade);

    for (int i = 0; i < lista_e.quantidade; i++){
        float valor = lista_e.items[i];
        vetor_adicionar_float(&lista_ite, valor*((i-integral_t_vezes_e) * (i-integral_t_vezes_e)));
    }
    
    return lista_ite;
}

float integra_funcao_anterior(Vetor_float lista_ite, float intervalo){
    float s = 0.0;

    for (int i = 0; i < lista_ite.quantidade + 1; i++) {
        float atual = lista_ite.items[i];
        float proximo = lista_ite.items[i + 1];

        s += (atual + proximo) * intervalo / 2.0;
    }

    return s;
}

Vetor_float Theta(int quantidade_ou_capacidade_dos_vetores, float integral_t_vezes_e){
    Vetor_float lista_theta = vetor_iniciar_float(quantidade_ou_capacidade_dos_vetores);

    for (int i = 0; i < lista_theta.capacidade; i++){
        vetor_adicionar_float(&lista_theta, i/integral_t_vezes_e);
    }

    return lista_theta;
}

Vetor_float normaliza_Theta(Vetor_float lista_e, float integral_t_vezes_e){
    Vetor_float lista_Norma_theta = vetor_iniciar_float(lista_e.quantidade);

    for (int i = 0; i < lista_e.quantidade; i++){
        vetor_adicionar_float(&lista_Norma_theta, lista_e.items[i]*integral_t_vezes_e);
    }
    
    return lista_Norma_theta;
}