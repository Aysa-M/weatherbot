import asyncio
import math

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import WeatherReports

from database.orm import get_reports
from lexicon import lexicon_ru


async def main_menu():
    btn1: KeyboardButton = KeyboardButton(text=lexicon_ru.my_location)
    btn2: KeyboardButton = KeyboardButton(text=lexicon_ru.other_location)
    btn3: KeyboardButton = KeyboardButton(text=lexicon_ru.history)
    btn4: KeyboardButton = KeyboardButton(text=lexicon_ru.set_own_location)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2],
                                           [btn3, btn4]],
                                 resize_keyboard=True)
    return markup


async def menu_answer():
    menu_btn: KeyboardButton = KeyboardButton(text=lexicon_ru.menu)
    return ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                               resize_keyboard=True)


async def report_inline(tg_id: int, current_pg=1) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    reports: WeatherReports = get_reports(tg_id)
    total_pages = math.ceil(len(reports) / 4)
    print(total_pages)
    if current_pg < total_pages:
        for report in reports[:current_pg*4]:
            kb_builder.row(*[InlineKeyboardButton(
                text=(f"{report.city} {report.date.day}.{report.date.month}."
                      f"{report.date.year}"),
                callback_data=f"report_{report.id}"
            )])
        current_pg += 1
        kb_builder.row(*[
            InlineKeyboardButton(text=f"{current_pg-1}/{total_pages}",
                                 callback_data="None"),
            InlineKeyboardButton(text=lexicon_ru.forward,
                                 callback_data=f'next_{current_pg}')
            ],
            width=2)
    return kb_builder.as_markup()
