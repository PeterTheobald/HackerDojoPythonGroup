def newfunc(x):
  return "Hello"+ x

def anotherfunc(x):
    return "Goodbye"+ x

def factorial(n):
    """Calculate the factorial of n (n!)"""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
