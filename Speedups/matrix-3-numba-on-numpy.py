from numba import jit
import numpy as np
import time

@jit(nopython=True)
def matrix_multiplication(A, B):
    return np.dot(A, B)

def main():
    size = 1000
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    start_time = time.time()
    C = matrix_multiplication(A, B)
    end_time = time.time()

    print(f"Matrix multiplication completed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()

