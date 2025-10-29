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

// --- Hiperparâmetros do PSO ---
const float w = 0.5;    // inércia
const float c1 = 0.5;   // coeficiente cognitivo (peso do Pbest)
const float c2 = 0.5;   // coeficiente social (peso do Gbest)

// --- Parâmetros de busca (limites) ---
const float A_MIN = 0.0, A_MAX = 200.0; // Normalmente usado em um problema ao estilo de um mapa topográfico com vários pontos máximo e mínimos em Z apesar de representar um plano x e y
const float B_MIN = 0.0, B_MAX = 200.0; // No entanto, como o algoritmo não será usado para um problema em um perfil topográfico, a delimitação e a análise dos valores sempre será > 0

// int main() {
//     Vetor_int vetor = vetor_iniciar_int(10);
//     vetor_adicionar_int(&vetor, 10);
//     return 0;
// }

Vetor_float ler_csv(const char* nome) {
    char BUFFER[256];         // Vetor de 256 bytes para armazenar string
    char *data_read;          // Ponteiro para um dado específico do arquivo .csv
    FILE *fptr;               // Ponteiro de manipulação de arquivo
    Vetor_float lista = vetor_iniciar_float(20);

    fptr = fopen(nome, "r"); /*A função para abrir o arquivo recebe dois parâmetros, o diretório do arquivo a ser aberto e o modo que ele será trabalhado:
        w - Grava em um arquivo
        a - Adiciona novos dados em um arquivo
        r - Lê um arquivo
        rb- Lê em binário        */

    if (fptr == NULL){
        printf("Nao ha arquivo o especificado\n");
        exit(1);
    }

    for (int i = 0; i < 7; i++){ // Ignore as primeiras 7 linhas do arquivo .csv
        void* ptr = fgets(BUFFER, sizeof(BUFFER), fptr);
    }

    while (fgets(BUFFER, sizeof(BUFFER), fptr)){ // Loop de leitura do arquivo .csv começando da linha 8 até o fim
        BUFFER[strlen(BUFFER)-1] = '\0'; // Trunca o arquivo para ele não haver salto de linha por linha por caracter invisível
        printf("%s\n", BUFFER);

        data_read = strtok(BUFFER, ","); // Aponta o data_read para ler a primeira coluna da linha do arquivo armazenado no buffer
        for (int i = 1; i < 4; i++){ // Aponte o data_read para ler os dados da quarta coluna da linha previamente carregado nele do buffer
            data_read = strtok(NULL, ",");
        }

        float valor = atof(data_read);
        vetor_adicionar_float(&lista, valor);

        // inserir_nodo(&lista, ); // Inseri o valor extraido de string para float em uma lista simples encadeada de valores de concentração
        printf("extraido: %s\n", data_read);
    }

    float integral_concentracao = integra_concentracao(lista, 1.0);
    Vetor_float lista_e = normaliza_concentracao(lista, integral_concentracao);

    // tmp_integral = integra_concentracao(lista, 1.0);
    // printf("integral: %f", tmp_integral);

    // imprimir_lista(lista);
    // liberar_lista(lista);

    fclose(fptr);

    return lista;
}

int main(int argc, char *argv[]){
    char *nome = argv[1]; // Argumento string do caminho para o arquivo a ser lido fornecido
    // Nodo *lista = NULL;  // Ponteiro para alocação dinâmica dos valores extraidos do arquivo .csv
    // float tmp_integral;

    Vetor_float lista = ler_csv(nome);

    return 0;
}
