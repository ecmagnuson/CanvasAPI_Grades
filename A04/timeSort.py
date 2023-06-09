#!/usr/bin/env python3

from pySort import sorter
import random
import time

def time_sort_list(nums):
    start_time = time.perf_counter()
    print(f"First element of your list is {nums[0]}")
    sorter(nums)
    end_time = time.perf_counter()
    result = round(end_time - start_time, 3)
    print(f"It took {result} seconds to sort your list of {len(nums)} numbers with a Bubble sort")
    print(f"Now the first element in your list is {nums[0]}\n")

def main():
    #random number between 1 and 1000
    random.seed(1)

    ten_to_3 = [random.randint(1,1001) for i in range(10 ** 3)]
    ten_to_4 = [random.randint(1,1001) for i in range(10 ** 4)]
    ten_to_5 = [random.randint(1,1001) for i in range(10 ** 5)]
    ten_to_6 = [random.randint(1,1001) for i in range(10 ** 6)]

    time_sort_list(ten_to_3)
    time_sort_list(ten_to_4)
    time_sort_list(ten_to_5)
    time_sort_list(ten_to_6)

if __name__ == "__main__":
    main()