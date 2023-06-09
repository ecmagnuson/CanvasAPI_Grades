#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

//check that user input is a positive integer
int check_int() 
{
    int N;
    //https://www.quora.com/What-is-a-C-program-that-accepts-only-integers-as-inputs
    // I assumed that == 1 means "is True" that it is a "%d" digit, but I guess
    // it means to check if one parameter was read
    // I don't fully understand why.. since 4.5 is one parameter.. but it works correctly
    if ((scanf("%d", &N) != 1) || (N < 0)) 
    {
        printf("Enter a positive integer");
        exit(1);
    }  
    return N;
}

int isNumber(char number[])
// I took this entire method from here - slightly changed
// https://stackoverflow.com/questions/29248585/c-checking-command-line-argument-is-integer-or-not
// This entire method is copied from the post except I changed the return to 1 and 0 because my C doesn't have booleans? idk..
// it looks at the first char of the number to make sure it isnt '-' so that takes care of negative numbers
// Then there is a handy "isdigit" method that can just check if the char is a digit, i.e. not a double or float etc.
{
    int i = 0;

    //checking for negative numbers
    if (number[0] == '-') 
    {
        printf("Enter a positive number");
        exit(1);
    }
    for (; number[i] != 0; i++)
    {
        if (!isdigit(number[i]))
            return 0;
    }
    return 1;
}

// fill and then print an int array -> 0 .. N.length
void print_array(int *nums, int length) 
{
    for (int i = 0; i < length; i++)
    {
        nums[i] = i;
    }

    for (int i = 0; i < length; i++)
    {
        printf("%d ", nums[i]);
    }
}

int compare(const void* numA, const void* numB)
//This method is from here
//https://www.includehelp.com/c-programs/sort-integer-array-using-qsort-with-a-function-pointer.aspx
//It uses the logic of comparing the two numbers that are passed into it
//if num1 is less than num2 it will know this by the return statement. Likewise, if it is greater
//it will return -1. If the same it will return 0.
//I understand const is a constant value so it wont change.
// It looks like from here
// https://stackoverflow.com/questions/34713446/qsort-comparison-why-const-void
// (classic that its closed -- yet entirely valid stack overflow question) 
// that the parameter is void to help it be a sort of generic type, because it might not need to be an int.
{
    const int* num1 = (const int*)numA;
    const int* num2 = (const int*)numB;

    if (*num1 < *num2) {
        return 1;
    }
    else if (*num1 > *num2) {
        return -1;
    }
    return 0;
}

void print_reverse(int *nums, int length) 
// reverse sorts the array and then prints it in reverse
{
    qsort(nums, length, sizeof(int), compare);

    for (int i = 0; i < length; i++)
    {
        printf("%d ", nums[i]);
    }
}


//This is really messy because I thought you wanted unser stdin not a command line argument the rant out of time to clean up
int main(int argc, char *argv[]) 
{
    int *nums;
    //int N = check_int();

    if(argc == 2) {
        if (!isNumber(argv[1]))
        {
            printf("Enter a positive number");
            exit(1);
        }
    }
    else if( argc > 2 ) {
        printf("Too many arguments supplied.\n");
    }
    else {
        printf("One argument expected.\n");
    }

    int N = atoi(argv[1]);
    int length = N + 1;

    nums = (int*)malloc(sizeof(int) * length);

    print_array(nums, length);

    printf("\n"); //new line

    print_reverse(nums, length);

    free(nums); //free nums malloc

    return 0;  
}

