# test_telegBot

Тестовое задание. Телеграм бот с выводом погоды в указаном городе. А также сбор статей с групп ВК и запись в articles.csv [ТЗ](https://github.com/alexsad95/test_telegBot/blob/master/files/ТЗ.pdf)

Для запуска бота нужно:
 - Склонировать репозиторий, перейти в папку с приложением
 - Сделать сборку через docker
 - Запустить docker run
 - Найти бот и прописать команду /help

```sh
$ git clone https://github.com/alexsad95/test_telegBot
$ cd test_telegBot
$ docker build -t bot-app .
$ docker run --rm --name bot bot-app
```

Работа бота: 

![](https://github.com/alexsad95/test_telegBot/blob/master/files/bot_work.png)
