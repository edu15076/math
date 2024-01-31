#include "../include/math.hpp"
#include <cstdlib>

double math::operate(const double n, const unsigned times, std::function<double (double, double)>& op, const double identity) {
    if (!times)
        return identity;

    div_t divmod = div(times, 2);
    double result = operate(op(n, n), divmod.quot, op, identity);

    return divmod.rem ? op(result, n) : result;
}

double math::pow(const double base, const unsigned short exponent) {
    std::function<double (double, double)> multiply {[](double a, double b) { return a * b; }};
    return operate(base, exponent, multiply, 1);
}
