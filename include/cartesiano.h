#ifndef CARTESIANO_H_INCLUDED
#define CARTESIANO_H_INCLUDED

// Macro para declarar a estrutura do ponto
#define CARTESIANO(tipo) \
typedef struct {         \
    tipo x;              \
    tipo y;              \
} Ponto_##tipo;

// Macro para declarar as funções de cada tipo
#define CARTESIANO_DECLARACAO(tipo)          \
CARTESIANO(tipo)                             \
Ponto_##tipo set_ponto_##tipo(tipo x, tipo y); \
void get_ponto_##tipo(Ponto_##tipo p, tipo *x, tipo *y);

// Declara estruturas e funções para int, float e double
CARTESIANO_DECLARACAO(int)
CARTESIANO_DECLARACAO(float)
CARTESIANO_DECLARACAO(double)

#endif // CARTESIANO_H_INCLUDED