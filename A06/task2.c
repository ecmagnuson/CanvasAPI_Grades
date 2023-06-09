#include "structs.h"
#include <stdio.h>
#include <stdlib.h>

int main() 
{
    printf("%lu\n", sizeof(struct A));
    printf("%lu\n", sizeof(struct B)); 
 
    struct A *a;
    struct B *b;

    a = (struct A*)malloc(sizeof(struct A));

    a->i = 10;
    a->c = 'a';
    a->d = 20.0;

    printf("%d\n", a->i);
    printf("%c\n", a->c);
    printf("%f\n", a->d);

    free(a);
    //free(b); I don't believe this is necessary because no malloc was called to make instance of B
    
    return 0;
}