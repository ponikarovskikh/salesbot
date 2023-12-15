from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage as STM
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import StatesGroup as STSGR,State as ste
import asyncio
from Text_of_messages import *
from config import *
from keyboards import *
import json

import asyncio
from pyrogram import Client


global app
global bot


async def clientside(bot):
    class SuperStates(STSGR):
        getkeyword = ste()





    # print(StateMemoryStorage().get_state(Message.de_json(dict).id,Message.de_json().from_user.id))


    @bot.message_handler(commands=['start'])
    async def welcome(msg:Message):
            if  'private' in msg.chat.type:

                username = msg.from_user.username
                user_id=msg.from_user.id
                chat_id=msg.chat.id

                await bot.send_message(msg.chat.id,text=f'Привет, {username}!\n\n{welcome_preview}')
                if add_users_field(user_id, username,chat_id) =='new added':
                    await bot.send_message(msg.chat.id,'Так как вы впервые у нас, ознакомьтесь с функционалом в разделе '
                                                       '</b>Руководство📚</b>'
                                                  ,reply_markup=menu_keyboard_2stage(user_id))
                else:
                   await  bot.send_message(msg.chat.id,'Друг, и снова здраствуй!',reply_markup=menu_keyboard_1stage())

    # @bot.message_handler(text=['Продавать товар'])
    async def sell(msg:Message):
              await bot.send_message(msg.chat.id,text=f'Вы в разделе продажа товаров.\n\n'
                                                      f'Сюда будут приходить все сообщения о товарах согласно вашим '
                                                      f'ключевым словам.\n\n'
                                                      f'Для ознкаомления работы бота нажмите FAQ',
                                reply_markup=menu_keyboard_2stage(msg.chat.id))




    @bot.message_handler(commands=['support'])
    async def  support_handler(msg:Message):
        print('support')
        if msg.chat.type == 'private':
            await  bot.send_message(msg.chat.id, text=support_info, parse_mode='HTML',reply_markup=menu_keyboard_2stage(
                msg.chat.id))

        # Утилита для получения  айди самого себя
    @bot.message_handler(commands=['ids'])
    async def idsend(msg:Message):
            if msg.chat.type=='private':
                username = msg.from_user.username
                link = f"[{username}](https://t.me/{username})"
                await  bot.send_message(msg.chat.id, link, parse_mode='Markdown', disable_web_page_preview=True,
                                  reply_markup=menu_keyboard_2stage(msg.chat.id))

    #блок ключевых слов
    @bot.message_handler(commands=['mykeywords'])
    async def kwrdupdt(msg:Message):
            if msg.chat.type=='private':
                keywords= get_user_and_keywords(msg.from_user.id)

                print(keywords)

                if len(keywords)==0:
                   await  bot.send_message(msg.chat.id,'💥🔦 <b>Мои ключевые слова</b>\n\nВ данный момент у тебя нет ключевых '
                                                   'слов и фраз.',parse_mode='html',reply_markup=adddelete_keywords('addonly'))

                elif len(keywords)>0:
                    keywords_showing=[]
                    for key in keywords:
                          keywords_showing.append(' '.join(key))
                    keywords_showing='\n'.join(keywords_showing)
                    await   bot.send_message(msg.chat.id,f'💥🔦 <b>Мои ключевые слова</b>\n\n{keywords_showing}',
                                      parse_mode='html',reply_markup=adddelete_keywords())

            #to do: убирать ключевые слова по клвавиатуре и добавлять по next step handler

    async def add_delete_keyword_handler(callback):
            await bot.edit_message_text('Добавьте ваше новое ключевое слово\n'
                                  'Только <b>одно</b> слово на одной строке!\n'
                                  'Например ->\n\nipad 3 mini\niphone 10s\nairpods 2'
                                  , callback.message.chat.id, callback.message.id,
                                  parse_mode='HTML')
            await bot.send_message(callback.message.chat.id,'И затем жми отправить')
            print(callback.from_user.id, callback.message.chat.id)
            # await bot.register_next_step_handler(callback.message,add_new_keyword)
            await bot.set_state(chat_id=callback.from_user.id,state=SuperStates.getkeyword,user_id=
                                              callback.message.chat.id)

    @bot.message_handler(state=SuperStates.getkeyword)
    async def add_new_keyword(msg:Message):

            print('state slovil')

            if '\n' in msg.text:
                newkeywordslist=msg.text.lower().split('\n')
                print(newkeywordslist)
                newkeyword=[]
                for keyword in newkeywordslist:
                    newkeyword=keyword.split(' ')

                    if add_delete_keyword(msg.chat.id, newkeyword, 'add') == 'added':
                         await bot.send_message(msg.chat.id, f'Ключевое слово {keyword} успешно добавлено!',reply_markup=menu_keyboard_2stage(msg.chat.id))

                    else:
                            await bot.send_message(msg.chat.id,
                                 'Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n' + premium_offer,
                                 reply_markup=menu_keyboard_2stage(msg.chat.id))
                            break
                await bot.delete_state(msg.from_user.id, msg.chat.id)
            elif '\n' not in msg.text:
                    newkeyword = msg.text.lower().split(' ')
                    if add_delete_keyword(msg.chat.id,newkeyword,'add') =='added':
                        await bot.send_message(msg.chat.id,'Ключевое слово успешно добавлено!',reply_markup=menu_keyboard_2stage(
                          msg.chat.id))
                        await bot.send_message(msg.chat.id, 'Добавим еще?',
                                      reply_markup=adddelete_keywords('addonly'))
                    await bot.delete_state(msg.from_user.id, msg.chat.id)
            else:
                await bot.send_message(msg.chat.id, '❌Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n'+premium_offer,reply_markup=menu_keyboard_2stage(msg.chat.id))
                await bot.delete_state(msg.from_user.id, msg.chat.id)

    @bot.message_handler(commands=['keywordslist_clear'])
    async def kwrd_list_del(callback):
        print('pltcm')
        if callback.message.chat.type == 'group':
            pass
        else:
             if add_delete_keyword(callback.message.chat.id,keyword=None,action='clear_list') == 'keywords_clear':
                 await bot.edit_message_text('Ваш список ключевых слов очищен',callback.message.chat.id,callback.message.id,reply_markup=adddelete_keywords('addonly'))
             else:
                  await bot.edit_message_text('Чтото не так со списком', callback.message.chat.id, callback.message.id)

        #банлист

    # логика блока бана
    @bot.message_handler(commands=['banlist_show'])
    async def block_list_show(msg:Message):
            if msg.chat.type=='group':
                pass
            else:
                print(msg.message_id)
                blocklist=add_delete_get_clear_blocked_users(user_id=msg.from_user.id,action='getall')
                print(len(blocklist))
                if len(blocklist)==0:
                         await bot.send_message(msg.chat.id,'⛔ Заблокированные люди\n\nУпс,список пока пуст',reply_markup=menu_keyboard_2stage(msg.chat.id))

                else:
                     await bot.send_message(msg.chat.id,banlist_preview
                                                 ,reply_markup=banlistmarkup(msg.from_user.id,blocklist))

    @bot.message_handler(commands=['banlist_clear'])
    async def block_list_clear(msg:Message):
            if msg.chat.type=='group':
                pass
            else:
                # print(msg.message_id)
                blocklist=add_delete_get_clear_blocked_users(user_id=msg.from_user.id,action='getall')
                # print(len(blocklist))
                if len(blocklist)!=0:
                   if add_delete_get_clear_blocked_users(user_id=msg.from_user.id, action='clear')==3:
                         await bot.send_message(msg.chat.id,'⛔ Блок-лист успешно очищен🧹')

                else:
                     await bot.send_message(msg.chat.id,'⛔Блок-лист пока пуст ')



    # Модуль оплаты премиума

    @bot.pre_checkout_query_handler(func=lambda query: True)
    async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
        print(pre_checkout_query)
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,error_message='Что-то не так')


    @bot.message_handler(content_types=['successful_payment'])
    async def process_successful_payment(msg: Message):
        # print('successful_payment')
        # print(msg)
        # message=json.dumps(message,ensure_ascii=False)
        if str(msg.from_user.id).lower() in str(msg.successful_payment.invoice_payload):
            if controling_premium(msg.from_user.id, new_premium_status=True) == 2:
                await bot.send_message(msg.chat.id, premium_purchase_ok,
                                 parse_mode='HTML')

        elif str(msg.from_user.id).lower()  not in str(msg.successful_payment.invoice_payload):
            user_pay=str(msg.successful_payment.invoice_payload)[12:]
            print(user_pay)
            if controling_premium(user_pay, new_premium_status=True) == 2:
                await bot.send_message(msg.chat.id, premium_purchase_ok,
                                 parse_mode='HTML')

        # логика кнопок

































    # #-----------------------------------------------------------------------------------------------------------------
    #                             ПРОВЕРКА ПОТОКА СООБЩЕНИЙ
    #     чекать все смс из чатов
    @bot.message_handler(func=lambda msg:Message )
    async def messagecheck(msg):
            print(msg.text,msg.chat.id,msg.chat.type)
            if msg.chat.type =='private':
                if add_users_field(msg.from_user.id,msg.from_user.username,msg.chat.id)!='new added':
                    if out_premium_check(msg.chat.id) in ['skip_prem','skip_notprem']:
                        print( out_premium_check(msg.chat.id))
                        if 'Главное меню' in msg.text:
                            # print(22)
                            await bot.send_message(msg.chat.id, text=f'Главное меню:', reply_markup=menu_keyboard_1stage())
                        elif 'Продавать товар' in msg.text:
                            await sell(msg)
                            # await bot.send_message(msg.chat.id, text=f'Продавать товар:', reply_markup=menu_keyboard_2stage(msg.chat.id))
                            # await bot.send_message(msg.chat.id,'продажа')

                        elif 'Блок-лист' in  msg.text:
                            # bot.send_message(msg.chat.id,'Раздел Блок-лист в разработке')
                             await block_list_show(msg)
                        elif 'Выбрать товары'in msg.text:
                            # print("yes")
                            # bot.send_message(msg.chat.id,'Раздел Выбрать товары в разработке')
                            await bot.send_message(msg.chat.id, 'Какие сообщения по товарам получать?',
                                             reply_markup=choosing_keyboard_proccess(msg.chat.id,level='memory'))
                        elif  'Premium-тариф' in msg.text:
                            if prem_status(msg.chat.id)==True:
                                await bot.send_message(msg.chat.id,f'Ваш Premium-тариф активен\n\n '
                                                             f'Осталось {out_premium_check(msg.chat.id,action=True)} дней ',
                                                 reply_markup=menu_keyboard_2stage(
                                                             msg.chat.id))
                            else:
                                await bot.send_message(msg.chat.id, premium_promo+'\n❗❗ВНИМАНИЕ❗❗\n'+premium_promo1,parse_mode='HTML',reply_markup=getfreepremium())
                                # await bot.send_invoice(msg.chat.id, 'Premium-тариф', f'\n\n⏬⏬Оплатить {msg.from_user.first_name} '\
                                #                                                f'Premium на '\
                                #                                                f'30 дней⏬⏬',
                                #                                                   f'buy_premium'
                                #                                                                    f'_{msg.from_user.id}',
                                #                  token_yukassa_payment_GorbushkinService, 'RUB', [LabeledPrice(
                                #         'Купить', 100 * 100)])
                        elif 'Руководство' in msg.text:
                            await bot.send_message(msg.chat.id, support_info, parse_mode='HTML' )

                        elif  'Ключевые слова' in msg.text:
                              print('кл сл')
                              await kwrdupdt(msg)
                        elif  'Продажи на паузу'in msg.text:
                            getchangeplaystatus(msg.chat.id,action=0)
                            await bot.send_message(msg.chat.id, 'Продажи приостановлены',reply_markup=menu_keyboard_2stage(msg.chat.id))
                        elif 'руководство бота' in msg.text.lower():
                            await  support_handler(msg)
                            # bot.send_message(msg.chat.id, 'Раздел продажи на паузу в разработке')
                        elif 'Возобновить продажи' in msg.text:
                             getchangeplaystatus(msg.chat.id, action=1)
                             await bot.send_message(msg.chat.id, 'Продажи возобновлены',reply_markup=menu_keyboard_2stage(msg.chat.id))
                        # elif 'Статистика запросов' in msg.text :
                        #     # print(msg.chat)
                        #     bot.send_message(msg.chat.id, 'Раздел Статистика запросов в разработке')
                        else:
                             await bot.send_message(msg.chat.id,"ты ввел что то не то, выбери что-то из этого списка",reply_markup=menu_keyboard_2stage(msg.chat.id))
                    else:
                        await bot.send_message(msg.chat.id,'Упс, ваш Premium-период истек.\n\n'
                                                     'Количество ваших ключевых слов и выбранных товаров сократилось до 1.'
                                                     '\n\n'
                                                     'Желаете Продлить ? - кликните на '
                                                     '<b>Premium-тариф</b>',
                                         parse_mode='HTML')
                        await messagecheck(msg=msg)

                else:
                    await welcome(msg)
            if 'group' in msg.chat.type:
                # print(msg)
                #По тех причинам мы не в состоянии связаться с человеком если отсутствует никнейн добавляте себе его и мы
                # обязатьно с вами свяжемся


                Text = msg.text
                print("Text-",Text)
                sender_id = msg.from_user.id
                sender_username = msg.from_user.username
                print('sender_id sender_username',sender_id,sender_username)
                crdtl = 'None'
                if ("_@_set") in Text:
                    crdtl = Text[Text.index('set_@_'):Text.index('_@_set') + 6]
                    Text = Text[Text.index('_@_set') + 6:]
                    # crdtl = crdtl.split('_@_')
                    crdtl = crdtl.split('_@_')
                    sender_id = crdtl[1]
                    sender_username = crdtl[2]
                else:
                    print("_@_set not in Text" )

                message_correct=Text.lower()
                print('сооьщ до полного перевода на англ',message_correct)
                message_correct=message_correct.split(' ')
                # print(message_correct)
                for item in message_correct:
                    if item in russiandict.keys():
                        # print('yes',item)
                        message_correct.insert(message_correct.index(item),russiandict[item])
                        message_correct.remove(item)
                message_correct=' '.join(message_correct)
                print('а теперь после полного преервода',message_correct)
                users_and_keywords=[]
                def users_and_keywords_list(access_sending:tuple,users_and_keywords:list):
                    for user_id in  access_sending:
                        print(user_id)
                        userkwrd=get_user_and_keywords(user_id,checking=True)
                        print(userkwrd)
                        users_and_keywords.append(userkwrd)
                        print('сейчас в польз и их словах ==',users_and_keywords)
                    print(users_and_keywords)
                    return tuple(users_and_keywords)


                # проверяем sender на наличие хоть у кого то в банлисте и высылаем список  тех у кого у он не в бане
                access_sending = get_users_without_sendusermsg_in_blocklist(sender_id)
                print('наши пользователи у которых отправитель не найден в блок листе ',access_sending)
                # кортеж из юзера нашего бота и его ключевых слов ,теперь включая все слова, которые в разделе выбор
                # товаров
                checkinglist = users_and_keywords_list(access_sending,users_and_keywords)
                print('кого и по чему проверка',checkinglist)

                # начало проверки
                for user_keys in checkinglist:

                    user_id_to=int(user_keys[0])
                    keywords_check=user_keys[1]
                    print(user_id_to)
                    print('список проверяемых слов ',keywords_check)

                    with open('IPHONE_LIST.json', 'r') as f:
                        productlist = json.load(f)
                    priorities_model=[]
                    priorities_color=[]
                    priorities_memories=[]
                    for product in tuple(productlist.keys()):
                        years=productlist[product]
                        for year in tuple(years.keys()):
                            models=years[year]
                            for model in models:
                                if model not in priorities_model:
                                    priorities_model.append(model)
                                specs=models[model]
                                for spec in specs:
                                    colors=specs[spec]
                                    for color in colors:
                                        if color not in priorities_color:
                                            priorities_color.append(color)
                                        memories=colors[color]
                                        for memory in memories:
                                            if memory not in priorities_memories:
                                                priorities_memories.append(memory)



                    # print(priorities_model)
                    # print(priorities_color)
                    # print(priorities_memories)

                    priorities=priorities_memories+priorities_color+priorities_model
                    # print(priorities)


                    for kwrd in keywords_check:
                        print('clovo',kwrd)
                        need_send = []
                        guarantee=0
                        for key in kwrd:
                            print('elslova',key)
                            if str(key).lower() in  message_correct.lower():

                                need_send.append(1)
                                if str(key).lower() in priorities:
                                    guarantee+=1
                            else:
                                # if str(key).lower() not in priorities:
                                    need_send.append(0)

                        print(need_send,guarantee,message_correct,user_id_to)
                        # print(need_send,not_need,sender_id,user_id_to)
                        if sender_username == 0 and sender_id == 0:
                            sender_username = msg.from_user.username
                            sender_id = msg.from_user.id
                        print()
                        if 0 not in need_send or (0 in need_send and guarantee>=3):
                            # if user_id_to!=int(sender_id):
                                if getchangeplaystatus(user_id_to,action='get')!=0:

                                    print("sender_username:",sender_username,"      sender_id",sender_id,'  user_id_to',
                                          user_id_to)

                                    link_text = f"[{sender_username}](https://t.me/{sender_username})\n\n" \
                                                f"{Text}"
                                    try:
                                        await bot.send_message(user_id_to, link_text, parse_mode='Markdown', disable_web_page_preview=True,reply_markup=block_keyboard(sender_id,sender_username,banlist=None))
                                    except Exception as e:
                                        pass
                                    break
                                    pass
                        # else:
                        #     need_send = 0
                        #     not_need = 0

















    #-----------------------------------------------------------------------------------------------------------------
    #     Callback-логика
    @bot.callback_query_handler(func=lambda callback:callback.data)
    async def callback_logic(callback):
                # print(callback.data)
                # /логика бана
                if callback.data == 'banlist_show':
                        blocklist = add_delete_get_clear_blocked_users(user_id=callback.message.chat.id, action='getall')
                        if len(blocklist) == 0:
                             await bot.edit_message_text(f'⛔ Заблокированные люди\n\nНа данный момент ваш список пуст', callback.message.chat.id,
                                              callback.message.id)
                        else:
                             await bot.edit_message_text(f'⛔ Заблокированные люди от которых теперь вы не получаете сообщений в боте:\n\nОчистить всех /banlist_clear\n\nУдалить человека из Блок-листа - выберите пользователя ниже',
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
                             await bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,None))
                    else:
                        for ban_item in blocklist:
                            if block_id  not in ban_item:
                                need_ban.append(1)
                            else :
                                need_ban.append(0)
                        print('need_ban',need_ban)
                        if 1 in need_ban:
                            if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                                await bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,
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
                              await bot.edit_message_text(f'🔒 {block_name} заблокирован(a)\n❌И сообщения от него больше поступать не будут',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,True))
                    else:
                        for ban_item in blocklist:
                            if block_id  not in ban_item:
                                need_ban.append(0)
                            else :
                                need_ban.append(1)
                        print(need_ban)
                        if 1 not in need_ban:
                            if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                              await bot.edit_message_text(f'🔒 {block_name} заблокирован(a)\n❌И сообщения от него больше поступать не будут',callback.message.chat.id,callback.message.id,reply_markup=unblock_keyboard(block_id, block_name,True))
                            elif     add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')=='2.1':
                                await bot.edit_message_text(
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
                        await bot.edit_message_text(
                            f'✅ {unblock_name} разблокирован(a)',
                            callback.message.chat.id, callback.message.id,
                            reply_markup=block_keyboard(block_id=unblock_id, block_name=unblock_name, banlist=None))
                    else:
                        for ban_item in add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'getall'):
                            print('1====')
                            if unblock_id in ban_item:
                                print(unblock_id,'Eсть в списке')
                                if add_delete_get_clear_blocked_users(unblock_id,unblock_name,callback.message.chat.id,'delete')==2 :
                                    await bot.edit_message_text(f'✅ {unblock_name} разблокирован(a)', callback.message.chat.id, callback.message.id,
                                reply_markup=block_keyboard(block_id= unblock_id,block_name= unblock_name,banlist=None))
                            else:
                                await bot.edit_message_text(
                                f'✅ {unblock_name} разблокирован(a)',
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
                                    await bot.edit_message_text(f'🔓 {unblock_name} разблокирован(a) \n✅Теперь вы можете получать от него сообщения', callback.message.chat.id, callback.message.id, reply_markup=block_keyboard(block_id=unblock_id,block_name=unblock_name,banlist=True))

                elif callback.data=="add_keyword":
                    await  add_delete_keyword_handler(callback)
                elif callback.data in 'delete_keywords':
                    await kwrd_list_del(callback)
                     #временная раздача халявы
                elif callback.data == "free_premium":
                    await bot.delete_message(callback.message.chat.id, callback.message.id )
                    if controling_premium(callback.message.chat.id, True) in [2, 1]:
                       await bot.send_message(callback.message.chat.id, premium_bonus, parse_mode='HTML')

                elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepyear'):
                    product_name=callback.data.split('_')[1]
                    await bot.edit_message_text(
                        'Какие сообщения по товарам получать?',
                        callback.message.chat.id, callback.message.id,parse_mode="HTML",
                        reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'year',callback.data,{f'{product_name}':f'✅'}))


                elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepmemory'):
                    # product_name = callback.data.split('_')[1]
                    # product_year = callback.data.split('_')[2]

                    await bot.edit_message_text(
                    # f'Товар: <b>{product_name.capitalize()}</b>✅\n' \
                    # f'Год линейки: {product_year} ✅\n' \
                    # f'Теперь укажите серию, цвет, память ⤵',
                        'Какие сообщения по товарам получать?',
                    callback.message.chat.id, callback.message.id, parse_mode = "HTML",
                    reply_markup = choosing_keyboard_proccess(callback.message.chat.id, 'memory', callback.data))

                elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_add'):
                    print(callback.data)
                    product_name = callback.data.split('_')[1]
                    product_year = callback.data.split('_')[2]
                    product_model=callback.data.split('_')[3]
                    print(product_name,product_year,product_model)

                    product_spec = callback.data.split('_')[4]
                    product_color=callback.data.split('_')[5]
                    product_memory = callback.data.split('_')[6]






                    if product_spec == 'orig':
                                new_choosed_item = {f'{product_name}_{product_year}_{product_model}_{product_spec}_{product_color}'
                                                    f'_{product_memory}':[
                                    product_name,product_model,product_color,product_memory]}

                    else:
                                new_choosed_item = {f'{product_name}_{product_year}_{product_model}_{product_spec}_{product_color}'
                                                    f'_{product_memory}':[
                                    product_name,product_model,product_spec,product_color,product_memory]}
                    print(new_choosed_item)
                    if prem_status(callback.message.chat.id)==True:
                        get_add_del_choosed_item(callback.message.chat.id,"add",new_choosed_item)
                        await bot.edit_message_text('Какие сообщения по товарам получать?', callback.message.chat.id,
                                              callback.message.id,
                                              reply_markup=choosing_keyboard_proccess(callback.message.chat.id,
                                                                                      level='memory',
                                                                                      construct=f'construct_{product_name}_{product_year}_stepmemory'))

                    else:
                        if len(tuple( get_add_del_choosed_item(callback.message.chat.id,"get").keys()))<1:
                            print('проблема',len(tuple( get_add_del_choosed_item(callback.message.chat.id,"get").keys())))
                            get_add_del_choosed_item(callback.message.chat.id, "add", new_choosed_item)
                            await bot.edit_message_text('Какие сообщения по товарам получать?', callback.message.chat.id,
                                                  callback.message.id,
                                                  reply_markup=choosing_keyboard_proccess(callback.message.chat.id,
                                                                                          level='memory',
                                                                                          construct=f'construct_{product_name}_{product_year}_stepmemory'))

                        else:
                            # bot.edit_message_text(premium_offer, callback.message.chat.id,
                            #                       callback.message.id)
                            await bot.send_message(callback.message.chat.id,premium_offer)


                            # else:


                    # else:
                    #         bot.edit_message_text(
                    #          f'<b>Лимит на добавление ключевых слов превышен❌ </b>\n\n'+Text_of_messages.premium_offer,
                    #                 callback.message.chat.id, callback.message.id, parse_mode="HTML")


                elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_delete'):
                    print(callback.data)
                    product_name = callback.data.split('_')[1]
                    product_year = callback.data.split('_')[2]
                    product_model = callback.data.split('_')[3]


                    product_spec = callback.data.split('_')[4]
                    product_color = callback.data.split('_')[5]
                    product_memory = callback.data.split('_')[6]

                    # print(product_name, product_year, product_model,product_spec,product_color,pr)
                    to_del=f'{product_name}_{product_year}_{product_model}_{product_spec}_{product_color}'\
                                                    f'_{product_memory}'
                    if to_del in tuple(get_add_del_choosed_item(callback.message.chat.id,"get").keys()):
                        if get_add_del_choosed_item(callback.message.chat.id,"del",to_del)=='deleted':
                            await bot.edit_message_text('Какие сообщения по товарам получать?', callback.message.chat.id,  callback.message.id,
                    reply_markup = choosing_keyboard_proccess(callback.message.chat.id,
                                                              level='memory',
                                                              construct=f'construct_{product_name}_{product_year}_stepmemory'))


    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    await bot.polling(non_stop=True)





async def serverside(app):
    print('pfgeo')


    # Замените "TARGET_GROUP" на username или ID вашей группы
    # TARGET_GROUP = "-1001946865525"

    async def send_message_with_interval(app, chat_id, text, interval):

        await asyncio.sleep(interval)
        await app.send_message(chat_id=chat_id, text=text)



    @app.on_message()
    async def forward_to_private_chat(app, message):

        if int(message.from_user.id)!=6724529493:
            if int(message.chat.id) != -1001869659170:
                CANAL=message.chat.title
                user_id=message.from_user.id
                text=message.text
                resolve=json.loads  (str(message.from_user))

                if 'username' in resolve.keys():
                    if 'bot' not in text.lower() and "True"  not in str(resolve['is_bot']):
                        usrnm = message.from_user.username
                        if any(keyword in text.lower() for keyword in ['куплю', 'предложите', 'ищу','?']):
                            # print('-------------\n',resolve['username'])
                            # print(message.text)

                                task_list.append(send_message_with_interval(app, -1001869659170,
                                f'set_@_{user_id}_@_{usrnm}_@_set{CANAL}\n\n{message.text}', 2))






                            # await  app.send_message(text=f'set_@_{user_id}_@_{usrnm}_@_set' \
                            #                       f'{message.text}', chat_id=-1001869659170)
                            # except Exception as e:
                            #     print(e)

async def checking ():
    global wait_seconds
    wait_seconds=1
    while True:
        from pyrogram.errors.exceptions.flood_420 import FloodWait

        await asyncio.sleep(1)
        print('таски=',task_list,len(task_list))
        if len(task_list)>=5:
            for task in task_list.copy():
                await asyncio.sleep(wait_seconds)
                try:
                       await task
                       task_list.remove(task)
                       wait_seconds=1

                except Exception as error_message:
                    print(error_message)
                    async def extract_flood_wait_seconds(error_message):
                        # Паттерн для поиска числа (количество секунд) в сообщении об ожидании
                        pattern = r'A wait of (\d+) seconds is required'

                        # Поиск совпадений в сообщении об ошибке
                        match = re.search(pattern, error_message)

                        if match:
                            # Извлечение числа из совпадения и преобразование в int
                            seconds = int(match.group(1))
                            return seconds
                        else:
                            # Если совпадения не найдены, вернуть None или другое значение по умолчанию
                            return None

                    # Пример использования
                    # error_message = 'Telegram says: [420 FLOOD_WAIT_X] - A wait of 55 seconds is required (caused by "messages.SendMessage")'
                    wait_seconds = await extract_flood_wait_seconds(error_message)
                    print(wait_seconds)


















            print("done")

async def main():
    global task_list
    task_list=[]
    app = Client("salesbot")
    bot = AsyncTeleBot(token=token_GorbushkinService,
                       state_storage=STM())

    await asyncio.gather (asyncio.create_task(checking()),asyncio.create_task(serverside(await app.start())),
                          asyncio.create_task(clientside(bot)))


    # Запуск бота в бесконечном цикле
if __name__ == '__main__':
    asyncio.run(main())

















