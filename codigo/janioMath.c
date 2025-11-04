#include <janioMath.h>

float integra(float data_A, float data_B, float intervalo){
    float s = 0.0;
    s = (data_A + data_B) * intervalo / 2.0;
    return s;
}

float normaliza(float data_A, float int_res){
    float s = 0.0;
    s = (data_A / int_res);
    return s;
}
