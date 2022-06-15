# python_chat_bots_lesson1

Телеграмм бот, присылающий оповещение о проверке работ, написанный в рамках курса "Чат-боты на Python" [dvmn.org](dvmn.org).  Бот взаимодействует с API сайта [dvmn.org](dvmn.org) и присылает уведомления о сданных работах пользователю с идентификатором USER_ID.

### Как установить

Скачайте файлы проекта. Создайте файл .env с полями:
```
BOT_TOKEN=''# значение, полученное при регистрации телеграмм бота
BOT_USER_ID=''# идентификатор пользователя в телеграмм
DVMN_TOKEN=''# идентификатор пользователя на сайте [dvmn.org](dvmn.org)
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример запуска скрипта

#### Запуск из терминала
Телеграмм бота можно запустить командой:```python main.py```
В случае удачного выполнения команды пользователю идентификатором BOT_USER_ID будут приходить оповещения о проверенных  работах на сайте сайта [dvmn.org](dvmn.org).

#### Запуск на сервере Heroku
Код готов к запуску на сервисе Heroku. Для этого нужно скопировать этот репозиторий, зарегистрироваться на Heroku и на странице приложений создать новое.
На странице приложения на вкладке Deploy нужно связать аккаунты GitHub и Heroku и загрузить код из основной ветки. Сервис автоматически установит зависимости из файла requirements.txt, считает тип приложения из Procfile и запустит бота в окружении, сконфигурированном через runtime.txt. Также на вкладке Resourses нужно выделить ресурсы для работы бота. Необходимые переменные окружения нужно задать в Config Vars настройках (Settings) приложения на web-сервисе Heroku.


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
