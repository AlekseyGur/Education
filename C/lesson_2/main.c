#include <stdio.h>

int main(int argc, char **argv) {
    
    // Выводит аргументы, с которыми была 
    // вызвана программа (включая название скрипта!)
        if (argc > 1){
            for (int i = 0; i < argc; ++i) {
                printf("%s\n", argv[i]);
            }
        }else{
            printf("Скрипт запущен без параметров\n");
        }
        
    // Тернарный оператор
        a = (a>b) ? b : a;
    
    // Пример задания переменной, ввода и вывода
        int a = 50;
        int b;
        
        printf("Введите целое число: ");
        scanf("%d", &b);
        
        printf("a = %d\nb = %d\n", a, b);
        
    return 0;
}
