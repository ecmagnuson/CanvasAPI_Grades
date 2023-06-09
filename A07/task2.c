#include "mvmul.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>


/* generate a random floating point number from min to max */
// From https://stackoverflow.com/questions/33058848/generate-a-random-double-between-1-and-1
// the range is clear. 
// randmax of 2147483647 / range, honestly isnt clear to me
// and we want the min value added to the stdlib rand() method over this div
// that isnt really clear to me
double randfrom(double min, double max) 
{
    double range = (max - min); 
    double div = RAND_MAX / range;
    return min + (rand() / div);
}

int main(int argc, char *argv[]) 
{
    double *A;
    int n = atoi(argv[1]);

    //fill A with doubles range(-1, 1)
    A = (double*)malloc(sizeof(double) * (n*n));
    for (int i = 0; i < (n*n); i++) 
    {
        double num = randfrom(-1.0, 1.0);
        A[i] = num;
    }

    //fill b with 1.0
    double b[n];
    for (int i = 0 ; i < n; i++) 
    {
        b[i] = 1.0;
    } 

    double c[n];


    clock_t begin = clock();
    mvmul(A, b, c, n);
    clock_t end = clock();
    double time_spent = ((double)(end - begin) / CLOCKS_PER_SEC) * 1000;
    
    printf("%f\n", c[n -1]);
    printf("%f", time_spent);

    free(A);

    return 0;
}