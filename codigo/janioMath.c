#include <janioMath.h>

// Macro para implementação das funções para cada tipo
#define JANIO_MATH_IMPL(tipo) \
tipo integra_##tipo(tipo data_A, tipo data_B, tipo intervalo) { \
    return (data_A + data_B) * intervalo / 2.0f; \
} \
tipo normaliza_##tipo(tipo data_A, tipo int_res) { \
    return data_A / int_res; \
}

// Implementa as funções para cada tipo
JANIO_MATH_IMPL(int)
JANIO_MATH_IMPL(float)
JANIO_MATH_IMPL(double)