# BOT-ASSISTENT - Telegram-бот (далее - "бот")

Описание бота:

Бот предоставляет сведения о погоде в указанном пользователем населенном пункте по состоянию на текущую дату путем обращения к API сервиса Яндекс.Погода.
Для запуска корректной работы бота необходимо указывать в файле .env токен бота и идентификатор администратора.

Для получения данных необходимых для формирования отчета о погоде в насленном пункте в запросе к API сервиса Яндекс.Погода необходимо отправить точные координаты населенного пункта, которые можно получить из базы сервиса Геокод.
Обращение к API сервиса Геокод для установки точных координат происходит с помощью уникального API ключа.
Таким образом, для получения данных нужно сгенерировать два ключа для отправки / получения запросов / ответов на / от API Яндекс.Погода и API Геокод.

Результат запроса к серверу Яндекс.Погода в виде отчета сохраняется в базе данных реализованной на СУБД PostgreSQL.
Для представления моделей Python в БД используется ORM система SQLAlchemy. Именно эта система создает движок с подключением к БД и сессию подключения.


**Деплой бота:**

Склонируйте репозиторий: $ git clone https://github.com/Aysa-M/weatherbot.git

Создайте виртуальное окружение - должен быть флажок (venv) в начале строки: $ python -m venv venv

Установите зависимости: $ pip install -r requirements.txt

Создайте аккаунт бота в мессенджере Telegram:

Найдите в Telegram бота @BotFather. Обратите внимание на иконку возле имени бота: белая галочка на голубом фоне - она означает, что бот настоящий.

Зарегистрируйте бота. Начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»). Затем отправьте команду /newbot и укажите параметры нового бота:
*имя (на любом языке), под которым ваш бот будет отображаться в списке контактов;
*техническое имя вашего бота, по которому его можно будет найти в Telegram. Имя должно быть уникальным и оканчиваться на слово bot в любом регистре, например Kittybot, kitty_bot.
*Если аккаунт создан, @BotFather поздравит вас и отправит в чат токен для работы с Bot API.

Настройте аккаунт бота через @BotFather. Отправьте команду /mybots и вы получите список ботов, которыми вы управляете. Укажите бота, которого нужно отредактировать, и нажмите кнопку Edit Bot. Можно изменить: Имя бота (Edit Name). Описание (Edit Description) — текст, который пользователи увидят в самом начале диалога с ботом под заголовком «Что может делать этот бот?» Общую информацию (Edit About) — текст, который будет виден в профиле бота. Картинку-аватар (Edit Botpic). Команды (Edit Commands) — подсказки для ввода команд.

Для полноценной работы необходимо разместить бот на рабочем сервере: Необходимо найти хостинг, где вы сможете развернуть проект.

Технологии (основные инструменты):
Python==3.11.9
aiogram==3.3.0
SQLAlchemy==2.0.25

**Авторы:**
Matsakova Aysa