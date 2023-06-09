#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np 
import random
import sys 
import time

from pySort import sorter

def oneD_lst(n):
    #return a list of random ints (-10 to +10) of size n
    return [random.randint(-10,10) for num in range(n)]

def my_sort(A):
    start_time = time.perf_counter()
    sorter(A)
    end_time = time.perf_counter()
    miliseconds = round((end_time - start_time) * 1000, 3) #miliseconds 
    if len(A) == 2 ** 13:
        print(A[0])
        print(miliseconds)
    return miliseconds

def py_sort(A):
    start_time = time.perf_counter()
    B = sorted(A) #sorted not in place
    end_time = time.perf_counter()
    miliseconds = round((end_time - start_time) * 1000, 3) #miliseconds 
    if len(B) == 2 ** 13:
        print(B[0])
        print(miliseconds)
    return miliseconds

def np_sort(A):
    start_time = time.perf_counter()
    B = np.sort(A)
    end_time = time.perf_counter()
    miliseconds = round((end_time - start_time) * 1000, 3) #miliseconds 
    if len(B) == 2 ** 13:
        print(B[0])
        print(miliseconds)
    return miliseconds    
    
def make_plot(my_t, py_t, np_t):
    n_values = [2**10, 2**11, 2**12, 2**13]
    plt.plot(n_values, my_t, label="my bubblesort function")
    plt.plot(n_values, py_t, label="py sorted function")
    plt.plot(n_values, np_t, label='np sort function')
    plt.xscale('log',base=2) 
    plt.yscale('log',base=10) 
    plt.legend()
    plt.title('Comparing sorting algorithms:\n manual bubblesort, python sorted, and numpy sort')
    plt.xlabel("Size of list (n)")
    plt.ylabel("Time (ms)")
    plt.savefig('sorting_compare.pdf')
    #plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("set_plotBool", help="set plotBool to a value 0 or 1", type=int, choices=[0,1])
    args = parser.parse_args()
    plotBool = args.set_plotBool

    #3 lists for differing sorting algorithms from 2**10 to 2**13
    my_times = [] #my sorter from pySort
    py_times = [] #python stdlib sorted
    np_times = [] #numpy.sort
    for power in range(10, 14):
        A_list = oneD_lst(2 ** power)
        B_list = A_list[:]
        A = np.array(A_list)

        my_times.append(my_sort(A_list))
        py_times.append(py_sort(B_list))
        np_times.append(np_sort(A))

    if plotBool == True: #same as if 1
        make_plot(my_times, py_times, np_times)

if __name__ == "__main__":
    main()