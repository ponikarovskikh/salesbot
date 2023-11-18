from telebot import *
from telebot.types import *
from telebot.util import quick_markup
from telebot.callback_data import CallbackData, CallbackDataFilter
import logging
from sql import *
from keyboards import *
from requests.exceptions import ReadTimeout
logging.basicConfig(filename='bot_log.txt', level=logging.INFO)
bot=telebot.TeleBot(token='6304024040:AAGrVuOeVr6-uHbKweeWfBRX56__xT7b1mc',disable_web_page_preview=True)



parseinfo=['iphone 15','iphone 14','айфон 14']





@bot.message_handler(commands=['start'])
def welcome(msg:Message):
    username = msg.from_user.username
    user_id=msg.from_user.id
    chat_id=msg.chat.id
    bot.send_message(msg.chat.id,text=f'Привет,{username} Это бот воронка запросов из чатов по твоим интересующим позициям')
    if add_users_field(user_id, username,chat_id) =='new added':
        bot.send_message(msg.chat.id,'Друг, видим что ты впервые у нас ознакомься с функционалом',reply_markup=menu_keyboard_1stage())
    else:
        bot.send_message(msg.chat.id,'Друг, и снова здраствуй!',reply_markup=menu_keyboard_1stage())


@bot.message_handler(text=['Продавать товар'])
def menu(msg:Message):
    bot.send_message(msg.chat.id,text=f'Продавать товар:',reply_markup=menu_keyboard_2stage())









# Утилита для получения  айди самого себя
@bot.message_handler(commands=['ids'])
def idsend(msg:Message):
    username = msg.from_user.username
    link = f"[{username}](https://t.me/{username})"
    bot.send_message(msg.chat.id, link, parse_mode='Markdown', disable_web_page_preview=True)

#блок ключевых слов
@bot.message_handler(commands=['keywords'])
def kwrdupdt(msg:Message):
    if len(parseinfo)==0:
        bot.send_message(msg.chat.id,'💥🔦 <b>Мои ключевые слова</b>\nСейчас у тебя нет ключевых слов и фраз.',parse_mode='html',reply_markup=adddelete_keywords())
    elif len(parseinfo)>=0:
        keytext='\n'.join(parseinfo)
        print(keytext)
        bot.send_message(msg.chat.id,f'💥🔦 <b>Мои ключевые слова</b>\nСейчас у тебя следующие ключевые слова:\n\n{keytext}',parse_mode='html',reply_markup=adddelete_keywords())















#банлист
@bot.message_handler(commands=['banlist'])
def block_list(msg:Message):
    if get_blocked_users(msg.from_user.id,'len')==0:
            bot.send_message(msg.chat.id,'⛔ Заблокированные люди\n\nУпс,список пока пуст')
    elif get_blocked_users(msg.from_user.id,'len')>=0:
        bot.send_message(msg.chat.id,f'⛔ Заблокированные люди\n\nЛюди, от которых ты не получаешь сообщений в боте:'
                                     ,reply_markup=banlistmarkup(msg.from_user.id))

#-----------------------------------------------------------------------------------------------------------------
                        #ПРОВЕРКА ПОТОКА СООБЩЕНИЙ
# чекать все смс из чатов
@bot.message_handler(content_types=['text'])
def messagecheck(msg:Message):
    print(msg.text)
    if msg.text == 'Главное меню':
        bot.send_message(msg.chat.id, text=f'Главное меню:', reply_markup=menu_keyboard_1stage())
    if msg.text=='Продавать товар':
        bot.send_message(msg.chat.id, text=f'Продавать товар:', reply_markup=menu_keyboard_2stage())
    if msg.text=='Блок-лист':
        bot.send_message(msg.chat.id,'Раздел Блок-лист в разработке')
        block_list(msg)
    if msg.text == 'Выбрать товары':
        bot.send_message(msg.chat.id,'Раздел Выбрать товары в разработке')
    if msg.text == 'Premium-тариф':
        bot.send_message(msg.chat.id, 'Раздел Premium-тариф разработке')
    if msg.text == 'Ключевые слова':
        bot.send_message(msg.chat.id, 'Раздел Ключевые слова в разработке')
    if   msg.text == 'Продажи на паузу':
        bot.send_message(msg.chat.id, 'Раздел продажи на паузу в разработке')
    if   msg.text == 'Статистика запросов':
        bot.send_message(msg.chat.id, 'Раздел Статистика запросов в разработке')

    if msg.from_user.id not in get_blocked_users(msg.from_user.id,'dict'):
        for element in parseinfo:
            if element.lower() in msg.text.lower():
                print(element)
        # Прерываем цикл, если хотя бы один элемент найден
                sender_username = msg.from_user.username
                sender_user_id=msg.from_user.id
                text=msg.text
                link = f"[{sender_username}](https://t.me/{sender_username})\n\n" \
            f"{text}"
                bot.send_message(msg.from_user.id, link, parse_mode='Markdown', disable_web_page_preview=True,reply_markup=block_keyboard(sender_user_id,sender_username))
                break

#логика кнопок
@bot.callback_query_handler(func=lambda callback:callback.data)
def callback_logic(callback):
        print(callback.data)
        if str(callback.data).startswith('ban_'):
            clback=callback.data.split('_')
            block_id = int(clback[1])
            block_name=clback[2]
            # blocklist=add_delete_get_clear_blocked_users(block_id,block_name,callback.message.chat.id,'getall')
            need_ban=None
            for ban_item in add_delete_get_clear_blocked_users(block_id,block_name,callback.message.chat.id,'getall'):
                if block_id  not in ban_item:
                    need_ban=1
                else :
                    need_ban=0
            if need_ban==1:
                print(block_id,'нет в списке')
            if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                    bot.edit_message_text(f'{block_name} заблокирован',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name))
        elif str(callback.data).startswith('unban_') :
            clback = callback.data.split('_')
            unblock_id = int(clback[1])
            unblock_name = clback[2]
            print(unblock_id,unblock_name)

            for ban_item in add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'getall'):
                if unblock_id in ban_item:
                    print(unblock_id,'Eсть в списке')
                    if add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'delete')==2 :
                        bot.edit_message_text(f'{unblock_name} разблокирован', callback.message.chat.id, callback.message.id,
                        reply_markup=block_keyboard(unblock_id, unblock_name))






while True:
    bot.polling(none_stop=True,skip_pending=True)
    try:
        bot.polling(none_stop=True)
    except ReadTimeout as e:
        print(f"ReadTimeout error: {e}")
        # Перезапуск бота при ошибке чтения тайм-аута
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        # Здесь можно добавить обработку других исключений, если необходимо
        pass


