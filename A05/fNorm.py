#!/usr/bin/env python3

import csv
import os
import sys

import numpy as np

def csv_data(csv_filename_arg):
    with open(os.path.join(os.path.dirname(__file__), csv_filename_arg + '.csv')) as f:
        reader = csv.reader(f)
        return np.array(list(reader))

def frobenius_norm(arr):
    #https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
    return round(np.linalg.norm(arr, 'fro'), 3 )

def main():
    csv_filename_arg = sys.argv[1]
    arr = csv_data(csv_filename_arg)
    print(frobenius_norm(arr))

if __name__ == "__main__":
    main()    