#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from math import sqrt


def fib(n):
    """Recursive function to print Fibonacci sequence

    Easy to understand but slow in execution
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci(n):
    """Calculated value of the fibonacci sequence

    Difficult to understand but very fast in execution
    """
    return int(((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5)))


if __name__ == '__main__':

    # Change this value for a different result
    nterms = 40

    # uncomment to take input from the user
    # nterms = int(input("How many terms? "))

    # check if the number of terms is valid
    if nterms <= 0:
        print("Plese enter a positive integer")
    else:
        print("Fibonacci sequence:")
        for i in range(nterms):
            print(fibonacci(i))
