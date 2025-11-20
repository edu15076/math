#include <iostream>
#include <string>
#include <math.hpp>
#include <cstdint>

#define _ std::ios::sync_with_stdio(false); std::cin.tie(NULL); std::cout.tie(NULL);
#define dbg(x) cout << #x << " = " << x << endl
#define endl "\n"

void playExp() {
    double n; std::cin >> n;
    std::cout << "e^" << n << " = " << math::exp(n) << endl;
}

void playPow() {
    std::cout << "Type a double for the base: ";
    double b;
    std::cout << endl << "Type a unsigned short for the exponent: ";
    std::uint16_t e;
    std::cout << endl;
    std::cin >> b >> e;
    std::cout << b << "^" << e << " = " << math::pow(b, e) << endl;
}

void playPrime() {
    std::cout << "Type a integer number: ";
    int64_t n;
    if (!(std::cin >> n))
        return;
    math::PrimeUtils<int64_t> primeUtils;

    std::cout << n << " is: " << (primeUtils.isPrime(n) ? "prime" : "composite") << endl;
    auto& factorsOfN = primeUtils.factors(n);
    std::cout << n << " = " << primeUtils.factorsToString(factorsOfN) << endl;
    delete& factorsOfN;
}

int main() { _
    std::string play;
    std::cout << "Chose what playground you want to go by its name: "; std::cin >> play;

    if (play == "exp")
        playExp();
    else if (play == "pow")
        playPow();
    else
        playPrime();
    
    return 0;
}
