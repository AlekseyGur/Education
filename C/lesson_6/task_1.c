#include <stdio.h>
#include "func.h"

int func_after(); // прототип

int main() {
    printf("Главный файл загрузился\n");
    check_include();
    func_after();
}

int func_after() {
    printf("Функция, которая находится после main()\n");
}
