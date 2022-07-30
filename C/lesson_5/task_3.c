/*
Циклы.
Запросить у пользователя десять числе. Вывести на эжкран среднее арифметическое введённых чисел.
*/

#include <stdio.h>

int main() {
    float sum = 0;
    int count = 10;
    
    for(int i=1; i<=count; i++){
        int num = 0;
        printf("Введите число=");
        scanf("%d", &num);
        printf("\n");
        sum += num;
    }
    printf("Среднее арифметическое = %.2f\n", sum / count);
}
