#include "cartesiano.h"

// Implementação para int
Ponto_int set_ponto_int(int x, int y) {
    Ponto_int tmp;
    tmp.x = x;
    tmp.y = y;
    return tmp;
}

void get_ponto_int(Ponto_int p, int *x, int *y) {
    if (x) *x = p.x;
    if (y) *y = p.y;
}

// Implementação para float
Ponto_float set_ponto_float(float x, float y) {
    Ponto_float tmp;
    tmp.x = x;
    tmp.y = y;
    return tmp;
}

void get_ponto_float(Ponto_float p, float *x, float *y) {
    if (x) *x = p.x;
    if (y) *y = p.y;
}

// Implementação para double
Ponto_double set_ponto_double(double x, double y) {
    Ponto_double tmp;
    tmp.x = x;
    tmp.y = y;
    return tmp;
}

void get_ponto_double(Ponto_double p, double *x, double *y) {
    if (x) *x = p.x;
    if (y) *y = p.y;
}