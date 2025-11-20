from decimal import Decimal
from fractions import Fraction

from .util import lowest_prime_factor


class NotDivisibleError(RuntimeError):
    pass


class Factors:
    def __init__(self, n: 'int | Factors') -> None:
        if isinstance(n, int):
            self._n = self._factorize(n)
        else:
            self._n = n._n.copy()

    @classmethod
    def _factorize(cls, n: int) -> dict[int, int]:
        prime_factors = {}
        low = 2

        while n != 1:
            low = lowest_prime_factor(n, low)
            prime_factors[low] = 1
            n //= low
            while not n % low:
                prime_factors[low] += 1
                n //= low

        return prime_factors

    def __int__(self):
        n = 1
        for p, e in self._n.items():
            n *= p ** e
        return n

    def __repr__(self):
        s = ''
        for p, e in self._n.items():
            s += f'{p}^{e}' if e != 1 else str(p)
            s += ' * '
        return s[:-3]

    def __str__(self):
        return f'{int(self)} = {repr(self)}'

    def __iter__(self):
        return iter(self._n)

    def __getitem__(self, item):
        return self._n[item]

    def __setitem__(self, key, value):
        self._n[key] = value

    def __contains__(self, item):
        return item in self._n

    def copy(self):
        n = Factors(1)
        n._n.update(self._n)
        return n

    @property
    def number_of_factors(self):
        num = 1
        for p, e in self._n.items():
            num *= e + 1
        return num

    @property
    def all_factors(self):
        factors = [1]

        for p, e in self._n.items():
            factors_p = []

            p_exp = p
            for i in range(1, e + 1):
                factors_p.append(p_exp)
                p_exp *= p

            for i in range(len(factors)):
                for factor in factors_p:
                    factors.append(factors[i] * factor)

        return factors

    @property
    def factors_sum(self):
        s = 1
        for p, e in self._n.items():
            s *= (p ** (e + 1) - 1) // (p - 1)
        return s

    @property
    def factors_product(self):
        return self ** (self.number_of_factors / 2)
    # produtorio S = n!/n^((produtorio e_i+1)/2)

    def prime_factors(self):
        return list(self._n.keys())

    def prime_factors_to_exponents(self):
        return self._n.copy()

    def __mul__(self, other: 'int | Factors') -> 'Factors':
        if isinstance(other, int):
            other = Factors(other)
        return self._mul(self.copy(), other)

    def __imul__(self, other: 'int | Factors') -> None:
        if isinstance(other, int):
            other = Factors(other)
        self._mul(self, other)

    def __div__(self, other: 'int | Factors') -> 'Factors':
        if isinstance(other, int):
            other = Factors(other)
        return self._div(self.copy(), other)

    def __idiv__(self, other: 'int | Factors') -> None:
        if isinstance(other, int):
            other = Factors(other)
        self._div(self, other)

    def __pow__(self, other: 'int | float | Fraction | Decimal | Factors') -> 'Factors':
        p = q = 1
        if isinstance(other, float) or isinstance(other, Fraction):
            other = Fraction(other)
        if isinstance(other, Fraction):
            p = other.numerator
            q = other.denominator
        elif isinstance(other, Factors) or isinstance(other, int):
            p = int(other)
        if not p:
            return Factors(1)
        if q == 1:
            return self._pow(self.copy(), p)
        return self._pow(self._root(self.copy(), q), p)

    def __rpow__(self, other):
        return other ** int(self)

    def __eq__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return int(self) == other

    def __ne__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return int(self) != other

    def __gt__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return int(self) > other

    def __ge__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return self > other or self == other

    def __lt__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return not self <= other

    def __le__(self, other: 'int | float | Fraction | Decimal | Factors') -> bool:
        return not self > other

    @classmethod
    def _mul(cls, n: 'Factors', m: 'Factors') -> 'Factors':
        for p, e in m._n.items():
            if p in n:
                n[p] += e
            else:
                n[p] = e

        return n

    @classmethod
    def _div(cls, n: 'Factors', m: 'Factors') -> 'Factors':
        for p, e in m._n.items():
            if p not in n or n[p] < e:
                raise NotDivisibleError
            n[p] -= e
            if not n[p]:
                del n._n[p]

        return n

    @classmethod
    def _pow(cls, n: 'Factors', m: int) -> 'Factors':
        for p in n._n.keys():
            n[p] *= m
        return n

    @classmethod
    def _root(cls, n: 'Factors', m: int) -> 'Factors':
        for p in n._n.keys():
            if n[p] % m:
                raise ValueError
            n[p] //= m

        return n
