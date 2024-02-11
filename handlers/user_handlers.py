from email import message
import math
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup

from api_requests import request
from database.orm import (add_user, get_reports, set_user_city,
                          create_report, get_user_location)
from handlers.states import ChoicePlace, ChoiceUserPlace
from keyboards.keyboard import main_menu, menu_answer, report_inline
from lexicon import lexicon_ru


usrouter: Router = Router()


@usrouter.message(CommandStart(), StateFilter(default_state))
async def start_message(message: Message):
    """
    Хэндлер обрабатывающий сообщение, содержащее команду '/start'
    Args:
        message (Message): message object from update
    """
    add_user(message.from_user.id)
    text: str = (f'{message.from_user.first_name}'
                 f'{lexicon_ru.CMD_RU["/start"]}')
    markup: ReplyKeyboardMarkup = await main_menu()
    await message.answer(text, reply_markup=markup)


@usrouter.message(F.text == lexicon_ru.menu, StateFilter(default_state))
async def menu_message(message: Message):
    """
    Хэндлер срабатывает на ввод сообщения Меню
    Args:
        message (Message): message object from update
    """
    text: str = (f'{message.from_user.first_name}'
                 f'{lexicon_ru.LEXICON_RU[lexicon_ru.menu]}')
    await message.answer(text, reply_markup=await main_menu())


@usrouter.message(F.text == lexicon_ru.my_location, StateFilter(default_state))
async def get_myplace_weather(message: Message):
    """
    Хэндлер срабатывает на нажатие кнопки 'Погода в моём городе'
    Args:
        message (Message): message object from update
    """
    user_loc = get_user_location(message.from_user.id)
    if user_loc is None:
        await message.answer(lexicon_ru.absence_user_city,
                             reply_markup=await main_menu())
        return
    data = request.get_weather_data(user_loc)
    create_report(
        message.from_user.id, data['temp'], data['feels_like'],
        data['wind_speed'], data['pressure_mm'], user_loc
    )
    weather: str = (f"Forecast for {user_loc}\n"
                    f"Temperature: {data['temp']} C\n"
                    f"Feels like: {data['feels_like']} C\n"
                    f"Wind: {data['wind_speed']} m/sec\n"
                    f"Pressure: {data['pressure_mm']} mm")
    await message.answer(weather, reply_markup=await main_menu())


@usrouter.message(F.text == lexicon_ru.other_location,
                  StateFilter(default_state))
async def set_any_location(message: Message, state: FSMContext):
    """
    Хэндлер срабатывает на нажатие кнопки 'Погода в другом месте'
    и переводит бота в состояние ожидания ввода населенного пункта
    Args:
        message (Message): message object from update
        state (State): waiting for the location name input
    """
    await message.answer(lexicon_ru.set_location,
                         reply_markup=await main_menu())
    await state.set_state(ChoicePlace.any_location)


@usrouter.message(StateFilter(ChoicePlace.any_location), F.text.isalpha())
async def chosen_any_location(message: Message, state: FSMContext):
    """
    Хэндлер срабатывает, если бот в состоянии ожидания ввода населенного пункта
    и пользователь ввел информацию
    Args:
        message (Message): message object from update
        state (State): waiting for the location name input
    """
    if message.text[0].islower():
        await message.answer(lexicon_ru.error_name)
        return
    await state.update_data(any_location=message.text)
    location = await state.get_data()
    data = request.get_weather_data(location.get('any_location'))
    create_report(
        message.from_user.id, data['temp'], data['feels_like'],
        data['wind_speed'], data['pressure_mm'], location.get('any_location')
    )
    text: str = (f"Forecast for {location.get('any_location')}\n"
                 f"Temperature: {data['temp']} C\n"
                 f"Feels like: {data['feels_like']} C\n"
                 f"Wind: {data['wind_speed']} m/sec\n"
                 f"Pressure: {data['pressure_mm']} mm")
    await message.answer(text, reply_markup=await main_menu())
    await state.clear()


@usrouter.message(F.text == lexicon_ru.history, StateFilter(default_state))
async def get_user_reports(message: Message):
    """
    Хэндлер срабатывает на нажатие кнопки 'История', формируя
    все отчеты по погоде, которые пользователь запрашивал
    Args:
        message (Message): message object from update
    """
    inline_markup = await report_inline(message.from_user.id)
    await message.answer(
        lexicon_ru.LEXICON_RU[lexicon_ru.history],
        reply_markup=inline_markup)


@usrouter.callback_query(lambda callback_query: 'next' in callback_query.data)
async def process_forward_inlbtn(callback: CallbackQuery, state: FSMContext):
    """
    Когда пользователь нажимает на инлайн кнопку "Вперед", бот загружает
    следующую страницу отчета, если текущая страница не последняя.
    Номер текущей страницы на кнопке увеличится на 1.
    А если текущая страница последняя в отчете, то ничего не изменится.
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery, в
        котором callback data это слово Вперед - "data": "next_{current_pg}"
                    {
                        "text": "Вперед",
                        "callback_data": "next_{current_pg}"
                    }
    """
    # Выход если получили str(None). Как в последней или первой странице.
    if callback.data == 'None':
        return
    # Получаем тип операции и номер следующей страницы или отчета из
    # callback_data
    forward_btn, next_pg = callback.data.split('_')
    # Сохраняем страницу на которой находится пользователь в память
    data = await state.get_data()
    data['current_pg'] = int(next_pg)
    await state.update_data(current_pg=data['current_pg'])
    # Если пользователь нажал кнопку вперед
    if forward_btn == 'next':
        markup = await report_inline(callback.from_user.id, data['current_pg'])
        await callback.message.edit_reply_markup(reply_markup=markup)


@usrouter.callback_query(lambda callback_query: 'previous'
                         in callback_query.data)
async def process_prev_inlbtn(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'None':
        return


@usrouter.message(F.text == lexicon_ru.set_own_location,
                  StateFilter(default_state))
async def set_user_location(message: Message, state: State):
    """
    Хэндлер срабатывает на нажатие кнопки 'Установить свой город'
    и переводит бота в состояние ожидания ввода "своего" города
    Args:
        message (Message): message object from update
        state (State): waiting for the location name input
    """
    await message.answer(
        lexicon_ru.LEXICON_RU[lexicon_ru.set_own_location],
        reply_markup=await menu_answer())
    await state.set_state(ChoiceUserPlace.user_location)


@usrouter.message(StateFilter(ChoiceUserPlace.user_location), F.text.isalpha())
async def chosen_user_location(message: Message, state: FSMContext):
    """
    Хэндлер срабатывает, если бот в состоянии ожидания ввода "своего" города
    и пользователь ввел информацию
    Args:
        message (Message): message object from update
        state (State): waiting for the location name input
    """
    if message.text[0].islower():
        await message.answer(lexicon_ru.error_name)
        return
    await state.update_data(user_location=message.text)
    user_data = await state.get_data()
    set_user_city(message.from_user.id, user_data.get('user_location'))
    text: str = f'{user_data.get("user_location")} установлен как "свой" город'
    await message.answer(text, reply_markup=await main_menu())
    await state.clear()
