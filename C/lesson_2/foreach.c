#include <stdio.h>

#define foreach(item, array) \
    for(int keep = 1, \
            count = 0,\
            size = sizeof (array) / sizeof *(array); \
        keep && count != size; \
        keep = !keep, count++) \
      for(item = (array) + count; keep; keep = !keep)

int main(int argc, char **argv, char **envp) {
    
    // Выводит аргументы, с которыми была 
    // вызвана программа (включая название скрипта!)
        if (argc > 1){
            foreach(int *v, argv) {
                printf("%s\n", *v);
            }
        }else{
            printf("Скрипт запущен без параметров\n");
        }
    
        
    return 0;
}
