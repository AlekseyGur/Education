# Урок 2. Docker

Напишите Dockerfile к любому приложению из директорий [golang или python](https://github.com/adterskov/geekbrains-conteinerization/blob/master/homework/2.docker/README.md) на ваш выбор (можно к обоим).

Образ должен собираться из официального базового образа для выбранного языка. На этапе сборки должны устанавливаться все необходимые зависимости, а так же присутствовать команда для запуска приложения.

Старайтесь следовать рекомендациям (Best Practices) из лекции при написании Dockerfile.

При запуске контейнера из образа с указанием проксирования порта (флаг -p или -P если указан EXPOSE) при обращении
на localhost:port должно быть доступно приложение в контейнере (оно отвечает Hello, World!).

Сохраните получившийся Dockerfile в любом публичном Git репозитории, например GitHub, и пришлите ссылку на репозиторий.
