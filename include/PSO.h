#ifndef PSO_H_INCLUDED
#define PSO_H_INCLUDED

#include <janioMath.h>
#include <cartesiano.h>
#include <vetor.h>

#define DIMENSOES 2
#define ITERACOES 200
#define POPULACAO 20

typedef struct {
    float position[DIMENSOES];
    float velocity[DIMENSOES];
    float best_position[DIMENSOES];
    float best_fitness;
} Particula;

// Hiperparâmetros do PSO
extern const float w;
extern const float c1;
extern const float c2;

// Parâmetros de busca
extern const float A_MIN, A_MAX;
extern const float B_MIN, B_MAX;

// Declarações das funções
float func_objetivo(Ponto_float *dado, int n, float A, float B);
void init_particula(Particula *p, float a_min, float a_max, float b_min, float b_max);
void update_particula(Particula *p, float gbest[], float a_min, float a_max, float b_min, float b_max);
void exec_pso(Ponto_float *dados, int n_dados, float *melhor_A, float *melhor_B);
void visualizar_dado(Vetor_float *dados, const char *filename);
void visualizar_dado_por_dado(Vetor_float *dado1, Vetor_float *dado2, const char *filename);
void visualizar_ajuste_pso(Vetor_float *theta, Vetor_float *E_theta, float A, float B, const char *filename);

#endif // PSO_H_INCUDED