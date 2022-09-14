# Урок 6. ETL

## Задачи

Развернуть Airflow из репозитория: https://github.com/puckel/docker-airflow (командой docker-compose -f docker-compose-LocalExecutor.yml up -d)

Написать даг, котрый будет делать следующее:

task_1 будет BranchPythonOperator, который будет читать Variable hw_etl, которое должно равняться 1, 2 или любое другое число; и в зависимости от этого даг должен запускать таски по-разному:

1. Когда hw_etl=1 картинка hw_6_var_1.png
2. Когда hw_etl=2 картинка hw_6_var_2.png
3. Когда hw_etl not in (1,2) картинка hw_6_var_not_12.png

Картинки приложил.
Ваш даг должен выглядеть так же, как на картинках в материалах.

## Решение

См. файл my_dag.py
