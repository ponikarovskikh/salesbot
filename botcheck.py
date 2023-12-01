import telebot.async_telebot
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.storage import StateMemoryStorage
from telebot import types
from telebot import asyncio_filters
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.asyncio_filters import AdvancedCustomFilter
import Text_of_messages
import config
from sql import *
from keyboards import *
from requests.exceptions import ReadTimeout
from Text_of_messages import *

bot = telebot.TeleBot(token=config.token)



# @bot.message_handler(commands=['menu'])
# def menu_up(callback=None,msg:Message=None):
#     if callback is not None and msg is None:
#         bot.send_message(callback.message.chat.id,'Главное меню',reply_markup=menu_keyboard_2stage(callback.message.chat.id))
#     elif msg is not None and callback is None:
#         bot.send_message(msg.chat.id,'Главное меню',reply_markup=menu_keyboard_2stage(msg.chat.id))

@bot.message_handler(commands=['start'])
def welcome(msg:Message):
        if  'group' in msg.chat.type:
            pass
        else:
            username = msg.from_user.username
            user_id=msg.from_user.id
            chat_id=msg.chat.id
            bot.send_message(msg.chat.id,text=f'Привет, {username}!\n\n{welcome_preview}')
            if add_users_field(user_id, username,chat_id) =='new added':
                 bot.send_message(msg.chat.id,'Друг, видим что ты впервые у нас ознакомься с функционалом - жми Продавать товар',reply_markup=menu_keyboard_1stage())
            else:
                 bot.send_message(msg.chat.id,'Друг, и снова здраствуй!',reply_markup=menu_keyboard_1stage())

@bot.message_handler(text=['Продавать товар'])
def menu(msg:Message):
          bot.send_message(msg.chat.id,text=f'Выберите сообщения которые хотите получать:',reply_markup=menu_keyboard_2stage(msg.chat.id))


@bot.message_handler(commands=['support'],regexp='Руководство бота')
def support_handler(msg:Message):
    if msg.chat.type == 'group':
        pass
    else:
          bot.send_message(msg.chat.id, text=support_info, parse_mode='HTML',reply_markup=menu_keyboard_2stage(msg.chat.id))

    # Утилита для получения  айди самого себя
@bot.message_handler(commands=['ids'])
def idsend(msg:Message):
        if msg.chat.type=='group':
            pass
        else:
            username = msg.from_user.username
            link = f"[{username}](https://t.me/{username})"
            bot.send_message(msg.chat.id, link, parse_mode='Markdown', disable_web_page_preview=True,reply_markup=menu_keyboard_2stage(msg.chat.id))

    #блок ключевых слов
@bot.message_handler(commands=['mykeywords'])
def kwrdupdt(msg:Message):
        if msg.chat.type=='group':
            pass
        else:
            keywords= get_user_and_keywords(msg.from_user.id)

            print(keywords)

            if len(keywords)==0:
                 bot.send_message(msg.chat.id,'💥🔦 <b>Мои ключевые слова</b>\n\nВ данный момент у тебя нет ключевых слов и фраз.',parse_mode='html',reply_markup=adddelete_keywords('addonly'))

            elif len(keywords)>0:
                keywords_showing=[]
                for key in keywords:
                      keywords_showing.append(' '.join(key))
                keywords_showing='\n'.join(keywords_showing)
                bot.send_message(msg.chat.id,f'💥🔦 <b>Мои ключевые слова</b>\n\n{keywords_showing}',parse_mode='html',reply_markup=adddelete_keywords())

        #to do: убирать ключевые слова по клвавиатуре и добавлять по next step handler

def add_delete_keyword_handler(callback):
         bot.edit_message_text('Добавьте ваше новое ключевое слово\n'
                              'Только <b>одно</b> слово на одной строке!\n'
                              'Например ->\n\nipad 3 mini\niphone 10s\nairpods 2'
                              , callback.message.chat.id, callback.message.id,
                              parse_mode='HTML')
         bot.send_message(callback.message.chat.id,'И затем жми отправить',reply_markup=ReplyKeyboardRemove())
         print(callback.message)
         bot.register_next_step_handler(callback.message,add_new_keyword)
def add_new_keyword(msg:Message):
        if '\n' in msg.text:
            newkeywordslist=msg.text.lower().split('\n')
            print(newkeywordslist)
            newkeyword=[]
            for keyword in newkeywordslist:
                newkeyword=keyword.split(' ')

                if add_delete_keyword(msg.chat.id, newkeyword, 'add') == 'added':
                     bot.send_message(msg.chat.id, f'Ключевое слово {keyword} успешно добавлено!',reply_markup=menu_keyboard_2stage(msg.chat.id))

                else:
                        bot.send_message(msg.chat.id,
                             'Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n' + premium_offer,
                             reply_markup=menu_keyboard_2stage(msg.chat.id))
                        break

        elif '\n' not in msg.text:
                newkeyword = msg.text.lower().split(' ')
                if add_delete_keyword(msg.chat.id,newkeyword,'add') =='added':
                 bot.send_message(msg.chat.id,'Ключевое слово успешно добавлено!',reply_markup=menu_keyboard_2stage(msg.chat.id))
                 bot.send_message(msg.chat.id, 'Добавим еще?',
                                  reply_markup=adddelete_keywords('addonly'))

        else:
                 bot.send_message(msg.chat.id, '❌Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n'+premium_offer,reply_markup=menu_keyboard_2stage(msg.chat.id))


@bot.message_handler(commands=['keywordslist_clear'])
def kwrd_list_del(callback):
    print('pltcm')
    if callback.message.chat.type == 'group':
        pass
    else:
         if add_delete_keyword(callback.message.chat.id,keyword=None,action='clear_list') == 'keywords_clear':
             bot.edit_message_text('Ваш список ключевых слов очищен',callback.message.chat.id,callback.message.id,reply_markup=adddelete_keywords('addonly'))
         else:
              bot.edit_message_text('Чтото не так со списком', callback.message.chat.id, callback.message.id)

    #банлист
@bot.message_handler(commands=['banlist_show'])
def block_list_show(msg:Message):
        if msg.chat.type=='group':
            pass
        else:
            print(msg.message_id)
            blocklist=add_delete_get_clear_blocked_users(user_id=msg.from_user.id,action='getall')
            print(len(blocklist))
            if len(blocklist)==0:
                     bot.send_message(msg.chat.id,'⛔ Заблокированные люди\n\nУпс,список пока пуст',reply_markup=menu_keyboard_2stage(msg.chat.id))

            else:
                 bot.send_message(msg.chat.id,banlist_preview
                                             ,reply_markup=banlistmarkup(msg.from_user.id,blocklist))




@bot.message_handler(commands=['banlist_clear'])
def block_list_clear(msg:Message):
        if msg.chat.type=='group':
            pass
        else:
            # print(msg.message_id)
            blocklist=add_delete_get_clear_blocked_users(user_id=msg.from_user.id,action='getall')
            # print(len(blocklist))
            if len(blocklist)!=0:
               if add_delete_get_clear_blocked_users(user_id=msg.from_user.id, action='clear')==3:
                     bot.send_message(msg.chat.id,'⛔ Блок-лист успешно очищен🧹')

            else:
                 bot.send_message(msg.chat.id,'⛔Блок-лист пока пуст ')





    #-----------------------------------------------------------------------------------------------------------------
                            #ПРОВЕРКА ПОТОКА СООБЩЕНИЙ
    # чекать все смс из чатов
@bot.message_handler(content_types=['text'])
def messagecheck(msg:Message):
        print(msg.text,msg.chat.id)
        if msg.chat.type =='private':
            if 'Главное меню' in msg.text:
                # print(22)
                bot.send_message(msg.chat.id, text=f'Главное меню:', reply_markup=menu_keyboard_1stage())
            elif 'Продавать товар' in msg.text:
                print(9)
                bot.send_message(msg.chat.id, text=f'Продавать товар:', reply_markup=menu_keyboard_2stage(msg.chat.id))
            elif 'Блок-лист' in  msg.text:
                # bot.send_message(msg.chat.id,'Раздел Блок-лист в разработке')
                 block_list_show(msg)
            elif 'Выбрать товары'in msg.text:
                print("yes")
                # bot.send_message(msg.chat.id,'Раздел Выбрать товары в разработке')
                bot.send_message(msg.chat.id, 'Выберите следующие товары по которым вы хотите получать сообщения',reply_markup=choosing_keyboard_proccess(level='product'))
            elif  'Premium-тариф' in msg.text:
                if prem_status(msg.chat.id)==True:
                    bot.send_message(msg.chat.id,'Ваш Premium-тариф активен',reply_markup=menu_keyboard_2stage(msg.chat.id))
                else:
                    bot.send_message(msg.chat.id, premium_promo+'\n❗❗ВНИМАНИЕ❗❗\n'+premium_promo1,parse_mode='HTML',reply_markup=getfreepremium())
            elif 'FAQ' in msg.text:
                bot.send_message(msg.chat.id, support_info, parse_mode='HTML',
                                 )

            elif  'Ключевые слова' in msg.text:
                 kwrdupdt(msg)
            elif  'Продажи на паузу'in msg.text:
                getchangeplaystatus(msg.chat.id,action=0)
                bot.send_message(msg.chat.id, 'Продажи приостановлены',reply_markup=menu_keyboard_2stage(msg.chat.id))
            elif 'руководство бота' in msg.text.lower():
                 support_handler(msg)
                # bot.send_message(msg.chat.id, 'Раздел продажи на паузу в разработке')
            elif 'Возобновить продажи' in msg.text:
                 getchangeplaystatus(msg.chat.id, action=1)
                 bot.send_message(msg.chat.id, 'Продажи возобновлены',reply_markup=menu_keyboard_2stage(msg.chat.id))
            # elif 'Статистика запросов' in msg.text :
            #     # print(msg.chat)
            #     bot.send_message(msg.chat.id, 'Раздел Статистика запросов в разработке')
            else:
                 bot.send_message(msg.chat.id,"ты ввел что то не то, выбери что-то из этого списка",reply_markup=menu_keyboard_2stage(msg.chat.id))
        if msg.chat.type=='supergroup' :
            # print(msg)

            Text = msg.text
            sender_id = msg.from_user.id
            sender_id = 0
            sender_username = 0
            crdtl = 'None'
            if ("_@_set") in Text:
                crdtl = Text[Text.index('set_@_'):Text.index('_@_set') + 6]
                Text = Text[Text.index('_@_set') + 6:]
                # crdtl = crdtl.split('_@_')
                crdtl = crdtl.split('_@_')
                sender_id = crdtl[1]
                sender_username = crdtl[2]

            message_correct=Text.lower()
            # print(message_correct)
            message_correct=message_correct.split(' ')
            # print(message_correct)
            for item in message_correct:
                if item in russiandict.keys():
                    # print('yes',item)
                    message_correct.insert(message_correct.index(item),russiandict[item])
                    message_correct.remove(item)
            message_correct=' '.join(message_correct)
            # print(message_correct)
            users_and_keywords=[]
            def users_and_keywords_list(access_sending:tuple,users_and_keywords:list):
                for user_id in  access_sending:
                    # print(user_id)
                    users_and_keywords.append(get_user_and_keywords(user_id,checking=True))
                # print(users_and_keywords)
                return tuple(users_and_keywords)



            access_sending = get_users_without_sendusermsg_in_blocklist(sender_id)
            # print(access_sending)
            checkinglist = users_and_keywords_list(access_sending,users_and_keywords)
            for user_keys in checkinglist:

                user_id_to=int(user_keys[0])
                keywords_check=user_keys[1]
                # print(user_id_to)
                # print(keywords_check)

                for kwrd in keywords_check:
                    need_send=0
                    not_need=0
                    for key in kwrd:
                        if str(key).lower() in  message_correct.lower():

                            need_send+=1
                        else:
                            not_need+=1
                    print(need_send,message_correct,user_id_to)
                    print(need_send,not_need,sender_id,user_id_to)
                    if sender_username == 0 and sender_id == 0:
                        sender_username = msg.from_user.username
                        sender_id = msg.from_user.id
                    if need_send>=3:
                        # if user_id_to!=int(sender_id):
                            if getchangeplaystatus(user_id_to,action='get')!=0:

                                print("sender_username:",sender_username,"      sender_id",sender_id,'  user_id_to',
                                      user_id_to)

                                link_text = f"[{sender_username}](https://t.me/{sender_username})\n\n" \
                                            f"{Text}"
                                bot.send_message(user_id_to, link_text, parse_mode='Markdown', disable_web_page_preview=True,reply_markup=block_keyboard(sender_id,sender_username,banlist=None))
                                break
                                pass
                    else:
                        need_send = 0
                        not_need = 0









    #логика кнопок
@bot.callback_query_handler(func=lambda callback:callback.data)
def callback_logic(callback):
            print(callback.data)
            # /логика бана
            if callback.data == 'banlist_show':
                    blocklist = add_delete_get_clear_blocked_users(user_id=callback.message.chat.id, action='getall')
                    if len(blocklist) == 0:
                         bot.edit_message_text(f'⛔ Заблокированные люди\n\nНа данный момент ваш список пуст', callback.message.chat.id,
                                          callback.message.id)
                    else:
                         bot.edit_message_text(f'⛔ Заблокированные люди от которых теперь вы не получаете сообщений в боте:\n\nОчистить всех /banlist_clear\n\nУдалить человека из Блок-листа - выберите пользователя ниже',
                                          callback.message.chat.id,
                                            callback.message.id, reply_markup=banlistmarkup(callback.message.chat.id,blocklist))

            elif str(callback.data).startswith('ban_') and not str(callback.data).endswith("_banlist"):
                print("ban")
                clback=callback.data.split('_')
                print(clback)
                block_id = int(clback[1])
                block_name=clback[2]
                need_ban=[]
                blocklist=add_delete_get_clear_blocked_users(block_id, block_name, callback.message.chat.id, 'getall')
                print(blocklist)
                if len(blocklist)==0:
                    if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                         bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,None))
                else:
                    for ban_item in blocklist:
                        if block_id  not in ban_item:
                            need_ban.append(1)
                        else :
                            need_ban.append(0)
                    print('need_ban',need_ban)
                    if 1 in need_ban:
                        if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                            bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,
                                                  callback.message.id,reply_markup=unblock_keyboard(block_id,
                                                                                                    block_name,None))
            elif str(callback.data).startswith('ban_')  and str(callback.data).endswith("_banlist"):
                print("ban_banlist")
                clback=callback.data.split('_')
                block_id = int(clback[1])
                block_name=clback[2]
                need_ban=[]
                blocklist= add_delete_get_clear_blocked_users(block_id,block_name,callback.message.chat.id,'getall')
                if len(blocklist)==0:
                    if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                          bot.edit_message_text(f'🔒 {block_name} заблокирован(a)\n❌И сообщения от него больше поступать не будут',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,True))
                else:
                    for ban_item in blocklist:
                        if block_id  not in ban_item:
                            need_ban.append(0)
                        else :
                            need_ban.append(1)
                    print(need_ban)
                    if 1 not in need_ban:
                        if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                          bot.edit_message_text(f'🔒 {block_name} заблокирован(a)\n❌И сообщения от него больше поступать не будут',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,True))
                        elif     add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')=='2.1':
                            bot.edit_message_text(
                            f' ⚠️Ошибка! {block_name} уже нет в списке или раннее вы его разблокировали',
                            callback.message.chat.id, callback.message.id,
                            reply_markup=menu_keyboard_2stage(callback.message.from_user.id))

            elif str(callback.data).startswith('unban_') and not str(callback.data).endswith("_banlist"):
                print('unban 1')
                clback = callback.data.split('_')
                unblock_id = int(clback[1])
                unblock_name = clback[2]
                # print(unblock_id,unblock_name)
                blocklist=add_delete_get_clear_blocked_users(unblock_id, unblock_name, callback.message.chat.id, 'getall')
                if len(blocklist)==0:
                    bot.edit_message_text(
                        f'🔓 {unblock_name} разблокирован(a) \n✅Теперь вы можете получать от него сообщения',
                        callback.message.chat.id, callback.message.id,
                        reply_markup=block_keyboard(block_id=unblock_id, block_name=unblock_name, banlist=None))
                else:
                    for ban_item in add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'getall'):
                        print('1====')
                        if unblock_id in ban_item:
                            print(unblock_id,'Eсть в списке')
                            if add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'delete')==2 :
                                bot.edit_message_text(f'🔓 {unblock_name} разблокирован(a) \n✅Теперь вы можете получать от него сообщения', callback.message.chat.id, callback.message.id,
                            reply_markup=block_keyboard(block_id= unblock_id,block_name= unblock_name,banlist=None))
                        else:
                            bot.edit_message_text(
                            f'🔓 {unblock_name} разблокирован(a) \n✅Теперь вы можете получать от него сообщения',
                            callback.message.chat.id, callback.message.id,
                            reply_markup=block_keyboard(block_id=unblock_id, block_name=unblock_name, banlist=None))
            elif str(callback.data).startswith('unban_') and str(callback.data).endswith("_banlist"):
                    clback = callback.data.split('_')
                    unblock_id = int(clback[1])
                    unblock_name = clback[2]
                    # print(unblock_id,unblock_name)
                    for ban_item in add_delete_get_clear_blocked_users(unblock_id, unblock_name, callback.message.chat.id,
                                                                       'getall'):
                        if unblock_id in ban_item:
                        # print(unblock_id, 'Eсть в списке')
                            if add_delete_get_clear_blocked_users(unblock_id, unblock_name, callback.message.chat.id, 'delete') == 2:
                                bot.edit_message_text(f'🔓 {unblock_name} разблокирован(a) \n✅Теперь вы можете получать от него сообщения', callback.message.chat.id, callback.message.id, reply_markup=block_keyboard(block_id=unblock_id,block_name=unblock_name,banlist=True))

            elif callback.data=="add_keyword":
                 add_delete_keyword_handler(callback)
            elif callback.data in 'delete_keywords':
                 kwrd_list_del(callback)
                 #временная раздача халявы
            elif callback.data == "free_premium":
                bot.delete_message(callback.message.chat.id, callback.message.id )
                if controling_premium(callback.message.chat.id, True) in [2, 1]:
                    bot.send_message(callback.message.chat.id, premium_bonus, parse_mode='HTML')

            elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepyear'):
                product_name=callback.data.split('_')[1]
                bot.edit_message_text(
                    f'Товар <b>{product_name.capitalize()}</b> выбран✅\nТеперь укажите год вашей линейки снизу ',
                    callback.message.chat.id, callback.message.id,parse_mode="HTML",
                    reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'year',callback.data,{f'{product_name}':f'✅'}))


            elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepmemory'):
                product_name = callback.data.split('_')[1]
                product_year = callback.data.split('_')[2]

                bot.edit_message_text(
                f'Товар: <b>{product_name.capitalize()}</b>✅\n' \
                f'Год линейки: {product_year} ✅\n' \
                f'Теперь укажите серию, цвет, память ⤵',
                callback.message.chat.id, callback.message.id, parse_mode = "HTML",
                reply_markup = choosing_keyboard_proccess(callback.message.chat.id, 'memory', callback.data,
                                                          {f'{product_name}': f'✅',f"{product_year}":"✅"}))

            elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_choosen'):

                product_name = callback.data.split('_')[1]
                product_year = callback.data.split('_')[2]
                product_model=callback.data.split('_')[3]
                product_spec = callback.data.split('_')[4]
                product_color=callback.data.split('_')[5]
                product_memory = callback.data.split('_')[6]

                if product_spec == 'orig':
                            new_keyword = f'{product_name} {product_model} {product_color} {product_memory}'
                else:
                            new_keyword = f'{product_name} {product_model} {product_spec} {product_color} {product_memory}'
                new_keyword=new_keyword.split(' ')


                if add_delete_keyword(callback.message.chat.id, new_keyword, 'add') == 'added':

                            bot.edit_message_text(
                            f'Ключевое слово добавлено ✅\n\n'\
                            f'Теперь по <b>{ " ".join(new_keyword)}</b>\n'
                            f'Будут приходить запросы в этот бот 📩\n'
                            f'Эта позиция дополнительно сохранится  в списке ваших ключевых слов',
                            callback.message.chat.id, callback.message.id, parse_mode="HTML")

                else:
                        bot.edit_message_text(
                         f'<b>Лимит на добавление ключевых слов превышен❌ </b>\n\n'+Text_of_messages.premium_offer,
                                callback.message.chat.id, callback.message.id, parse_mode="HTML")






import asyncio
if __name__=='__main__':
    while True :
        try:
            bot.polling(non_stop=True)
        except Exception as E:
            pass
        except IndexError as I:
            pass
        except ConnectionError as CE:
           pass




