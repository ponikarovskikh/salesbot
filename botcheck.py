from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage as STM
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import StatesGroup as STSGR,State as ste
from Text_of_messages import *
from config import *
from keyboards import *
from sqlfile import *
import asyncio
from pyrogram import Client,methods as MTHPYRO

import openpyxl
global app
global bot
import pandas as pd
import time
from apscheduler.schedulers.background import BackgroundScheduler


global last_message_len1
last_message_len1 = {}

async def clientside(bot):
        class SuperStates(STSGR):
            getkeyword = ste()
            getnewprice=ste()
            getnamemail=ste()
            getcontentmail=ste()
            getpricelist=ste()

            add_new_admin=ste()
            add_new_seller=ste()


        # прайслист
        @bot.message_handler(state=SuperStates.getpricelist,content_types=['document'])
        async def pricelistprocess(msg):
            chat_id = msg.chat.id
            user_id = msg.from_user.id

            username=msg.from_user.username
            if username is None:
                await bot.send_message(msg.chat.id,'Упс у вас не указан Юзернэйм в вашем Tелеграмм-профиле,'
                                                'без него никак. Укажите его и повторите попытку. ')
                await bot.delete_state(msg.from_user.id, msg.chat.id)
                pass
            else:
                try:
                    file_info =await bot.get_file(msg.document.file_id)
                    # print(file_info)
                    downloaded_file =await bot.download_file(file_info.file_path)
                    # print(downloaded_file,'down-')
                except Exception as e:
                    print(e)

                file_name = 'temp.xlsx'
                with open(file_name, 'wb') as new_file:
                    new_file.write(downloaded_file)

                try:
                    df = pd.read_excel(file_name, usecols='A:B')
                    # print(df, 'df')
                    data = [(row) for index, row in df.iterrows()]
                    print(data, 'писок')
                    create_table_and_insert_data(user_id, data,username)
                    print('утка')
                    await bot.send_message(chat_id, "Ваш новый прайслист сохранен✅")
                    await bot.send_message(chat_id,autocall_text,parse_mode='html',
                    reply_markup=pricelistmenu( msg.from_user.id))
                except Exception as e:
                    await bot.send_message(chat_id=-4010327668, text=f"Ошибка при обработке файла: {e}")

                if os.path.exists(file_name):
                    os.remove(file_name)

        # admin_control

        @bot.message_handler(state=SuperStates.add_new_admin)
        async def add_admin(msg:Message):
            new_admin_user=msg.text
            if all_permissions(action='add',new_admin_id=new_admin_user)== 'admin added':
                await bot.send_message(msg.chat.id,f'Админ {new_admin_user} добавлен')
            elif all_permissions(action='add',new_admin_id=new_admin_user) == 'added yet':
                await bot.send_message(msg.chat.id, f'Админ {new_admin_user} уже в списке админов')
            await bot.delete_state(msg.from_user.id, msg.chat.id)

        @bot.message_handler(state=SuperStates.add_new_seller)
        async def add_autoseller(msg: Message):
            new_seller_user = msg.text
            if "@" not in new_seller_user:
                await bot.send_message(msg.chat.id, f'Не получется обработать. \n'
                                                    f'Введите еще раз,например: '
                                                    f'@shop_username')


            if all_permissions(action='add', new_autoseller_id=new_seller_user) == 'added seller':
                await bot.send_message(msg.chat.id, f'Продавец {new_seller_user} добавлен')
                await bot.delete_state(msg.from_user.id, msg.chat.id)
            elif all_permissions(action='add', new_autoseller_id=new_seller_user) == 'added yet':
                await bot.send_message(msg.chat.id, f'Админ {new_seller_user} уже в списке продавцов')
                await bot.delete_state(msg.from_user.id, msg.chat.id)

        # @bot.message_handler(commands=['admininfo'])
        async def userslist(msg: Message):
            admins=all_permissions('get_admins')
            if msg.from_user.id in admins:
                all_users,all_users_play,users_premium_list=all_users_list()
                # sum,price,last_month,quant_sold,last_year = profit_calc()

                await bot.send_message(msg.chat.id,parametrs_info.format(all_users,all_users_play,users_premium_list
                                                                         ),
                                       parse_mode='HTML')

        @bot.message_handler(commands=['global_stop'])
        async def global_stop(msg: Message):
            if msg.from_user.id==704718950:
                if stop_function('change') is True:
                    text='Работает'
                else:
                    text='Приостановлен'
                await bot.send_message(msg.chat.id,f'Функционал бота {text}',
                                                                             parse_mode='HTML')








        @bot.message_handler(commands=['setprice'])
        async def pricesetinit(msg: Message):
            admins = all_permissions()
            if msg.from_user.id in admins:
                await bot.send_message(msg.chat.id,f'Укажите новую цену Premium')
                await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.getnewprice, user_id=
                msg.chat.id)

        @bot.message_handler(state=SuperStates.getnewprice)
        async def pricesetprocess(msg: Message):
            price=msg.text
            try:
                # Try to convert the text to an integer
                value = int(price)
                if  setprice('set',value) == 1:
                    await  bot.send_message(msg.chat.id, f'Новая цена Premium: {price} руб')
                await bot.delete_state(msg.from_user.id, msg.chat.id)
            except ValueError:
                await bot.send_message(msg.chat.id, f'Что-то не так, введите стоимость еще раз')
                await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.getnewprice, user_id=
                msg.chat.id)

        @bot.message_handler(commands=['mail'])
        async def mailing(callback):
            await bot.send_message(callback.message.chat.id, f'Напишите название вашей будущей рассылки ')
            print(callback.message.chat.id,callback.from_user.id)
            await bot.set_state(chat_id=callback.from_user.id, state=SuperStates.getnamemail, user_id=
                callback.message.chat.id)
            async with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
                    data['namemail'] = None
                    data['contentmail'] = None
                    print('mailing',data)


        @bot.message_handler(state=SuperStates.getnamemail)
        async def mailingnameprocess(msg):
            name=msg.text
            print(name)
            # await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.getnamemail, user_id=
            # msg.chat.id)
            async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                print('mailingnameprocess',data)
                data['namemail'] = name
                content=data['contentmail']
                if  data['contentmail'] is None:
                    await bot.send_message(msg.chat.id, f'Наберите текст рассылки {str(name).capitalize()}')
                    await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.getcontentmail, user_id=
                    msg.chat.id)
                    print('Привет',data)

                else:
                    await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.getcontentmail, user_id=
                    msg.chat.id)
                    async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                        data['namemail'] = name
                        # if data['contentmail'] is not None:
                        #     data['contentmail']=content

                    print('ты кто',data)
                    await mailingcontentprocess(msg)





        @bot.message_handler(state=SuperStates.getcontentmail)
        async def mailingcontentprocess(msg:Message,callback=None):
            if msg is not   None:
                content = msg.text
                async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                    if data['contentmail'] is None:
                        data['contentmail'] = content
                        print('ваш',data)
                    if  data['contentmail'] !=content and content != data['namemail']:
                        print('pltcm')
                        data['contentmail'] = content

                print('ailingcontentprocess finish  ',data)
                await bot.send_message(msg.chat.id, f'Вот так будет выглядеть ваша рассылка '
                                                    f'{data["namemail"].capitalize()}:\n\n'
                                                    f'{data["contentmail"]}',reply_markup=addmail_reject())
            else:
                async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                    await bot.send_message(msg.chat.id, f'Вот так будет выглядеть ваша рассылка '
                                                        f'{data["namemail"].capitalize()}:\n\n'
                                                        f'{data["contentmail"]}', reply_markup=addmail_reject())


        @bot.message_handler(commands=['start'])
        async def welcome(msg:Message):
            if stop_function() is True:
                if  'private' in msg.chat.type:

                    username = msg.from_user.username
                    user_id=msg.from_user.id
                    chat_id=msg.chat.id

                    await bot.send_message(msg.chat.id,text=f'Привет, {username}!\n\n{welcome_preview}')
                    if add_users_field(user_id, username,chat_id) =='new added':
                        await bot.send_message(msg.chat.id,'Так как вы впервые у нас, ознакомьтесь с функционалом в разделе '
                                                           '<b>Руководство📚</b>',  parse_mode='html', reply_markup=menu_keyboard_2stage(user_id))
                    else:
                       await  bot.send_message(msg.chat.id,'Друг, и снова здраствуй!',reply_markup=menu_keyboard_1stage())

        # @bot.message_handler(text=['Продавать товар'])





        # @bot.message_handler(commands=['support'])
        # async def  support_handler(msg:Message):
        #     # print('support')
        #     if msg.chat.type == 'private':
        #         await  bot.send_message(msg.chat.id, text=support_info, parse_mode='HTML',reply_markup=menu_keyboard_2stage(
        #             msg.chat.id))

            # Утилита для получения  айди самого себя
        # @bot.message_handler(commands=['ids'])
        # async def idsend(msg:Message):
        #         if msg.chat.type=='private':
        #             username = msg.from_user.username
        #             link = f"[{username}](https://t.me/{username})"
        #             await  bot.send_message(msg.chat.id, link, parse_mode='Markdown', disable_web_page_preview=True,
        #                               reply_markup=menu_keyboard_2stage(msg.chat.id))

        #блок ключевых слов
        # @bot.message_handler(commands=['mykeywords'])
        async def kwrdupdt(msg:Message):
                if msg.chat.type=='private':
                    keywords= get_user_and_keywords(msg.from_user.id)

                    # print(keywords)

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
                # print(callback.from_user.id, callback.message.chat.id)
                # await bot.register_next_step_handler(callback.message,add_new_keyword)
                await bot.set_state(chat_id=callback.from_user.id,state=SuperStates.getkeyword,user_id=
                                                  callback.message.chat.id)



















        @bot.message_handler(state=SuperStates.getkeyword)
        async def add_new_keyword(msg:Message):
                if '\n' in msg.text:
                    newkeywordslist=msg.text.lower().split('\n')
                    # print(newkeywordslist)
                    newkeyword=[]
                    for keyword in newkeywordslist:
                        newkeyword=keyword.split(' ')

                        if add_delete_keyword(msg.chat.id, newkeyword, 'add') == 'added':
                             await bot.send_message(msg.chat.id, f'Ключевое слово {keyword} успешно добавлено!',reply_markup=menu_keyboard_2stage(msg.chat.id))

                        else:
                                await bot.send_message(msg.chat.id,
                                     'Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n' + premium_offer,
                                     reply_markup=menu_keyboard_2stage(msg.chat.id))



                    # await bot.delete_state(msg.from_user.id, msg.chat.id)
                elif '\n' not in msg.text:
                        newkeyword = msg.text.lower().split(' ')
                        if add_delete_keyword(msg.chat.id,newkeyword,'add') =='added':
                            await bot.send_message(msg.chat.id,'Ключевое слово успешно добавлено!',reply_markup=menu_keyboard_2stage(
                              msg.chat.id))
                            await bot.send_message(msg.chat.id, 'Добавим еще?',
                                          reply_markup=adddelete_keywords('addonly'))

                        else:
                            await bot.send_message(msg.chat.id, '❌Ключевое слово не может быть добавлено, так как превышает лимит 1 из 1.\n\n'+premium_offer,reply_markup=menu_keyboard_2stage(msg.chat.id))
                await bot.delete_state(msg.from_user.id, msg.chat.id)

        # @bot.message_handler(commands=['keywordslist_clear'])
        async def kwrd_list_del(callback):
            # print('pltcm')
            if callback.message.chat.type == 'group':
                pass
            else:
                 if add_delete_keyword(callback.message.chat.id,keyword=None,action='clear_list') == 'keywords_clear':
                     await bot.edit_message_text('Ваш список ключевых слов очищен',callback.message.chat.id,callback.message.id,reply_markup=adddelete_keywords('addonly'))
                 else:
                      await bot.edit_message_text('Чтото не так со списком', callback.message.chat.id, callback.message.id)

            # банлист

        # логика блока бана
        # @bot.message_handler(commands=['banlist_show'])
        async def block_list_show(msg:Message):
                if msg.chat.type=='group':
                    pass
                else:
                    # print(msg.message_id)
                    blocklist=add_delete_get_clear_blocked_users(user_id=msg.from_user.id,action='getall')
                    # print(len(blocklist))
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
            print('successful_payment')
            print(msg.successful_payment)
            user_id=msg.successful_payment.invoice_payload.split('_')[2]
            bill=int(msg.successful_payment.total_amount)/100

            # print(date,user_id,amount/100)

            # message=json.dumps(message,ensure_ascii=False)
            if str(msg.from_user.id).lower() in str(msg.successful_payment.invoice_payload):
                if controling_premium(msg.from_user.id, new_premium_status=True) == 2:
                    await bot.send_message(msg.chat.id, premium_purchase_ok,
                                     parse_mode='HTML')


            elif str(msg.from_user.id).lower()  not in str(msg.successful_payment.invoice_payload):
                user_pay=str(msg.successful_payment.invoice_payload).split('_')[2]
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
            print(msg.from_user.username)
            if stop_function() is True:
                if msg.chat.type =='private':
                    if msg.from_user.username is None:
                        await bot.send_message(msg.chat.id, 'Извините,но для продолжения дальнейшей полноценной '
                                                            'работы бота укажите '
                                                            'ваше Имя Пользователя(username) в Телеграмм',
                                               parse_mode='HTML')

                    else:
                        if add_users_field(msg.from_user.id,msg.from_user.username,msg.from_user.id)!='new added':
                            if out_premium_check(msg.chat.id) in ['skip_prem','skip_notprem']:
                                # print( out_premium_check(msg.chat.id))
                                if msg.from_user.username in all_permissions('get_admins'):
                                    print('get_admins')
                                    if all_permissions('update',username_remove=msg.from_user.username,
                                                       new_admin_id=msg.from_user.id)=='admin id changed':
                                        await bot.send_message(msg.chat.id, text='Вам выдана роль Админа🛠',
                                                           reply_markup=menu_keyboard_2stage(msg.from_user.id))

                                if msg.from_user.username in all_permissions('get_autosellers'):
                                    print('get_autosellers')
                                    if all_permissions('update',username_remove=msg.from_user.username,
                                                       new_autoseller_id=msg.from_user.id)=='autoseller id changed':
                                        await bot.send_message(msg.chat.id, text='Вам выдан доступ к Автопродажам🤖',
                                        reply_markup = menu_keyboard_2stage(msg.from_user.id)  )
                                refresh_username(msg.from_user.id,msg.from_user.username)
                                if 'Главное меню' in msg.text:
                                    # print(22)
                                    await bot.send_message(msg.chat.id, text=f'Главное меню:', reply_markup=menu_keyboard_1stage())


                                elif 'Админ-панель' in msg.text:
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        await bot.send_message(msg.chat.id, text='Админ-панель',
                                                           reply_markup=admin_panel())

                                elif 'Назад' in msg.text:
                                    await bot.send_message(msg.chat.id, text='Главное меню',
                                                           reply_markup=menu_keyboard_2stage(msg.from_user.id))


                                elif 'Добавить админа' in msg.text:
                                    print( all_permissions('get_admins'))
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        await bot.send_message(msg.chat.id, text='Введите [@username](https://usernamе) '
                                                                                 'пользователя '
                                                                                 'Telegram',parse_mode='Markdown')
                                        await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.add_new_admin,
                                                            user_id=msg.chat.id)


                                elif 'Добавить продавца' in msg.text:
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        await bot.send_message(msg.chat.id, text='Введите [@username](https://usernamе) '
                                                                                 'пользователя '
                                                                                 'Telegram', parse_mode='Markdown')
                                        await bot.set_state(chat_id=msg.from_user.id, state=SuperStates.add_new_seller,
                                                            user_id=msg.chat.id)


                                elif 'Перейти на Бесплатный Premium'  in msg.text:
                                    print(123)
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        if premium_admin_switch('change')[1] is False:

                                            await bot.send_message(msg.chat.id, text='Оплата за Premium-тариф '
                                                                                     'отключена!\n'
                                                                                     'Действует '
                                                                                     'бесплатная раздача ',reply_markup=admin_panel())
                                elif 'Включить Платный Premium' in msg.text:
                                    print(456)
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        if premium_admin_switch('change')[1] is True:
                                            await bot.send_message(msg.chat.id, text='Оплата за Premium-тариф '
                                                                                     'включена ',reply_markup=admin_panel())






                                elif 'Продавать товар' in msg.text:
                                        await bot.send_message(msg.chat.id, text=f'Вы в разделе продажа товаров.\n\n'
                                                                                 f'Сюда будут приходить все сообщения о товарах согласно вашим '
                                                                                 f'ключевым словам.\n\n'
                                                                                 f'Для ознакомления работы бота нажмите Руководство',
                                                               reply_markup=menu_keyboard_2stage(msg.chat.id))

                                    # await bot.send_message(msg.chat.id, text=f'Продавать товар:', reply_markup=menu_keyboard_2stage(msg.chat.id))
                                    # await bot.send_message(msg.chat.id,'продажа')

                                elif 'Блок-лист' in  msg.text:
                                    # bot.send_message(msg.chat.id,'Раздел Блок-лист в разработке')
                                     await block_list_show(msg)



                                elif 'Выбрать товары'in msg.text:
                                    # print("yes")
                                    # bot.send_message(msg.chat.id,'Раздел Выбрать товары в разработке')
                                    await bot.send_message(msg.chat.id, 'Какие сообщения по товарам получать?',
                                                     reply_markup=choosing_keyboard_proccess(msg.chat.id,level='memory',
                                                                                             product_choosen='iphone'))









                                elif  'Premium-тариф' in msg.text:
                                    if prem_status(msg.chat.id)==True:
                                        await bot.send_message(msg.chat.id,f'Ваш Premium-тариф активен\n\n '
                                                                     f'Осталось {out_premium_check(msg.chat.id,action=True)} дней ',
                                                         reply_markup=menu_keyboard_2stage(
                                                                     msg.chat.id))
                                    else:
                                        if premium_admin_switch() is True:
                                            amount = (int(setprice('get')) * 100)
                                            await bot.send_invoice(msg.chat.id, 'Premium-тариф', f'Оплатить '

                                                                                                 f'Premium на 30 дней ',
                                                                   f'successful_payment_{msg.from_user.id}',
                                                                   token_yukassa_online_payment_GorbushkinService,
                                                                   'RUB', [LabeledPrice(
                                                    'Купить', amount)])
                                        else:
                                            await bot.send_message(msg.chat.id, premium_promo+'\n❗❗ВНИМАНИЕ❗❗\n'+premium_promo1,parse_mode='HTML',reply_markup=getfreepremium())
                                            print(setprice('get'),type(setprice('get')))

                                elif 'Руководство' in msg.text:
                                    await bot.send_message(msg.chat.id, support_info, parse_mode='HTML' )

                                elif  'Ключевые слова' in msg.text:
                                      # print('кл сл')
                                      await kwrdupdt(msg)
                                elif  'Продажи на паузу' in msg.text:
                                    getchangeplaystatus(msg.chat.id,action=0)
                                    await bot.send_message(msg.chat.id, 'Продажи приостановлены',reply_markup=menu_keyboard_2stage(msg.chat.id))

                                    # bot.send_message(msg.chat.id, 'Раздел продажи на паузу в разработке')
                                elif 'Возобновить продажи' in msg.text:
                                     getchangeplaystatus(msg.chat.id, action=1)
                                     await bot.send_message(msg.chat.id, 'Продажи возобновлены',reply_markup=menu_keyboard_2stage(msg.chat.id))
                                elif 'Статистика запросов' in msg.text :
                                    def get_current_date_numeric():
                                        current_date = datetime.now()
                                        return current_date.strftime("%d.%m")
                                    await bot.send_message(msg.chat.id, f'Cтатистика на {get_current_date_numeric()}')

                                    def format_products_for_message(products):
                                        message = "Список продуктов:\n"
                                        for product, count in products:
                                            # Удаляем 'iphone' из строки продукта
                                            product_without_iphone = product.replace('iphone ', '')
                                            message += f"   {product_without_iphone} - {count}\n"

                                        return message
                                    def split_message_for_telegram(text, max_length=4096):
                                        # Разделение текста на части по максимальной длине
                                        parts = []
                                        while len(text) > 0:
                                            # Если текст короче максимальной длины, добавляем его целиком
                                            if len(text) <= max_length:
                                                parts.append(text)
                                                break
                                            else:
                                                # Находим последний подходящий перенос строки
                                                split_index = text.rfind('\n', 0, max_length)
                                                if split_index == -1:
                                                    # Если перенос строки не найден, разбиваем по максимальной длине
                                                    split_index = max_length

                                                # Добавляем часть текста в список
                                                parts.append(text[:split_index])
                                                # Удаляем добавленную часть из исходного текста
                                                text = text[split_index:]

                                        return parts
                                    products=addinf_pos(action='get')
                                    # Форматирование сообщения
                                    formatted_message = format_products_for_message(products)

                                    # Разделение сообщения на части
                                    message_parts = split_message_for_telegram(formatted_message)
                                    for item in message_parts:
                                        await bot.send_message(msg.chat.id, item)




                                elif 'Изменить цену Premium' in msg.text:
                                    await  pricesetinit(msg)
                                elif 'Сводка' in msg.text:
                                    await  userslist(msg)
                                elif 'Рассылка' in msg.text:
                                    if msg.from_user.id in all_permissions('get_admins'):
                                        await  bot.send_message(msg.chat.id,'Раздел Рассылок',reply_markup=mailmenu())
                                elif 'Автопродажи' in msg.text:
                                    if msg.from_user.id in  all_permissions('get_autosellers'):
                                        await  bot.send_message(msg.chat.id, autocall_text,
                                                            parse_mode='html',
                                                            reply_markup=pricelistmenu(msg.chat.id))
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
                    # print("Text-",Text)
                    sender_id = msg.from_user.id
                    sender_username = msg.from_user.username
                    # print('sender_id sender_username',sender_id,sender_username)
                    crdtl = 'None'
                    if ("_@_set") in Text:
                        crdtl = Text[Text.index('set_@_'):Text.index('_@_set') + 6]
                        Text = Text[Text.index('_@_set') + 6:]
                        # crdtl = crdtl.split('_@_')
                        crdtl = crdtl.split('_@_')
                        sender_id = crdtl[1]
                        sender_username = crdtl[2]
                    else:
                        print("_@_set not in Text")

                    message_correct=Text.lower()
                    # print('сооьщ до полного перевода на англ',message_correct)
                    message_correct=message_correct.split(' ')
                    # print(message_correct)
                    for item in message_correct:
                        if item in russiandict.keys():
                            # print('yes',item)
                            message_correct.insert(message_correct.index(item),russiandict[item])
                            message_correct.remove(item)
                    message_correct=' '.join(message_correct)

                    # with open('IPHONE_LIST.json', 'r') as f:
                    #     productlist = json.load(f)
                    # priorities_model = []
                    # priorities_color = []
                    # priorities_memories = []
                    #
                    # years = productlist['iphone']
                    # for year in tuple(years.keys()):
                    #         models = years[year]
                    #         for model in models:
                    #             if model not in priorities_model:
                    #                 priorities_model.append(model)
                    #             specs = models[model]
                    #             for spec in specs:
                    #                 colors = specs[spec]
                    #                 for color in colors:
                    #                     if color not in priorities_color:
                    #                         priorities_color.append(color)
                    #                     memories = colors[color]
                    #                     for memory in memories:
                    #                         if memory not in priorities_memories:
                    #                             priorities_memories.append(memory)

                    # print(priorities_color)
                    # print(priorities_memories)

                    # priorities = priorities_memories + priorities_color + priorities_model
                    if 'airpods' in message_correct:
                        prio=priorities['airpods_prio']
                    elif 'iphone' in message_correct:
                        prio=priorities['iphone_prio']
                    addinf_pos(text=message_correct,priorities=prio)









                                       # print('а теперь после полного преервода',message_correct)
                    users_and_keywords=[]
                    def users_and_keywords_list(access_sending:tuple,users_and_keywords:list):
                        for user_id in  access_sending:
                            # print(user_id)
                            userkwrd=get_user_and_keywords(user_id,checking=True)
                            # print(userkwrd)
                            users_and_keywords.append(userkwrd)
                            # print('сейчас в польз и их словах ==',users_and_keywords)
                        # print(users_and_keywords)
                        return tuple(users_and_keywords)


                    # проверяем sender на наличие хоть у кого то в банлисте и высылаем список  тех у кого у он не в бане
                    access_sending = get_users_without_sendusermsg_in_blocklist(sender_id)
                    # print('наши пользователи у которых отправитель не найден в блок листе ',access_sending)
                    # кортеж из юзера нашего бота и его ключевых слов ,теперь включая все слова, которые в разделе выбор
                    # товаров
                    checkinglist = users_and_keywords_list(access_sending,users_and_keywords)
                    # print('кого и по чему проверка',checkinglist)

                    # начало проверки
                    for user_keys in checkinglist:

                        user_id_to=int(user_keys[0])
                        keywords_check=user_keys[1]
                        # print(user_id_to)
                        # print('список проверяемых слов ',keywords_check)


                        # print(priorities)


                        for kwrd in keywords_check:
                            # print('clovo',kwrd)
                            need_send = []
                            guarantee=0
                            for key in kwrd:
                                # print('elslova',key)
                                if str(key).lower() in  message_correct.lower():

                                    need_send.append(1)
                                    if str(key).lower() in prio:
                                        guarantee+=1
                                else:
                                    # if str(key).lower() not in priorities:
                                        need_send.append(0)

                            # print(need_send,guarantee,message_correct,user_id_to)
                            # print(need_send,not_need,sender_id,user_id_to)
                            if sender_username == 0 and sender_id == 0:
                                sender_username = msg.from_user.username
                                sender_id = msg.from_user.id
                            # print()
                            if 0 not in need_send or (0 in need_send and guarantee>=2):
                                # if user_id_to!=int(sender_id):
                                    if getchangeplaystatus(user_id_to,action='get')!=0:

                                        # print("sender_username:",sender_username,"      sender_id",sender_id,'  user_id_to',
                                              # user_id_to)

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
            if stop_function() is True:
                    # print(callback.data)
                    # логика бана
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
                        print(callback.data)
                        clback=callback.data.split('_')
                        # print(clback)
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
                            if 0 not in need_ban:
                                if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                                    await bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,
                                                          callback.message.id,reply_markup=unblock_keyboard(block_id,
                                                                                                            block_name,None))
                            else:
                                if add_delete_get_clear_blocked_users(block_id=block_id,block_name= block_name, user_id= callback.from_user.id,action='add')==1:
                                    await bot.edit_message_text(f'🔒 {block_name} заблокирован(a) 🔒',callback.message.chat.id,
                                                          callback.message.id,reply_markup=unblock_keyboard(block_id,
                                                                                                            block_name,None))
                    elif str(callback.data).startswith('ban_')  and str(callback.data).endswith("_banlist"):
                        # print("ban_banlist")
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
                            # print(need_ban)
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
                        print(callback)
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
                                # print('1====')
                                if unblock_id in ban_item:
                                    # print(unblock_id,'Eсть в списке')
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
                    # ключ слово логика
                    elif callback.data=="add_keyword":
                        await  add_delete_keyword_handler(callback)
                    elif callback.data in 'delete_keywords':
                        await kwrd_list_del(callback)
                         #временная раздача халявы
                    # премиум логика
                    elif callback.data == "free_premium":
                        if premium_admin_switch() is False:
                            if controling_premium(callback.message.chat.id, True) in [2, 1]:
                                await bot.send_message(callback.message.chat.id, premium_bonus, parse_mode='HTML')
                        else:
                            await bot.send_message(callback.message.chat.id,'Извините, Промоакция уже не актульна',
                                                   parse_mode='HTML')



                    #         --------------------------------------------------------------------------------
                    # airpods
                    elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepmodel'):
                        print(callback.data)
                        product_choosen=callback.data.split('_')[1]
                        await bot.edit_message_text( 'Какие сообщения по товарам получать?',
                            callback.message.chat.id, callback.message.id,parse_mode="HTML",

                            reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'model',
                                                                 product_choosen= product_choosen))














                    # выбор товара choosed-item
                    elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepyear'):
                        product_choosen=callback.data.split('_')[1]
                        await bot.edit_message_text(
                            'Какие сообщения по товарам получать?',
                            callback.message.chat.id, callback.message.id,parse_mode="HTML",
                            reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'memory',callback.data,
                                                                    product_choosen))
                    elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_stepmemory'):
                        product_choosen = callback.data.split('_')[1]
                        product_year = callback.data.split('_')[2]
                        # print(callback.data)
                        await bot.edit_message_text(
                        # f'Товар: <b>{product_name.capitalize()}</b>✅\n' \
                        # f'Год линейки: {product_year} ✅\n' \
                        # f'Теперь укажите серию, цвет, память ⤵',
                            'Какие сообщения по товарам получать?',
                        callback.message.chat.id, callback.message.id, parse_mode = "HTML",
                        reply_markup = choosing_keyboard_proccess(callback.message.chat.id, 'memory',
                                                                  product_choosen=product_choosen,year=product_year))


                    elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_add'):
                        print(callback.data)

                        product_name = callback.data.split('_')[1]
                        if product_name=='iphone':
                            product_year = callback.data.split('_')[2]
                            product_model=callback.data.split('_')[3]
                            print(product_name,product_year,product_model)

                            product_spec = callback.data.split('_')[4]
                            product_color=callback.data.split('_')[5]
                            product_memory = callback.data.split('_')[6]

                            print(product_name,',', product_year, product_model,product_spec,product_color,product_memory)
                            if product_spec == 'orig':

                                new_choosed_item = {
                                    f'{product_name}_{product_year}_{product_model}_{product_spec}_{product_color}'
                                    f'_{product_memory}': [
                                        product_name, product_model, product_color, product_memory]}
                                stroke_stat = (' ').join([
                                    product_name, product_model, product_color, product_memory])
                            else:
                                new_choosed_item = {
                                    f'{product_name}_{product_year}_{product_model}_{product_spec}_{product_color}'
                                    f'_{product_memory}': [
                                        product_name, product_model, product_spec, product_color, product_memory]}
                                stroke_stat = (' ').join([
                                    product_name, product_model, product_spec, product_color, product_memory])

                            # print(new_choosed_item)
                            if prem_status(callback.message.chat.id) == True:
                                get_add_del_choosed_item(callback.message.chat.id, "add", new_choosed_item)
                                await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                            callback.message.chat.id,
                                                            callback.message.id,
                                                            reply_markup=choosing_keyboard_proccess(
                                                                callback.message.chat.id,
                                                                level='memory',
                                                                product_choosen=product_name, year=product_year))

                            else:
                                if len(tuple(get_add_del_choosed_item(callback.message.chat.id, "get").keys())) < 1:
                                    # print('проблема',len(tuple( get_add_del_choosed_item(callback.message.chat.id,"get").keys())))
                                    get_add_del_choosed_item(callback.message.chat.id, "add", new_choosed_item)
                                    await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                                callback.message.chat.id,
                                                                callback.message.id,
                                                                reply_markup=choosing_keyboard_proccess(
                                                                    callback.message.chat.id,
                                                                    level='memory',
                                                                    product_choosen=product_name, year=product_year))

                                else:
                                    # bot.edit_message_text(premium_offer, callback.message.chat.id,
                                    #                       callback.message.id)
                                    await bot.send_message(callback.message.chat.id, premium_offer)









                        elif product_name=='airpods':
                            product_model = callback.data.split('_')[2]
                            print(callback.data)
                            product_spec=callback.data.split("_")[3]
                            print(product_spec)



                            if ' ' in product_spec:
                                product_spec=product_spec.split(" ")


                                new_choosed_item = {
                                        f'{product_name}_{product_model}_{("_").join(product_spec)}': [
                                    product_name, product_model,*product_spec]}

                            else:
                                new_choosed_item = {
                                f'{product_name}_{product_model}_{product_spec}': [
                                    product_name, product_model, product_spec]}
                            print(new_choosed_item)

                            if prem_status(callback.message.chat.id) == True:
                                get_add_del_choosed_item(callback.message.chat.id, "add", new_choosed_item)
                                await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                            callback.message.chat.id,
                                                            callback.message.id,
                                                            reply_markup=choosing_keyboard_proccess(
                                                                callback.message.chat.id,

                                                                product_choosen=product_name))

                            else:
                                if len(tuple(get_add_del_choosed_item(callback.message.chat.id, "get").keys())) < 1:
                                    # print('проблема',len(tuple( get_add_del_choosed_item(callback.message.chat.id,"get").keys())))
                                    get_add_del_choosed_item(callback.message.chat.id, "add", new_choosed_item)
                                    await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                                callback.message.chat.id,
                                                                callback.message.id,
                                                                reply_markup=choosing_keyboard_proccess(
                                                                    callback.message.chat.id,

                                                                    product_choosen=product_name))

                                else:
                                    # bot.edit_message_text(premium_offer, callback.message.chat.id,
                                    #                       callback.message.id)
                                    await bot.send_message(callback.message.chat.id, premium_offer)

                        # addinf_pos(stroke_stat)

                        # print('здесь')


                                # else:


                        # else:
                        #         bot.edit_message_text(
                        #          f'<b>Лимит на добавление ключевых слов превышен❌ </b>\n\n'+Text_of_messages.premium_offer,
                        #                 callback.message.chat.id, callback.message.id, parse_mode="HTML")
                    elif str(callback.data).startswith('construct_') and str(callback.data).endswith('_delete'):
                        print(callback.data)
                        if callback.data.split('_')[1]=='iphone':
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
                                    await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                                callback.message.chat.id,
                                                                callback.message.id,
                                                                reply_markup=choosing_keyboard_proccess(
                                                                    callback.message.chat.id,
                                                                    level='memory',
                                                                    product_choosen=product_name, year=product_year))
                        elif callback.data.split('_')[1]=='airpods':
                            product_name = callback.data.split('_')[1]

                            product_model = callback.data.split('_')[2]

                            product_spec = callback.data.split('_')[3]
                            print(product_name,product_model,product_spec)
                            if " " in product_spec:
                                product_spec=product_spec.replace(" ","_")
                            # print(product_name, product_year, product_model,product_spec,product_color,pr)
                            to_del = f'{product_name}_{product_model}_{product_spec}'

                            if to_del in tuple(get_add_del_choosed_item(callback.message.chat.id, "get").keys()):
                                if get_add_del_choosed_item(callback.message.chat.id, "del", to_del) == 'deleted':
                                    await bot.edit_message_text('Какие сообщения по товарам получать?',
                                                                callback.message.chat.id,
                                                                callback.message.id,
                                                                reply_markup=choosing_keyboard_proccess(
                                                                    callback.message.chat.id,

                                                                    product_choosen=product_name))


                    #
                    #
                    # -------------------------------------------------------------------------------------------------
                    # блок рассылки
                    elif callback.data=='reject_new_mail':
                            print(callback.data)
                            await bot.edit_message_text(f"Мои рассылки\n\nВыберите рассылку ", callback.message.chat.id,
                                                        callback.message.id,
                                                        reply_markup=mail_list_db_kb(action='list'))
                            # await bot.delete_message(callback.message.chat.id,callback.message.id)
                            await bot.delete_state(callback.from_user.id, callback.message.chat.id)
                    elif callback.data == 'change_name_mail':
                        print(callback.data)

                        await bot.edit_message_text('Наберите новое название для рассылки', callback.message.chat.id,
                                                    callback.message.id)
                        await bot.set_state(callback.from_user.id,SuperStates.getnamemail,callback.message.chat.id)
                    elif callback.data=='change_content_mail':
                        print(callback.data)

                        await bot.edit_message_text('Наберите новый текст для рассылки', callback.message.chat.id,
                                                    callback.message.id)
                        await bot.set_state(callback.from_user.id,SuperStates.getсontentmail,callback.message.chat.id)
                    elif callback.data == 'add_list_mail':
                        print(callback.data)

                        async with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
                            print(data,'clbck')
                            if mail_db(data['namemail'],data['contentmail'],action='add') =="added":

                                await bot.edit_message_text( "Рассылка добавлена",callback.message.chat.id,
                                                             callback.message.id,
                                                       reply_markup=mailmenu())
                                # await bot.delete_message(callback.message.chat.id, callback.message.id)
                                await bot.delete_state(callback.from_user.id, callback.message.chat.id)

                            else:
                                # await bot.delete_message(callback.message.chat.id,callback.message.id)
                                await bot.edit_message_text( f"Рассылка с таким именем {data['namemail']} "
                                                                                 "уже существует.\nЗамените имя и "
                                                                                 "отправьте ",
                                                             callback.message.chat.id,callback.message.id )
                                await bot.set_state(callback.from_user.id,SuperStates.getnamemail,callback.message.chat.id)
                    elif callback.data=='add_mail_item':
                        print(callback.data)
                        await bot.edit_message_text('Напишите название вашей будущей рассылки',
                                                    callback.message.chat.id, callback.message.id)
                        await bot.set_state(callback.from_user.id,SuperStates.getnamemail,callback.message.chat.id)
                        async with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
                            print('mailingnameprocess', data)
                            data['namemail'] = None
                            data['contentmail']=None
                    elif callback.data.startswith('mail_send_'):
                        print(callback.data)
                        name = callback.data.split("_")[2]
                        text=mail_db(namemail=name,action='get')
                        mail=f'{text}'
                        async def instant_sending_mail(text):
                            userslist=all_users_list(action='get')
                            allauditory=len(userslist)
                            # userslist=[6724529493,704718950]
                            auditory=0
                            for user in userslist:
                                print(user)
                                try:
                                    await bot.send_message(user,mail,parse_mode='html')
                                    auditory+=1

                                except Exception as e:
                                    print(e)
                            return auditory, allauditory
                        auditory,allauditory= await  instant_sending_mail(mail)
                        await bot.send_message(callback.message.chat.id,
                                               f"Рассылка разослана {auditory} из {allauditory}",
                                               parse_mode='html',
                                               reply_markup=mailopenmenu(name))
                    elif callback.data=='my_mail_list':
                        print(callback.data)

                        if len( mail_db(action='list'))>0:
                            await bot.edit_message_text(f"Мои рассылки\n\nВыберите рассылку ",callback.message.chat.id,callback.message.id,
                                               reply_markup=mail_list_db_kb(action='list'))
                        else:
                            await bot.edit_message_text( f"Мои рассылки\n\nУ вас нет рассылок ",
                             callback.message.chat.id,callback.message.id,
                                                   reply_markup=mail_list_db_kb(action='back'))
                    elif callback.data == 'my_mail_menu':
                        print(callback.data)

                        await bot.edit_message_text('Выберите действие',callback.message.chat.id,callback.message.id,
                                                    reply_markup=mailmenu())
                    elif callback.data.startswith('mail_open_'):
                        print(callback.data)
                        name=callback.data.split("_")[2]
                        text=mail_db(namemail=name,action='get')
                        await bot.edit_message_text( f"Рассылка <b>{name.capitalize()}</b>\n\n{text}",
                                                     callback.message.chat.id,callback.message.id,
                                               parse_mode='html',
                                               reply_markup=mailopenmenu(name))
                    elif callback.data.startswith('mail_delete_'):
                        print(callback.data)

                        name = callback.data.split("_")[2]
                        if mail_db(namemail=name,action='delete')=='delete':
                            # await bot.edit_message_text(f"Рассылка <b>{name.capitalize()}</b> удалена",
                            #                         callback.message.chat.id,callback.message.id,
                            #                        parse_mode='html',reply_markup=mail_list_db_kb('list')
                            #                        )


                            if len(mail_db(action='list')) > 0:
                                await bot.edit_message_text(f"Рассылка <b>{name.capitalize()}</b> удалена\n\nВыберите рассылку ",
                                                            callback.message.chat.id, callback.message.id,
                                                            parse_mode='html',
                                                            reply_markup=mail_list_db_kb(action='list'))
                            else:
                                await bot.edit_message_text(f"Мои рассылки\n\nУ вас нет рассылок ",
                                                            callback.message.chat.id, callback.message.id,
                                                            reply_markup=mail_list_db_kb(action='back'))
                        await bot.delete_state(callback.from_user.id, callback.message.chat.id)
                      # блок прайслист
                    elif callback.data=='upload_pricelist':
                        await bot.send_message(callback.message.chat.id,
                                               f"<b>Загрузите ваш прайслист в формате EXCEL-файла</b>\n\n"
                                               f"<b>Прайслист должен быть в следующем формате</b>❗❗❗\n\nв 1 столбце - товар, "
                                               f"во 2-ом - цена\n\n"
                                               f"Пример: https://clck.ru/37V8L5",disable_web_page_preview=True,
                                               parse_mode='html'
                                               )
                        await bot.set_state(callback.from_user.id, SuperStates.getpricelist, callback.message.chat.id)
                    elif callback.data=='get_pricelist':
                        def format_products_data(data):
                            message = "<u><b>Ваш текущий прайслист</b></u>💰\n\n"
                            for product, price in data:
                                message += f"<b>{product.capitalize()}</b> : {int(price)} ₽\n"
                            return message

                        data = get_products_data(callback.from_user.id,callback.from_user.username)
                        formatted_message = format_products_data(data)
                        await  bot.send_message(callback.message.chat.id, formatted_message,parse_mode='html')
                    elif callback.data == 'autocall_on':
                        if prem_status(callback.from_user.id)==False and callback.from_user.id not in all_permissions(\
                            'get_autosellers'):
                            await  bot.send_message(callback.message.chat.id, premium_offer_autocall, parse_mode='html')
                        elif callback.from_user.id in all_permissions('get_autosellers') or prem_status(
                            callback.from_user.id) is True:
                            autocall_status(callback.from_user.id,'change')
                            await bot.edit_message_text(autocall_text,callback.message.chat.id,callback.message.id,
                                                    parse_mode='html',
                                                    reply_markup=pricelistmenu(callback.from_user.id))
                    elif callback.data == 'autocall_off':
                        autocall_status(callback.from_user.id,'change')
                        await bot.edit_message_text(autocall_text,callback.message.chat.id,callback.message.id,parse_mode='html',
                                                    reply_markup=pricelistmenu(callback.from_user.id))
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))
        await bot.polling(non_stop=True)


async def autocall_with_interval(auto_call_bot, chat_id, text, interval):
    await asyncio.sleep(interval)
    try:
        await auto_call_bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)

    except Exception as e:
        task_list.append(autocall_with_interval(auto_call_bot, chat_id, text, interval))
        await app.send_message(chat_id=-4010327668,text=f'autocall_with_interval(auto_call_bot, chat_id, text, "\
                                                   "interval)\n\n{e}')











async def send_message_with_interval(app, chat_id, text, interval):
        await asyncio.sleep(interval)
        try:
            await app.send_message(chat_id=chat_id, text=text,disable_web_page_preview=True)

        except Exception as e:
            print(e)
            task_list.append(send_message_with_interval(app,chat_id,text,interval))
            await app.send_message(chat_id=-4010327668, text=f"send_message_with_interval(app, chat_id, text, "
                                                            f"interval)\n\n{e}")
async def serverside(app):
    # автоответ



    async  def recall_pricelist(msg):
        # print('дошло')
        tasks=checking_products_bd(msg)
        do=None
        for deal in tasks:
            if len(deal[0])==0:
                do=None
            else:
                do=True
                break
        if do is True:
        # parse_mode='Markdown'
            price_offer = (f'<b>Добрый день! Мы собрали для вас интересные предложения по вашему запросу '
                           f'с '
                           f'Горбушки</b>\n')
            customers = tasks[0][2]
            for task in tasks:
                items,seller,customer=task
                price_offer+=f'\n<b>Предложение от</b> <i><b>[{seller}](https://t.me/{seller})</b></i>:\n\n'
                for item in items:
                    price_offer+=f'<b>{item[0].capitalize() } : {int(item[1])}</b>\n'

                # print(price_offer)
                await asyncio.sleep(2)
            auto_call_process.append(autocall_with_interval(app, customers,
                                                            price_offer, 1))

        else:pass



    # проверки на ник в таблице и рассылку почистить от сообщений
    @app.on_message()
    async def forward_to_private_chat(app, message):
        if stop_function() is True:
         # print(message.from_user.last_name)

         # if message.from_user.id in [704718950 ,6724529493]:
        #     print(message)
            if int(message.chat.id) not in chat_ids:

                    user_id=message.from_user.id
                    text=str(message.text).lower()
                    resolve=json.loads(str(message.from_user))



                    if 'username' in resolve.keys():
                                if 'bot' not in resolve['username'].lower() :
                                    usrnm = message.from_user.username
                                    if any(keyword in text for keyword in ['куплю', 'предложите', 'ищу','?','купить',
                                                                                   'buy','ищу']):


                                        if user_id in last_message_len1.keys():

                                                if (last_message_len1[user_id]['len'] == len(text) and
                                                   time.time()-last_message_len1[user_id]['time']<7) :
                                                    send = False
                                                    # print(usrnm,'spamiiiiiiiiiiiiiiiiiiinnnnnnng')
                                                else:
                                                    send = True
                                                    last_message_len1[user_id]['len'] = len(text)
                                                    last_message_len1[user_id]['time'] = int(time.time())
                                        else:
                                            last_message_len1[user_id]={}
                                            last_message_len1[user_id]['len'] = len(text)
                                            last_message_len1[user_id]['time'] = int(time.time())
                                            send = True
                                        if send == True:
                                            await recall_pricelist(message)
                                            # print('-------------\n',resolve['username'])
                                            # print(message.text)
                                            random.shuffle(chat_ids)

                                            # Выбираем случайный элемент из перемешанного списка
                                            random_chat_id = int(chat_ids[0])

                                            task_list.append(send_message_with_interval(app,  random_chat_id,
                                                f'set_@_{user_id}_@_{usrnm}_@_set{message.text}', 0.1))
















# автокол свкрху прикуртить
async def checking ():
    print('ok')
    global wait_seconds
    wait_seconds=1
    first_len=0

    while True:
        from pyrogram.errors.exceptions.flood_420 import FloodWait
        first_len_task = len(task_list)

        # await asyncio.sleep(5)
        # print('таски=',task_list,len(task_list))

        if len(task_list)>5 or first_len==len(task_list) or len(task_list)-first_len<4 :
                for task in task_list.copy():
                    await asyncio.sleep(wait_seconds)
                    try:
                            await task
                            task_list.remove(task)
                            wait_seconds=2

                    except Exception as e :
                        await bot.send_message(chat_id=-4010327668, text=f'{task}\n\n{e}')
        autocall_first_len = len(auto_call_process)

        await asyncio.sleep(wait_seconds)
        # print('автоответчик=', auto_call_process, len(auto_call_process))

        if (len(auto_call_process) > 5 or autocall_first_len == len(auto_call_process) or len(auto_call_process) - first_len
            < 4):
            for autocall_task in auto_call_process.copy():
                await asyncio.sleep(1)
                try:
                    await autocall_task
                    auto_call_process.remove(autocall_task)
                    wait_seconds = 2

                except Exception:
                    pass
        # print(last_message_len1)
        keys=tuple(last_message_len1.keys())
        for user_ids in keys:
            if time.time()- last_message_len1[user_ids]['time']>5:
                # print(user_ids,'удален из недавно отправленных')
                del last_message_len1[user_ids]








async def main():
    global task_list
    global auto_call_process
    global auto_call_bot
    global chat_ids


    task_list=[]
    auto_call_process=[]
    app = Client("Gorbushkin_resender")
    chat_ids = [-1001995766142, -1002018161709, -1002091805379, -1001869659170, -1002101187519, -1002011356796,
                -1001995187845, -1002057441036, -1002049302049, -1002014932385, -1002060439501]

    bot = AsyncTeleBot(token=token_GorbushkinService,
                       state_storage=STM())
    # auto_call_bot=Client('salesbot')
    scheduler = BackgroundScheduler()
    # обнулятор статистики не трогать

    def reset_column_values():
        # Функция для обнуления значений в колонке
        conn = sqlite3.connect('bot_db.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE stats SET query_count = 0")
        conn.commit()
        conn.close()



    scheduler.add_job(reset_column_values, 'cron', hour=23, minute=59,
                      )

    scheduler.start()
    await asyncio.gather(asyncio.create_task(checking()),
                         asyncio.create_task(clientside(bot)), asyncio.create_task(serverside(await app.start()))
                         )
    await reset_column_values()





    # Запуск бота в бесконечном цикле
if __name__ == '__main__':
    asyncio.run(main())

















