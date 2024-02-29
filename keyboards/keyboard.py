from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon import lexicon_ru


async def main_menu() -> ReplyKeyboardMarkup:
    btn1: KeyboardButton = KeyboardButton(text=lexicon_ru.my_location)
    btn2: KeyboardButton = KeyboardButton(text=lexicon_ru.other_location)
    btn3: KeyboardButton = KeyboardButton(text=lexicon_ru.history)
    btn4: KeyboardButton = KeyboardButton(text=lexicon_ru.set_own_location)
    markup = ReplyKeyboardMarkup(keyboard=[[btn1, btn2],
                                           [btn3, btn4]],
                                 resize_keyboard=True)
    return markup


async def menu_answer() -> ReplyKeyboardMarkup:
    menu_btn: KeyboardButton = KeyboardButton(text=lexicon_ru.menu)
    return ReplyKeyboardMarkup(keyboard=[[menu_btn]],
                               resize_keyboard=True)


async def process_admin_btn() -> ReplyKeyboardMarkup:
    admin_btn: KeyboardButton = KeyboardButton(
        text=lexicon_ru.LEXICON_RU['admin'])
    return ReplyKeyboardMarkup(keyboard=[[admin_btn]], resize_keyboard=True)
