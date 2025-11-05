#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <string.h>
#include <lista.h>
#include <janioMath.h>
#include <vetor.h>

#define RNG_UNIFORM() (rand()/(double)RAND_MAX) // Gera valor entre 0 e 1
#define DIMENSOES 2     // Quantidade de variáveis no problema para ser analisado
#define ITERACOES 200   // Quantidade de loops que o algoritmo executará até encontrar solução
#define POPULACAO 20    // Quantidade de partículas de busca do algoritmo

typedef struct{
    float *position;
    float *velocity;
    float *pBest_position;
    float pBest_fitness;
} Particula;

// --- Hiperparâmetros do PSO ---
const float w = 0.7298;    // inércia
const float c1 = 0.5;   // coeficiente cognitivo (peso do Pbest)
const float c2 = 0.5;   // coeficiente social (peso do Gbest)

// --- Parâmetros de busca (limites) ---
const float A_MIN = 0.0, A_MAX = 200.0; // Normalmente usado em um problema ao estilo de um mapa topográfico com vários pontos máximo e mínimos em Z apesar de representar um plano x e y
const float B_MIN = 0.0, B_MAX = 200.0; // No entanto, como o algoritmo não será usado para um problema em um perfil topográfico, a delimitação e a análise dos valores sempre será > 0


int main(int argc, char *argv[]){
    char *arquivo = argv[1];  // Argumento string do caminho para o arquivo a ser lido fornecido
    char BUFFER[256];         // Vetor de 256 bytes para armazenar string
    char *data_read;          // Ponteiro para um dado específico do arquivo .csv
    FILE *fptr;               // Ponteiro de manipulação de arquivo
    Vetor_float concentracao = vetor_iniciar_float(2);// Uma lista alocada dinamicamente com a biblioteca vetor.h
    srand(time(NULL)); // Inicializa uma seed aleatória
    
    

    fptr = fopen(arquivo, "r"); /*A função para abrir o arquivo recebe dois parâmetros, o diretório do arquivo a ser aberto e o modo que ele será trabalhado:
        w - Grava em um arquivo (escrita)
        a - Adiciona novos dados em um arquivo (anexa)
        r - Lê um arquivo       (leitura)
        r+ - Leitura e escrita
        w+ - Leitura e escrita (apaga o conteúdo caso o arquivo já exista)
        a+ - Leitura e escrita (adiciona ao final do arquivo)
        rb- Lê em binário        */

    if (!fptr){
        printf("Nao ha arquivo o especificado\n");
        exit(1);
    }

    for (int i = 0; i < 7; i++){ // Ignore as primeiras 7 linhas do arquivo .csv
        fgets(BUFFER, sizeof(BUFFER), fptr);
    }

    while (fgets(BUFFER, sizeof(BUFFER), fptr)){ // Loop de leitura do arquivo .csv começando da linha 8 até o fim
        BUFFER[strlen(BUFFER)-1] = '\0'; // Trunca o arquivo para ele não haver salto de linha por linha por caracter invisível
        printf("%s\n", BUFFER);

        data_read = strtok(BUFFER, ","); // Aponta o data_read para ler a primeira coluna da linha do arquivo armazenado no buffer
        for (int i = 1; i < 4; i++){ // Aponte o data_read para ler os dados da quarta coluna da linha previamente carregado nele do buffer
            data_read = strtok(NULL, ",");
        }

        vetor_adicionar_float(&concentracao, atof(data_read));
    }

    // Passos matematicos para até o theta
    // 1. Int ｩ
    float integral_concentracao = 0.0;
    for (int i = 0; i < concentracao.quantidade; i++){
        integral_concentracao += integra_float(concentracao.item[i], concentracao.item[i+1], 1.0);
    }

    // 2. E
    Vetor_float E_normalizado = vetor_iniciar_float(concentracao.quantidade);
    for(int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&E_normalizado, normaliza_float(concentracao.item[i], integral_concentracao));
    }
    
    // 3. T*E
    Vetor_float T_E = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&T_E, (i * E_normalizado.item[i]));
    }

    // 4. int(T*E)
    float integral_T_E = 0.0;
    for (int i = 0; i < concentracao.quantidade; i++){
        integral_T_E += integra_float(T_E.item[i], T_E.item[i+1], 1.0);
    }
    
    // 5. Theta
    Vetor_float theta = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&theta, (i / integral_T_E));
    }

    // 6. E(Theta)
    Vetor_float E_theta = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&E_theta, (E_normalizado.item[i] * integral_T_E));
    }
        

    vetor_liberar_float(&concentracao);
    vetor_liberar_float(&E_normalizado);
    vetor_liberar_float(&T_E);
    vetor_liberar_float(&theta);
    vetor_liberar_float(&E_theta);
    fclose(fptr);
    return 0;
}
