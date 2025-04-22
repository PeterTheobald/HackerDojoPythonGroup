from numba import jit
import numpy as np
import time

# uncomment this to jit compile:
# @jit(nopython=True)
def matrix_multiplication(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Perform matrix multiplication of A and B using nested loops."""
    result = np.zeros((A.shape[0], B.shape[1]), dtype=A.dtype)
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                result[i, j] += A[i, k] * B[k, j]
    return result

def main():
    # Generate random matrices using NumPy
    size = 1000  # Adjust size for more intensive computation
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    # Measure time for matrix multiplication
    start_time = time.time()
    C = matrix_multiplication(A, B)
    end_time = time.time()
    
    print(f"Matrix multiplication completed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()

