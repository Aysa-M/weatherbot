import math
from typing import Tuple, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import WeatherReports
from database.orm import get_reports
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
    reports: WeatherReports = get_reports(tg_id)
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


async def next_page(current_pg: int, kb_builder_rep: InlineKeyboardBuilder,
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
        kb_builder_rep.row(*[
            InlineKeyboardButton(text=LEXICON_RU['prev'],
                                 callback_data=f'prev_{current_pg-CONST_2}'),
            InlineKeyboardButton(text=f"{current_pg-CONST_1}/{total_pages}",
                                 callback_data="None"),
            InlineKeyboardButton(text=LEXICON_RU['next'],
                                 callback_data=f"next_{current_pg}")
                                 ], width=3)
    else:
        pass
    return kb_builder_rep.as_markup()


async def previous_page(current_pg: int, kb_builder_rep: InlineKeyboardBuilder,
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
        kb_builder_rep.row(*[
            InlineKeyboardButton(text=LEXICON_RU['prev'],
                                 callback_data=f"prev_{current_pg}"),
            InlineKeyboardButton(text=f"{current_pg + CONST_1}/{total_pages}",
                                 callback_data="None"),
            InlineKeyboardButton(text=LEXICON_RU['next'],
                                 callback_data=f"next_{current_pg+CONST_2}")
                                 ], width=3)
    else:
        pass
    return kb_builder_rep.as_markup()


async def history_btn_inline(tg_id: int,
                             current_pg=CONST_1) -> InlineKeyboardMarkup:
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
    kb_builder_rep, total_pages = await report_inline(tg_id, current_pg)
    await next_page(current_pg, kb_builder_rep, total_pages)
    return kb_builder_rep.as_markup()


async def report_btn_inline(rep_id: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[
        InlineKeyboardButton(text='Назад',
                             callback_data=f"reports_{rep_id}"),
        InlineKeyboardButton(text='Удалить запрос',
                             callback_data=f"deleted_{rep_id}")
    ])
    return kb_builder.as_markup()
