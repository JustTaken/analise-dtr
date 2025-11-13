#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <string.h>
#include <math.h>
#include <PSO.h>
#include <vetor.h>

#define RNG_UNIFORM() (rand()/(float)RAND_MAX)

// Implementação das funções do PSO
const float w = 0.7298;
const float c1 = 0.5;
const float c2 = 0.5;

const float A_MIN = 0.0, A_MAX = 200.0;
const float B_MIN = 0.0, B_MAX = 200.0;

float func_objetivo(Ponto_float *dado, int n, float A, float B) {
    float err_total = 0.0;

    for (int i = 0; i < n; i++) {
        float y_previsto = A * exp(B * dado[i].x); // função fitness y(x(t)) = A · exp(B ·x(t))
        float err = dado[i].y - y_previsto;
        err_total += err * err;
    }
    
    float mse = err_total / n;
    return sqrt(mse);
}

void init_particula(Particula *p, float a_min, float a_max, float b_min, float b_max) {
    p->position[0] = a_min + (a_max - a_min) * RNG_UNIFORM();
    p->position[1] = b_min + (b_max - b_min) * RNG_UNIFORM();

    p->velocity[0] = (a_max - a_min) * (RNG_UNIFORM() - 0.5) / 10.0;
    p->velocity[1] = (b_max - b_min) * (RNG_UNIFORM() - 0.5) / 10.0;

    memcpy(p->best_position, p->position, sizeof(p->position));
    p->best_fitness = FLT_MAX;
}

void update_particula(Particula *p, float gbest[], float a_min, float a_max, float b_min, float b_max) {
    for(int i = 0; i < DIMENSOES; i++) {
        float r1 = RNG_UNIFORM();
        float r2 = RNG_UNIFORM();

        p->velocity[i] = w * p->velocity[i] 
                       + c1 * r1 * (p->best_position[i] - p->position[i])
                       + c2 * r2 * (gbest[i] - p->position[i]);

        p->position[i] += p->velocity[i];
    }

    p->position[0] = fmax(a_min, fmin(a_max, p->position[0]));
    p->position[1] = fmax(b_min, fmin(b_max, p->position[1]));
}

void exec_pso(Ponto_float *dados, int n_dados, float *melhor_A, float *melhor_B) {
    Particula particula[POPULACAO];
    float gbest_position[DIMENSOES];
    float gbest_fitness = FLT_MAX;

    for (int i = 0; i < POPULACAO; i++) {
        init_particula(&particula[i], A_MIN, A_MAX, B_MIN, B_MAX);
    }

    for (int iter = 0; iter < ITERACOES; iter++) {
        for (int i = 0; i < POPULACAO; i++) {
            float fitness_atual = func_objetivo(dados, n_dados, 
                              particula[i].position[0], 
                              particula[i].position[1]);

            if(fitness_atual < particula[i].best_fitness) {
                particula[i].best_fitness = fitness_atual;
                memcpy(particula[i].best_position, 
                       particula[i].position, 
                       sizeof(particula[i].position));
            }

            if(fitness_atual < gbest_fitness) {
                gbest_fitness = fitness_atual;
                memcpy(gbest_position, 
                       particula[i].position, 
                       sizeof(gbest_position));
            }

            update_particula(&particula[i], gbest_position, 
                           A_MIN, A_MAX, B_MIN, B_MAX);
        }
    }

    *melhor_A = gbest_position[0];
    *melhor_B = gbest_position[1];
}

void visualizar_dado(Vetor_float *dados, const char *filename) {
    FILE *gp = popen("gnuplot -persistent", "w");
    if(!gp){
        printf("\nGNUplot não encontrado. Imprimindo dado textualmente:\n");
        for (int i = 0; i < dados->quantidade; i++){
            vetor_imprimir_float(dados, "%f");
        }
        return;
    }

    fprintf(gp, "set title 'Dado %s'\n", filename);
    fprintf(gp, "set xlabel 'Tempo (s)'\n");
    fprintf(gp, "set ylabel 'Valor'\n");
    fprintf(gp, "set grid\n");
    fprintf(gp, "plot '-' with lines linewidth 2 title 'Dados'\n");

    for (int i = 0; i < dados->quantidade; i++){
        fprintf(gp, "%d %f\n", i, dados->item[i]);
    }
    fprintf(gp, "e\n");
    fflush(gp);
    pclose(gp);
}

void visualizar_dado_por_dado(Vetor_float *dado1, Vetor_float *dado2, const char *filename){
    FILE *gp = popen("gnuplot -persistent", "w");
    if(!gp){
        printf("\nGNUplot não encontrado. Imprimindo dado textualmente:\n");
        for (int i = 0; i < dado1->quantidade; i++){
            vetor_imprimir_float(dado1, "%f");
        }
        for (int i = 0; i < dado2->quantidade; i++){
            vetor_imprimir_float(dado2, "%f");
        }
        return;
    }

    fprintf(gp, "set title 'Dado %s'\n", filename);
    fprintf(gp, "set xlabel 'Dado1'\n");
    fprintf(gp, "set ylabel 'Dado2'\n");
    fprintf(gp, "set grid\n");
    fprintf(gp, "plot '-' with lines linewidth 2 title 'Dados'\n");

    for (int i = 0; i < dado1->quantidade; i++){
        fprintf(gp, "%f %f\n", dado1->item[i], dado2->item[i]);
    }
    fprintf(gp, "e\n");
    fflush(gp);
    pclose(gp);
}

void visualizar_ajuste_pso(Vetor_float *theta, Vetor_float *E_theta, float A, float B, const char *filename) {
    FILE *gp = popen("gnuplot -persistent", "w");
    if(!gp){
        printf("\nGNUplot não encontrado. Imprimindo dados textualmente:\n");
        printf("Dados originais (theta, E_theta):\n");
        for (int i = 0; i < theta->quantidade; i++){
            printf("(%f, %f)\n", theta->item[i], E_theta->item[i]);
        }
        printf("\nCurva ajustada: y = %f * exp(%f * x)\n", A, B);
        return;
    }

    fprintf(gp, "set title 'Ajuste PSO - %s'\n", filename);
    fprintf(gp, "set xlabel 'Theta'\n");
    fprintf(gp, "set ylabel 'E_Theta'\n");
    fprintf(gp, "set grid\n");
    
    // Plota os dados originais E a curva ajustada no mesmo gráfico
    fprintf(gp, "plot '-' with lines linewidth 2 title 'Dados Originais', ");
    fprintf(gp, "%f * exp(%f * x) with lines linewidth 2 title 'Curva Ajustada (y=%f*exp(%f*x))'\n", A, B, A, B);

    // Envia os dados originais para o gnuplot
    for (int i = 0; i < theta->quantidade; i++){
        fprintf(gp, "%f %f\n", theta->item[i], E_theta->item[i]);
    }
    fprintf(gp, "e\n");
    
    fflush(gp);
    pclose(gp);
}