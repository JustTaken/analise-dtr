#ifndef JANIOMATH_H_INCLUDED
#define JANIOMATH_H_INCLUDED

#define JANIO_MATH_DECL(tipo) \
tipo integra_##tipo(tipo data_A, tipo data_B, tipo intervalo); \
tipo normaliza_##tipo(tipo data_A, tipo int_res);               \


JANIO_MATH_DECL(int)
JANIO_MATH_DECL(float)
JANIO_MATH_DECL(double)


#endif // JANIOMATH_H_INCLUDED
