#include <stdio.h>
int main(void) {
    float a[1000];
    #pragma acc parallel loop copyout(a[0:1000])
    for (int i = 0; i < 1000; ++i) a[i] = 2.0f * i;
    for (int i = 0; i < 1000; ++i)
        if (a[i] != 2.0f * i) return 1;
    puts("PASS");
    return 0;
}
