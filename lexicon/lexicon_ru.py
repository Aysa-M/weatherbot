from typing import Dict


menu: str = 'Меню'
my_location: str = 'Погода в моём городе'
other_location: str = 'Погода в другом месте'
history: str = 'История'
set_own_location: str = 'Установить свой город'
set_location: str = 'Введите название города'
forward: str = '>>'
prev: str = '<<'

error_name: str = 'Напишите название города с заглавной буквы'
absence_user_city: str = 'Пожалуйста установите "ваш" город'

CMD_RU: Dict[str, str] = {
    '/start': ', привет! Я бот, показывающий прогноз погоды на сегодня.',
}

LEXICON_RU: Dict[str, str] = {
    'Меню': ', я бот, который расскажет тебе о погоде на сегодня',
    'Погода в моём городе': 'Я так пока не умею',
    'Установить свой город': 'Хотите установить ваш город? Введите название:',
    'История': 'История запросов:',
    'prev': '<<',
    'next': '>>',
}
