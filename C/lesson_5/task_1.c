/*
Математика
Есть формула (расчёт резисторного делителя) Uo=Ui*(R1/(R2+R1)). Написать расчёты для каждой переменной формулы по отдельности:
Ui = ...
R1 = ...
R2 = ...
*/

#include <stdio.h>

int main() {
    float Uo = 1;
    float Ui = 2;
    float R1 = 3;
    float R2 = 4;
    
    printf("Ui = %.2f\n", Uo/(R1/(R2+R1)) );
    printf("R1 = %.2f\n", Uo*(R2+R1)/Ui );
    printf("R2 = %.2f\n", (Ui*R1/Uo)-R1 );
}
