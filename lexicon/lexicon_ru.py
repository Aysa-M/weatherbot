from typing import Dict


my_location: str = 'Погода в моём городе'
other_location: str = 'Погода в другом месте'
history: str = 'История'
set_location: str = 'Установить свой город'
menu: str = 'Меню'

LEXICON_RU: Dict[str, str] = {
    '/start': ', привет! Я бот, показывающий прогноз погоды на сегодня.',
    menu: ', я бот, который расскажет тебе о погоде на сегодня',
    my_location: 'Я так пока не умею'
}
