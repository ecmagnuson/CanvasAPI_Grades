#!/usr/bin/env python3

'''
https://en.wikipedia.org/wiki/File:Bubble-sort-example-300px.gif
lst = [6,5,3,1,8,7,2,4]
lst = [5,6,3,1,8,7,2,4]
lst = [5,3,6,1,8,7,2,4]
etc
'''

# I feel like I may have overcomplicated this
def sorter(A):
    #sort list A and return None -- in place
    i = 0
    nums_sorted = 0  
    #current_len is the length of the array we have left to sort. 
    #Every time we sort one number, it gets pushed to the back, so we no longer
    #need to check that number and current_len is decreased by 1.
    current_len = len(A)

    while current_len != 0:
        if i == current_len - 1: #avoid index errors
            nums_sorted += 1 #We have placed the biggest remaining number in its correct place
            current_len -= 1 #Make sure to not look at already sorted numbers
            i = 0 
            continue

        current = A[i]
        nxt = A[i + 1]
        if nxt < current:
            A[i] = nxt
            A[i + 1] = current
        i += 1
    return None