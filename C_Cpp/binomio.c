#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef long long int int_64;

int_64 factF(int_64 n, int_64 a);
int_64 fact(int_64 n);
int binomial(int n, int p);

int main() {
    int n, *v;
    char s;
    scanf(" %c %d", &s, &n);
    v = (int *) malloc((n + 1) / 2 * sizeof(int));

    for (int p = 0; p <= n; p++) {
        if (p <= n / 2) v[p] = binomial(n, p);
        if (v[n - p + (p <= n / 2) * (2 * p - n)] - 1) printf("%d * ", v[n - p + (p <= n / 2) * (2 * p - n)]);
        if (n - p) n - p - 1 ? printf("a ^ %d", n - p) : puts("a");
        if (n - p && p) puts(" * ");
        if (p) p - 1 ? printf("b ^ %d", p) : puts("b");
        if (p - n) s - 43 ? pow(-1, p) + 1 ? puts(" - ") : puts(" + ") : puts(" + ");
    }
    putchar('\n');
}

int_64 factF(int_64 n, int_64 a) {
    if (n == 0) return a;
    return factF(n - 1, n * a);
}

int_64 fact(int_64 n) {
    return factF(n, 1);
}

int binomial(int n, int p) {
    return fact((int_64)n) / (fact((int_64)p) * fact((int_64)(n - p)));
}
