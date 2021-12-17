#!/usr/bin/env python
#  -*- coding: utf-8 -*-


def prime_factors(n: int) -> list[int]:
    """Returns all the prime factors of a positive integer

    used in "opgave 22" of 2017
    """
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n /= d
        d = d + 1
        if d * d > n:
            if n > 1:
                factors.append(int(n))
            break
    return factors


def prime_factors_unique(n: int) -> list[int]:
    """Returns all the prime factors of a positive integer

    used in "opgave 22" of 2017
    """
    factors = []
    d = 2
    while n > 1:
        if n % d == 0:
            _("Found prime factor:", n)
            factors.append(d)
            n /= d
        d = d + 1
        if d * d > n:
            if n > 1:
                factors.append(int(n))
            break
    return factors


def is_prime(n: int) -> bool:
    """returns True if parameter n is a prime number,
    False if composite and "Neither prime, nor composite" if neither

    >>> is_prime(5)
    True
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# returns smallest factor of parameter n
def find_smallest_factor(n: int) -> int:
    factor = 2  # start at the lowest possible factor
    while n % factor != 0:  # go until factor is a factor
        if factor >= n ** 0.5:  # there is no factor if past square root point
            return n
        factor += 1  # test the next factor
    return factor


def prime_factorization(n: int) -> list[int]:
    """Reduces the parameter n into a product of only prime numbers
    and returns a list of those prime number factors

    >>> prime_factorization(600851475143)
    [71, 839, 1471, 6857]
    """
    primes = []  # list of prime factors in the prime factorization
    largest_factor = n / find_smallest_factor(n)

    i = 2
    while i <= largest_factor:  # for all possible prime factors (2 - largest factor of the number being reduced)

        if is_prime(i) and n % i == 0:  # if this value is prime and the number is divisible by it

            primes.append(i)  # add that prime factor to the list
            n /= i  # divide out that prime factor from the number to start reducing the new number
            largest_factor /= i  # divide out that prime factor from the largest factor to get the largest factor of the new number
            i = 2  # reset the prime factor test
        else:
            i += 1  # increment the factor test

    primes.append(int(n))  # add the last prime number that could not be factored
    primes.sort()
    return primes


if __name__ == '__main__':
    import doctest

    doctest.testmod()
