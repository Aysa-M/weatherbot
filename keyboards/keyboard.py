from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
