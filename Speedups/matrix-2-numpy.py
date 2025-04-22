import numpy as np
import time

def main():
    # Generate random matrices using NumPy
    size = 1000  # Adjust size for more intensive computation
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    # Measure time for matrix multiplication using NumPy
    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()
    
    print(f"Matrix multiplication completed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()


