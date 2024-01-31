#ifndef MATH_MATH_HPP
#define MATH_MATH_HPP

#include <functional>
#include <type_traits>
#include <cstdint>
#include <map>
#include <string>

namespace math {
    /**
     * This function elevates <b>e</b> to the <b>x</b> with extreme precision. It's good to alert that a normal <b>pow()</b>
     * function may be faster but less precise.<br>
     *
     * This method is defined in Continued Fractions, Vol. 1: Convergence Theory. From: Lisa Lorentzen and Haakon Waadeland.
     * @param x the number to elevate <b>e</b>.
     * @return <b>e</b> to the power of <b>x</b>.
     */
    double exp(double x);

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
    double operate(double n, unsigned times, std::function<double (double, double)>& op, double identity);

    /**
     * Do <b>base</b> to the power of <b>exponent</b>.
     * @param base The base.
     * @param exponent The exponent.
     * @return The <b>base</b> to the power of the <b>exponent</b>.
     */
    double pow(double base, unsigned short exponent);

    template<typename I = unsigned, typename = typename std::enable_if<std::is_integral<I>::value, bool>::type>
    class PrimeUtils {
        public:
        /**
         * Gives the first divisor of n greater than 1.
         * If n == 0 or n == 1 or n == -1, if signed, then the return is 0.
         */
        I firstDivisor(I n);

        /**
         * Whether n is prime or not.
         * @param n The number to check if it is prime.
         * @return true if n is prime, else false.
         */
        bool isPrime(I n);

        std::map<I, uint16_t>& factors(I n, std::map<I, uint16_t>& factorsOfN);

        /**
         * Create a map in the heap with the prime factors of n to their power, the return of that method should be deleted&
         * @param n The number to get the factor
         * @return A map of the prime factor to their power
         */
        std::map<I, uint16_t>& factors(I n);

        std::string factorsToString(std::map<I, uint16_t>& f);

        private:
        I mFirstDivisor(I n);

        bool mIsPrime(I n);

        /**
         * Should assert n > 1, if it is negative should be inverted
         */
        std::map<I, uint16_t>& mFactors(I n, std::map<I, uint16_t>& factorsOfN);
    };
}

#endif //MATH_MATH_HPP
