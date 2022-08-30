/*
    1 Строки.
    Описать функцию, возвращающую строку с двоичным представлением десятичного числа, переданного в аргументе этой функции.
*/

#include <stdio.h>
#include <stdlib.h> // для calloc
#include <string.h> // для strlen
#define MAX_VAL_LEN 50 // максимальная длина числа для преобразования

char * str_bin();
char * strrev();

int main() {
    int a = 8; // десятичное число для преобразования в двоичное
    printf("%s\n", str_bin(a));
}

char * str_bin(int a) {
    char * str = calloc(MAX_VAL_LEN, sizeof(int));
    int i = 1;
    while(a > 0){
        if(a % 2 != 0){
            strcat(str, "1");
        }else{
            strcat(str, "0");
        }
        a /= 2;
        i++;
    }
    return strrev(str);
}

char *strrev(char *str) { // возвращает строк ус обратным порядком символов
    if (!str || ! *str)
        return str;

    int i = strlen(str) - 1, j = 0;

    char ch;
    while (i > j)
    {
        ch = str[i];
        str[i] = str[j];
        str[j] = ch;
        i--;
        j++;
    }
    return str;
}
