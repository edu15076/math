#include <cstdlib>

/**
 * Do an operation, <b>op</b>, that returns <b>T</b> <b>times</b> times with <b>n</b>.
 *
 * It has an complexity of log2(times)
 * @param n a type <b>T</b> variable.
 * @param times the number of times to execute <b>op</b>.
 * @param op the operation to be executed on <b>n</b> for <b>times</b> times. It must return the same type as <b>n</b>.
 * @param identity the value of type <b>T</b> that when operated with any other type <b>T</b> value does not change the latter.
 * @return <b>n</b> operated <b>times</b> times by <b>op</b>.
 */
double operate(const double n, const int times, double (*op)(double, double), const double identity) {
    if (!times)
        return identity;

    div_t divmod = div(times, 2);
    double result = operate(op(n, n), divmod.quot, op, identity);

    return divmod.rem ? op(result, n) : result;
}

double mult(double a, double b) { return a * b; }

double my_pow(const double base, const int power) {
    return operate(base, power, mult, 1);
}
