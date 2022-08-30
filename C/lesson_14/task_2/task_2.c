/*
    2 Структуры.
    Описать структуру "прямоугольник", содержащую целочисленные значения длины, ширины, 
    периметра и площади прямоугольника. Написать функцию, принимающую на вход указатель 
    на структуру, подсчитывающую и записывающую площадь и периметр данного 
    прямоугольника в структуру.
*/

#include <stdio.h>

typedef struct rectangle {
    int width;
    int height;
    int len;
    int area;
} Rectangle;

int calc_len_area(Rectangle *r);

int main() {
    Rectangle r;
    
    r.width = 2;
    r.height = 2;
    
    calc_len_area(&r);
    
    printf("width = %d\n", r.width);
    printf("height = %d\n", r.height);
    printf("len = %d\n", r.len);
    printf("area = %d\n", r.area);
}

int calc_len_area(Rectangle *r) {
    r->len = 2 * (r->width + r->height);
    r->area = r->width * r->height;
    return 0;
}
