#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <string.h>
#include <math.h>
#include <lista.h>
#include <janioMath.h>
#include <vetor.h>
#include <cartesiano.h>
#include <PSO.h>

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
        for (int i = 1; i < 1; i++){ // Aponte o data_read para ler os dados da x coluna em 'i < x' da linha previamente carregado nele do buffer
            data_read = strtok(NULL, ",");
        }

        vetor_adicionar_float(&concentracao, atof(data_read));
    }
    fclose(fptr);
    vetor_imprimir_float(&concentracao, "%f");
    visualizar_dado(&concentracao, "concentracao");
    

    // vetor concentração logatirimizado
    Vetor_float ln_concentracao = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&ln_concentracao, ln_float(concentracao.item[i]));
    }
    vetor_imprimir_float(&ln_concentracao, "%f");
    visualizar_dado(&ln_concentracao, "concentracao logaritmizado");

    // Passos matematicos para até o theta
    // 1. Int ｩ
    float integral_concentracao = 0.0;
    for (int i = 0; i < concentracao.quantidade - 1; i++){
        integral_concentracao += integra_float(concentracao.item[i], concentracao.item[i+1], 1.0);
    }
    // printf("integral_concentracao: %f\n", integral_concentracao);

    // 2. E
    Vetor_float E_normalizado = vetor_iniciar_float(concentracao.quantidade);
    for(int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&E_normalizado, normaliza_float(concentracao.item[i], integral_concentracao));
    }
    // vetor_imprimir_float(&E_normalizado, "%f");
    
    // 3. T*E
    Vetor_float T_E = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&T_E, (i * E_normalizado.item[i]));
    }
    // vetor_imprimir_float(&T_E, "%f");

    // 4. int(T*E)
    float integral_T_E = 0.0;
    for (int i = 0; i < concentracao.quantidade - 1; i++){
        integral_T_E += integra_float(T_E.item[i], T_E.item[i+1], 1.0);
    }
    // printf("integral_T_E: %f\n", integral_T_E);
    
    // 5. Theta
    Vetor_float theta = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&theta, (i / integral_T_E));
    }
    // vetor_imprimir_float(&theta, "%f");

    // 6. E(Theta)
    Vetor_float E_theta = vetor_iniciar_float(concentracao.quantidade);
    for (int i = 0; i < concentracao.quantidade; i++){
        vetor_adicionar_float(&E_theta, (E_normalizado.item[i] * integral_T_E));
    }
    // vetor_imprimir_float(&E_theta, "%f");

    // Gravar os dados
    fptr = fopen("dados.csv", "w");
    
    if(!fptr){
        printf("Erro ao abrir o dados.csv\n");
        exit(1);
    }

    fprintf(fptr, "Theta,E_theta\n"); // Monta o cabeçalho primeiro
    for (int i = 0; i < theta.quantidade; i++){
        fprintf(fptr, "%f,%f\n", theta.item[i], E_theta.item[i]);
    }
    
    fclose(fptr);

    visualizar_dado_por_dado(&theta, &E_theta, "Grafico de theta por E_theta");

    // PSO
    float melhor_A, melhor_B;
    Ponto_float *dados_do_pso = malloc(theta.quantidade * sizeof(Ponto_float));
    for (int i = 0; i < theta.quantidade; i++){
        dados_do_pso[i] = set_ponto_float(theta.item[i], E_theta.item[i]);
    }
    exec_pso(dados_do_pso, theta.quantidade, &melhor_A, &melhor_B);
    printf("melhor A: %f. Melhor B: %f", melhor_A, melhor_B);
    visualizar_ajuste_pso(&theta, &E_theta, melhor_A, melhor_B, "Ajuste PSO - Dados vs Modelo");
    
    
    vetor_liberar_float(&concentracao);
    vetor_liberar_float(&E_normalizado);
    vetor_liberar_float(&T_E);
    vetor_liberar_float(&theta);
    vetor_liberar_float(&E_theta);
    free(dados_do_pso);
    return 0;
}