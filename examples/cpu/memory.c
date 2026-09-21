#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const size_t n = 1u << 24;
    double *a = malloc(n * sizeof(*a));
    if (!a) return 2;
    for (size_t i = 0; i < n; ++i) a[i] = 1.0;
    for (size_t stride = 1; stride <= 64; stride *= 8) {
        double sum = 0.0;
        double start = omp_get_wtime();
        for (int repeat = 0; repeat < 8; ++repeat)
            for (size_t i = 0; i < n; i += stride) sum += a[i];
        double seconds = omp_get_wtime() - start;
        size_t visits = 8 * ((n + stride - 1) / stride);
        if (sum != (double)visits) return 1;
        printf("stride=%zu visits=%zu ns_per_element=%.3f useful_GBps=%.3f PASS\n",
               stride, visits, seconds * 1e9 / visits, visits * sizeof(double) / seconds / 1e9);
    }
    free(a);
    return 0;
}
