#include "../include/math.hpp"

double math::exp(double x) {
    double xsqr = x * x;
    int n = (10 + (int) x) * 4 - 2;
    __float128 sum = n + 4;
    for ( ; n != 2; n -= 4)
        sum = n + xsqr / sum;

    return 1 + 2 * x / (2 - x + xsqr / sum);
}
