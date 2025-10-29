#include <vetor.h>

void* vetor_realloc(void *ptr, int size, int capacidade) {
  free(ptr);

  return malloc(size * capacidade);
}

VETOR_IMPLEMENTACAO(int)
VETOR_IMPLEMENTACAO(float)
