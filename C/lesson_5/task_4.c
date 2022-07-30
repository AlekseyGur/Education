/*
Запросить у пользователя количество используемых для вывода строк. Написать программу, которачя при помощи циклов и символа ^ будет рисовать на указанном количестве строк равнобедренный треугольник.
*/

#include <stdio.h>

int main() {
    int rows;
    printf("Введите количество строк=");
    scanf("%d", &rows);
    
    int width = 20;
    for(int i=1; i<=rows; i++){
        int j = 1;
        if(i==1){ // верхняя вершина треугольника
            for(j=1; j<=width; j++){
                if(j == width / 2){
                    printf("^");
                } else {
                    printf(" ");
                }
            }
        } else if(i==rows){ // нижнее основание треугольника
            for(j=1; j<=width; j++){
                printf("^");
            }
        } else { // бока треугольника (в строке два символа ^)
            for(j=1; j<=width; j++){
                int w2 = width / 2;
                int pos = w2 * i / rows;
                if(
                    j == w2 - pos ||
                    j == w2 + pos
                ){
                    printf("^");
                } else {
                    printf(" ");
                }
            }
        }
        printf("\n");
    }
}
