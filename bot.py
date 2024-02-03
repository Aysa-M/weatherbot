from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from api_requests import request
from keyboards.keyboard import main_menu, menu_answer
from lexicon import lexicon_ru
from settings.bot_config import Config, load_config


config: Config = load_config('.env')
BOT: Bot = Bot(token=config.tg_bot.token)
# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()
DP: Dispatcher = Dispatcher(storage=storage)


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class ChoicePlace(StatesGroup):
    # Состояние ожидания ввода населенного пункта
    waiting_city: State = State()


@DP.message(CommandStart(), StateFilter(default_state))
async def start_message(message: Message):
    text: str = (f'{message.from_user.first_name}'
                 f'{lexicon_ru.LEXICON_RU["/start"]}')
    markup = await main_menu()
    await message.answer(text, reply_markup=markup)


# Хэндлер срабатывает на нажатие кнопки 'Установить свой город'
# и переводит бота в состояние ожидания ввода населенного пункта
@DP.message(F.text == lexicon_ru.set_location, StateFilter(default_state))
async def set_user_location(message: Message, state: State):
    start_txt = 'Введите название города'
    markup = await menu_answer()
    await message.answer(start_txt, reply_markup=markup)
    await state.set_state(ChoicePlace.waiting_city)


@DP.message(StateFilter(ChoicePlace.waiting_city), F.text.isalpha())
async def chosen_user_location(message: Message, state: State):
    if message.text[0].islower():
        await message.answer('Названия городов пишутся с большой буквы')
        return
    await state.update_data(waiting_city=message.text)
    markup = await main_menu()
    user_location = await state.get_data()
    data = request.get_weather_data(user_location.get('waiting_city'))
    text = f'Погода в {user_location.get("waiting_city")}\nТемпература: {data["temp"]} C\nОщущается как: {data["feels_like"]} C \nСкорость ветра: {data["wind_speed"]}м/с\nДавление: {data["pressure_mm"]}мм'
    await message.answer(text, reply_markup=markup)
    await state.clear()


# Хэндлер срабатывает на нажатие кнопки 'Погода в другом месте'
# и переводит бота в состояние ожидания ввода населенного пункта
@DP.message(F.text == lexicon_ru.other_location, StateFilter(default_state))
async def set_location(message: Message, state: FSMContext):
    start_txt = 'Введите название города'
    markup = await menu_answer()
    await message.answer(start_txt, reply_markup=markup)
    # Устанавливаем состояние ожидания ввода населенного пункта
    await state.set_state(ChoicePlace.waiting_city)


@DP.message(StateFilter(ChoicePlace.waiting_city), F.text.isalpha())
async def chosen_location(message: Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer('Названия городов пишутся с большой буквы')
        return
    await state.update_data(waiting_city=message.text)
    markup = await main_menu()
    location = await state.get_data()
    data = request.get_weather_data(location.get('waiting_city'))
    text = f'Погода в {location.get("waiting_city")}\nТемпература: {data["temp"]} C\nОщущается как: {data["feels_like"]} C \nСкорость ветра: {data["wind_speed"]}м/с\nДавление: {data["pressure_mm"]}мм'
    await message.answer(text, reply_markup=markup)
    await state.clear()


@DP.message(F.text == lexicon_ru.menu)
async def menu_message(message: Message):
    text: str = (f'{message.from_user.first_name}'
                 f'{lexicon_ru.LEXICON_RU[lexicon_ru.menu]}')
    markup = await main_menu()
    await message.answer(text, reply_markup=markup)


if __name__ == '__main__':
    DP.run_polling(BOT)
