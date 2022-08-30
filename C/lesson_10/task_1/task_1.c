/*
    1 Указатели.
    Используя заголовочный файл <math.h>, описать функцию,
    int calculateSquareEquality(int a, int b, int c, float* x1, float* x2);
    Которая будет решать квадратное уравнение вида a * x ^ 2 + b * x + c = 0,
    и записывать корни этого уравнения в переменные, адреса которых переданы
    в качестве указателей х1 и х2. Функция должна вернуть -1, если уравнение
    не имеет корней, 0, если у уравнения есть один корень, и 1, если у уравнения два корня.
*/

#include <stdio.h>
#include <math.h>

int calculateSquareEquality(); // прототип

int main() {
    float x1, x2;
    int calc = calculateSquareEquality(
        4,
        -7,
        -2,
        &x1,
        &x2
    );
    
    printf("Ответ функции: %d\n", calc);
    printf("x1 = %f\n", x1);
    printf("x2 = %f\n", x2);
}

int calculateSquareEquality(int a, int b, int c, float* x1, float* x2) {
    // Функция решает квадратное уравнение вида a * x ^ 2 + b * x + c = 0
    int d = b*b - 4*a*c;
    if(d < 0) return -1; // уравнение не имеет корней
    *x1 = ((-1)*b - sqrt(d)) / (2*a);
    *x2 = ((-1)*b + sqrt(d)) / (2*a);
    if(d == 0) return 0; // есть один корень
    return 1; // есть два корня
}
