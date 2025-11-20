import unittest
from primes import eratosthenes_sieve, is_prime


class MyTestCase(unittest.TestCase):
    primes_up_to_100 = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
                        61, 67, 71, 73, 79, 83, 89, 97}

    def test_eratosthenes_sieve(self):
        self.assertEqual(eratosthenes_sieve(100), self.primes_up_to_100)

    def test_is_prime(self):
        self.assertEqual({p for p in range(1, 100) if is_prime(p)}, self.primes_up_to_100)
