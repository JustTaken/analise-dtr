#ifndef JANIOMATH_H_INCLUDED
#define JANIOMATH_H_INCLUDED

#include <stdlib.h>
#include <vetor.h>

float integra_concentracao(Vetor_float, float);
Vetor_float normaliza_concentracao(Vetor_float, float);
Vetor_float T_vezes_concentracao_normalizada(Vetor_float lista_e);
float integral_T_vezes_e(Vetor_float lista_te);
Vetor_float E_vezes_T_menos_Tmquadrado(Vetor_float lista_e, float integral_t_vezes_e);
float integra_funcao_anterior(Vetor_float lista_ite, float intervalo);
Vetor_float Theta(int quantidade_ou_capacidade_dos_vetores, float integral_t_vezes_e);
Vetor_float normaliza_Theta(Vetor_float lista_e, float integral_t_vezes_e);

#endif
