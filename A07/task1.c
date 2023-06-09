#include "sort.h"
#include <stdio.h>

void print_int_array(int* arr, int length) 
{
    for (int i = 0; i < length; i++) 
    {
        printf("%d ", arr[i]);
    }
}

int main() 
{
    int A[] = {5,3,6,5,3,7,9,2,10,0};
    size_t length = sizeof(A) / sizeof(A[0]);

    print_int_array(A, length);
    sort(A, length);
    printf("\n");
    print_int_array(A, length);

    return 0;
}