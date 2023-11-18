from telebot import *
from telebot.types import *
from telebot.util import quick_markup
from sql import *

def menu_keyboard_1stage():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,one_time_keyboard=True)
    play_button = types.KeyboardButton('Продавать товар')

    keyboard.add(play_button)

    return keyboard


def menu_keyboard_2stage():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,one_time_keyboard=True)
    func1 = types.KeyboardButton('Главное меню')
    func2=types.KeyboardButton('Выбрать товары')
    func3=types.KeyboardButton('Premium-тариф')
    func4=types.KeyboardButton('Блок-лист')
    func5=types.KeyboardButton('Ключевые слова')
    func6=types.KeyboardButton('Продажи на паузу ')
    func7=types.KeyboardButton('Статистика запросов')
    keyboard.add(func1)
    keyboard.row(func2,func3)
    keyboard.row(func4,func5)
    keyboard.row(func6,func7)
    return keyboard


















#keyboard_block
def adddelete_keywords():
    return quick_markup(
        {

        '➕ Добавить ключевые слова': {'callback_data': f'add_keyword'},'🗑 Убрать ключевые слова':{'callback_data': f'delete_keyword'}
        }, row_width=1
    )































#ban/unban
def block_keyboard(block_id,block_name):
    return quick_markup({

                '🚷Заблокировать человека': {'callback_data': f'ban_{block_id}_{block_name}'}}, row_width=1)

def unblock_keyboard(block_id,block_name):
    return quick_markup({

                'Разблокировать человека🔑': {'callback_data': f'unban_{block_id}_{block_name}'}}, row_width=1)


def banlistmarkup(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    blocklist=get_blocked_users(user_id,'dict')

    for items in blocklist.items():

        button_text = f'{items[1]}'
        callback_data = f'unban_{items[0]}_{items[1]}_banlist'

        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        markup.add(button)

    return markup