#include "../include/math.hpp"
#include <sstream>

template<typename I, typename IS_INTEGRAL>
I math::PrimeUtils<I, IS_INTEGRAL>::firstDivisor(I n) {
    n = n <= 0 ? -n : n;
    return n > 1 ? mFirstDivisor(n) : 0;
}

template<typename I, typename IS_INTEGRAL>
bool math::PrimeUtils<I, IS_INTEGRAL>::isPrime(I n) {
    return n > 1 && (n < 4 || (n & 1 && n % 3 && mIsPrime(n)));
}

template<typename I, typename IS_INTEGRAL>
std::map<I, uint16_t>& math::PrimeUtils<I, IS_INTEGRAL>::factors(I n, std::map<I, uint16_t>& factorsOfN) {
    n = n <= 0 ? -n : n; // The factors of a negative integer is the same of its inverse
    return n > 1 ? mFactors(n, factorsOfN) : factorsOfN;
}

template<typename I, typename IS_INTEGRAL>
std::map<I, uint16_t>& math::PrimeUtils<I, IS_INTEGRAL>::factors(I n) {
    return factors(n, *(new std::map<I, uint16_t>()));
}

template<typename I, typename IS_INTEGRAL>
std::string math::PrimeUtils<I, IS_INTEGRAL>::factorsToString(std::map<I, uint16_t>& f) {
    std::stringstream s;
    for (auto& [prime, power] : f)
        s << to_string(prime) << (power == 1 ? " * " : ("^" + to_string(power) + " * "));
    std::string str = s.str();
    return str.substr(0, str.length() - 3);
}

template<typename I, typename IS_INTEGRAL>
I math::PrimeUtils<I, IS_INTEGRAL>::mFirstDivisor(I n) {
    if (!(n & 1))
        return 2;

    if (!(n % 3))
        return 3;

    // if this variable is false we assume we're at the number next to a multiple of six
    bool isBeforeMultipleOfSix {true};
    for (I i {5}; i * i <= n; i += isBeforeMultipleOfSix ? 2 : 4, isBeforeMultipleOfSix = !isBeforeMultipleOfSix)
        if (!(n % i))
            return i;

    return n;
}

template<typename I, typename IS_INTEGRAL>
bool math::PrimeUtils<I, IS_INTEGRAL>::mIsPrime(I n) {
    return mFirstDivisor(n) == n;
}

template<typename I, typename IS_INTEGRAL>
std::map<I, uint16_t>& math::PrimeUtils<I, IS_INTEGRAL>::mFactors(I n, std::map<I, uint16_t>& factorsOfN) {
    do {
        I firstDivisorN = firstDivisor(n);
        if (!factorsOfN.contains(firstDivisorN))
            factorsOfN[firstDivisorN] = 1;
        else
            factorsOfN[firstDivisorN]++;
        n /= firstDivisorN;
    } while (n != 1);

    return factorsOfN;
}
