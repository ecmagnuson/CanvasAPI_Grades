#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np 
import random
import sys 
import time

from pyMatmul import matmul

def twoD_matrix(n):
    #return a 2D list of n x n filled with random floats between -1 and 1
    #https://stackoverflow.com/questions/58605134/creating-a-2d-array-with-random-numbers-without-numpy-python
    return [[round(random.uniform(-1, 1),2) for _ in range(n)] for _ in range(n)]

def time_matmul(A, B):
    start_time = time.perf_counter()
    if isinstance(A, list) and isinstance(B, list):
        C = matmul(A, B)
    elif isinstance(A, np.ndarray) and isinstance(B, np.ndarray):
        C = A @ B
    else: return None
    end_time = time.perf_counter()
    miliseconds = round((end_time - start_time) * 1000, 3) #miliseconds 

    if len(A) == 2 ** 8:
        print(C[0][0])
        print(miliseconds)
    
    return miliseconds

def make_plot(my_times, np_times):
    #my_times -> List[float] from 2**5 to 2**8
    #np_times -> List[float] from 2**5 to 2**8
    n_values = [2**5, 2**6, 2**7, 2**8]
    plt.plot(n_values, my_times, label="my matmul")
    plt.plot(n_values, np_times, label='np matmul')
    plt.xscale('log',base=2) 
    plt.yscale('log',base=10) 
    plt.legend()
    plt.title('manual matmul of n x n array vs. numpy')
    plt.xlabel("Size of 2D matrix (n x n)")
    plt.ylabel("Time (ms)")
    plt.savefig('matmul_compare.pdf')
    #plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("set_plotBool", help="set plotBool to a value 0 or 1", type=int, choices=[0,1])
    args = parser.parse_args()
    plotBool = args.set_plotBool

    my_times = []
    np_times = []
    for power in range(5, 9):
        A_list = twoD_matrix(2 ** power)
        B_list = twoD_matrix(2 ** power)
        my_times.append(time_matmul(A_list, B_list))

        A = np.array(A_list)
        B = np.array(B_list)
        np_times.append(time_matmul(A, B))

    if plotBool == True: #same as if 1
        make_plot(my_times, np_times)

if __name__ == "__main__":
    main()