#include "sort.h"
#include <stdio.h>

void sort(int* A, size_t n_elements) {
    int i = 0;
    int nums_sourted = 0;
    int current_len = n_elements;

    while (current_len != 0)
    {
        if (i == current_len)
        {
            nums_sourted++;
            current_len--;
            i = 0;
            continue;
        }
        
        int current = A[i];
        int nxt = A[i+1];
        if (nxt < current) 
        {
            A[i] = nxt;
            A[i+1] = current;
        }
        i++;
    }
}
