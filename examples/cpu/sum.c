#include <errno.h>
#include <inttypes.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char *end = NULL;
    errno = 0;
    long n = argc > 1 ? strtol(argv[1], &end, 10) : 10000000;
    if (errno || (argc > 1 && (!*argv[1] || *end)) || n < 1 || n > 100000000) {
        fprintf(stderr, "n must be an integer in [1, 100000000]\n");
        return 2;
    }
    uint64_t *a = malloc((size_t)n * sizeof(*a));
    if (!a) return 2;
    for (long i = 0; i < n; ++i) a[i] = (uint64_t)i;
    uint64_t sum = 0;
    double start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(static)
    for (long i = 0; i < n; ++i) sum += a[i];
    double elapsed = omp_get_wtime() - start;
    uint64_t expected = (uint64_t)n * (n - 1) / 2;
    printf("threads_max=%d n=%ld sum=%" PRIu64 " seconds=%.9f %s\n",
           omp_get_max_threads(), n, sum, elapsed, sum == expected ? "PASS" : "FAIL");
    free(a);
    return sum != expected;
}
