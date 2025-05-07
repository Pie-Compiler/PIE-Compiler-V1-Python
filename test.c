#include <stdio.h>
#include <stdlib.h>

int main(){
    int test;
    printf("Hello, World!\n");
    printf("Enter a number: ");
    scanf("%d", &test);
    printf("You entered: %d\n", test);
    if (test > 0) {
        printf("The number is positive.\n");
    } else if (test < 0) {
        printf("The number is negative.\n");
    } else {
        printf("The number is zero.\n");
    }
    return 0;
}
