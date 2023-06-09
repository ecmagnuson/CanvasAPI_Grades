#!/usr/bin/env python3

from pyMatmul import matmul
import time

def time_2_to_nth(n):
    start_time = time.perf_counter()
    A = []
    #if n = 3
    #A is:
    #[[0, 0, 0], 
    # [1, 1, 1], 
    # [2, 2, 2]]
    #etc
    for i, _ in enumerate(range(n)):
        A.append([i] * n)
    B = A 
    C = matmul(A, B)
    end_time = time.perf_counter()
    result = round(end_time - start_time, 3)
    print(f"matrix product calculation for {n} x {n} array took {result} seconds.")

def main():
    time_2_to_nth(2 ** 7)
    time_2_to_nth(2 ** 8)
    time_2_to_nth(2 ** 9)

if __name__ == "__main__":
    main()