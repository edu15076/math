from common import cfor


def lowest_prime_factor(n: int, start: int = 2) -> int:
    """
    Find the lowest prime factor of a number.
    :param n: The number to find the lowest prime factor of.
    :param start: The starting prime from where to start the search.
    :return: The lowest prime factor of n.
    """
    if start <= 3:
        if not n & 1:
            return 2
        if not n % 3:
            return 3
        start = 5

    for i in cfor(start, lambda i: i * i <= n, lambda i: i + (i - 3) % 6):
        if not n % i:
            return i

    return n


def is_prime(n: int) -> bool:
    return 1 < n and (n <= 3 or not (n + 1) % 6 or not (n - 1) % 6) and n == lowest_prime_factor(n)


def eratosthenes_sieve(n: int) -> set:
    primes = {i for i in range(2, n + 1)}

    for i in range(2, n + 1):
        if i in primes:
            for j in range(i * i, n + 1, i):
                primes.discard(j)

    return primes
