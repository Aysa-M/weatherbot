import asyncio

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon import lexicon_ru


async def main_menu():
    btn1: KeyboardButton = KeyboardButton(text='Погода в моём городе')
    btn2: KeyboardButton = KeyboardButton(text='Погода в другом месте')
    btn3: KeyboardButton = KeyboardButton(text='История')
    btn4: KeyboardButton = KeyboardButton(text='Установить свой город')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2],
                                           [btn3, btn4]],
                                 resize_keyboard=True)
    return markup


async def menu_answer():
    menu_btn: KeyboardButton = KeyboardButton(text=lexicon_ru.menu)
    return ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                               resize_keyboard=True)
