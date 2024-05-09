import math
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Users, WeatherReports
from database.orm import get_reports, get_users
from lexicon import lexicon_ru
from lexicon.lexicon_ru import LEXICON_RU
from settings.bot_config import CONST_1, CONST_2, CONV_DISPLAY


async def report_inline(tg_id: int, current_pg=CONST_1):
    """
    Генерация отображения списка отчетов в инлайн кнопках при нажатии на
    кнопку меню 'История', на инлайн кнопки '<<' и '>>'.
    Args:
        tg_id (int): идентификатор пользователя в телеграме
        current_pg (int): передается текущая отображаемая страница списка
        отчетов. Defaults to CONST_1.
    Returns:
        InlineKeyboardBuilder: возвращает объект класса InlineKeyboardBuilder,
        для дальнейшего дополнения кнопками навигации пагинации
    """
    kb_builder_rep: InlineKeyboardBuilder = InlineKeyboardBuilder()
    reports: List[WeatherReports] = get_reports(tg_id)
    total_pages: int = math.ceil(len(reports) / CONV_DISPLAY)
    if current_pg <= total_pages and current_pg >= CONST_1:
        for rep in reports[current_pg*CONV_DISPLAY-CONV_DISPLAY:
                           current_pg*CONV_DISPLAY]:
            kb_builder_rep.row(*[InlineKeyboardButton(
                text=f"{rep.city} {rep.date.day}.{rep.date.month}."
                     f"{rep.date.year}",
                callback_data=f"report_{rep.id}"
            )])
    return kb_builder_rep, total_pages


async def reports_next_page(current_pg: int, kb_builder: InlineKeyboardBuilder,
                            total_pages: int) -> InlineKeyboardMarkup:
    """
    Генерирует сообщение с инлайн кнопками в случае нажатия кнопки ">>"
    Args:
        current_pg (int): передается текущая отображаемая страница списка
        отчетов.
        kb_builder_rep (InlineKeyboardBuilder): объект класса
        InlineKeyboardBuilder, для дальнейшего дополнения кнопками навигации
        пагинации
        total_pages (int): общее количество страниц списка отчетов
    Returns:
        InlineKeyboardMarkup: готовое инлайн меню, встроенное в сообщение
    """
    if current_pg <= total_pages:
        current_pg += CONST_1
        kb_builder.row(*[
            InlineKeyboardButton(text=LEXICON_RU['prev'],
                                 callback_data=f'prev_{current_pg-CONST_2}'),
            InlineKeyboardButton(text=f"{current_pg-CONST_1}/{total_pages}",
                                 callback_data="None"),
            InlineKeyboardButton(text=LEXICON_RU['next'],
                                 callback_data=f"next_{current_pg}")
                                 ], width=3)
    else:
        pass
    return kb_builder.as_markup()


async def reports_previous_page(current_pg: int,
                                kb_builder: InlineKeyboardBuilder,
                                total_pages: int) -> InlineKeyboardMarkup:
    """
    Генерирует сообщение с инлайн кнопками в случае нажатия кнопки "<<"
    Args:
        current_pg (int): передается текущая отображаемая страница списка
        отчетов.
        kb_builder_rep (InlineKeyboardBuilder): объект класса
        InlineKeyboardBuilder, для дальнейшего дополнения кнопками навигации
        пагинации
        total_pages (int): общее количество страниц списка отчетов

    Returns:
        InlineKeyboardMarkup: готовое инлайн меню, встроенное в сообщение
    """
    if current_pg <= total_pages and current_pg >= CONST_1:
        current_pg -= CONST_1
        kb_builder.row(*[
            InlineKeyboardButton(text=LEXICON_RU['prev'],
                                 callback_data=f"prev_{current_pg}"),
            InlineKeyboardButton(text=f"{current_pg + CONST_1}/{total_pages}",
                                 callback_data="None"),
            InlineKeyboardButton(text=LEXICON_RU['next'],
                                 callback_data=f"next_{current_pg+CONST_2}")
                                 ], width=3)
    else:
        pass
    return kb_builder.as_markup()


async def history_btn_inline(tg_id: int,
                             current_pg: int = CONST_1) -> InlineKeyboardMarkup:
    """
    Создает меню с инлайн кнопками первой страницы списка отчетов пользователя
    Args:
        tg_id (int): идентификатор пользователя в телеграме
        current_pg (int): передается текущая отображаемая страница списка
        отчетов. Defaults to CONST_1.
    Returns:
        InlineKeyboardMarkup: меню к сообщению истории запросов с
        инлайн кнопками каждого отчета и навигацией
    """
    kb_builder_rep, total_pages = await report_inline(tg_id,
                                                      current_pg)
    await reports_next_page(current_pg, kb_builder_rep, total_pages)
    return kb_builder_rep.as_markup()


async def report_btn_inline(rep_id: str,
                            current_pg: int = CONST_1) -> InlineKeyboardMarkup:
    """
    Генерирует меню с инлайн-кнопками при формировании сообщения в ответ
    на нажатие на инлайн кнопку с определенным отчетом
    Args:
        rep_id (str): идентификатор отчета по погоде по определенному
        населенному пункту
        current_pg (str): передается страница списка отчетов, которая
        содержала в себе запрошенный отчет.
    Returns:
        InlineKeyboardMarkup: меню с инлайн-кнопками к сообщению о
        конкретном запрошенном отчете
    """
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[
        InlineKeyboardButton(text='Назад',  # exmpl reports_3
                             callback_data=f"return_{current_pg}"),
        InlineKeyboardButton(text='Удалить запрос',
                             callback_data=f"delrep_{rep_id}")
    ])
    return kb_builder.as_markup()


async def users_list_inline(current_pg=CONST_1):
    kb_builder_users: InlineKeyboardBuilder = InlineKeyboardBuilder()
    users: List[Users] = get_users()
    total_pages: int = math.ceil(len(users) / CONV_DISPLAY)
    if current_pg <= total_pages and current_pg >= CONST_1:
        for user in users[current_pg*CONV_DISPLAY-CONV_DISPLAY:
                          current_pg*CONV_DISPLAY]:
            kb_builder_users.row(*[InlineKeyboardButton(
                text=(f'{user.id} '
                      f'id: {user.tg_id} '
                      f'Подключился: {user.connection_date.day}.'
                      f'{user.connection_date.month}.'
                      f'{user.connection_date.year} '
                      f'Отчётов: {len(user.reports)}'),
                callback_data='None')])
    return kb_builder_users, total_pages


async def users_list_page(current_pg: int,
                          kb_builder_users: InlineKeyboardBuilder,
                          total_pages: int) -> InlineKeyboardMarkup:
    if current_pg <= total_pages and current_pg >= CONST_1:
        kb_builder_users.row(*[
            InlineKeyboardButton(text=lexicon_ru.LEXICON_RU['prev'],
                                 callback_data=f'prevuser_{current_pg-CONST_1}'
                                 ),
            InlineKeyboardButton(text=f'{current_pg}/{total_pages}',
                                 callback_data='None'),
            InlineKeyboardButton(text=lexicon_ru.LEXICON_RU['next'],
                                 callback_data=f'nextuser_{current_pg+CONST_1}'
                                 )])
    return kb_builder_users.as_markup()


async def generate_users_list(current_pg=CONST_1) -> InlineKeyboardMarkup:
    kb_builder_users, total_pages = await users_list_inline(current_pg)
    await users_list_page(current_pg, kb_builder_users, total_pages)
    return kb_builder_users.as_markup()
