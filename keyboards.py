from telebot import *
from telebot.types import *
from telebot.util import quick_markup
from sqlfile import *


def example_kb():



            inline_keyboard = telebot.types.InlineKeyboardMarkup()
            url_button = telebot.types.InlineKeyboardButton(text="Visit ", url="https://t.me/704718950")
            inline_keyboard.add(url_button)

            return inline_keyboard

# 🧩🧩📧📨✉📩📬





def menu_keyboard_1stage():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,one_time_keyboard=True)
    play_button = types.KeyboardButton('Продавать товар')


    keyboard.add(play_button)

    return keyboard


def menu_keyboard_2stage(user_id):
    # print(user_id)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    func1=types.KeyboardButton('Выбрать товары🕹️')
    func2=types.KeyboardButton('Premium-тариф🔮')
    func3=types.KeyboardButton('Блок-лист❌')
    func4=types.KeyboardButton('Ключевые слова🔑')
    func5 = types.KeyboardButton("Руководство📚")
    func6 = types.KeyboardButton("Статистика запросов📈")
    keyboard.row(func1, func2)
    keyboard.row(func3, func4)
    keyboard.row(func5, func6)
    if getchangeplaystatus(user_id) == 1:
        func8=types.KeyboardButton('Продажи на паузу ⏸️')
        keyboard.add(func8)
    else:
        func8= types.KeyboardButton('Возобновить продажи▶️')
        keyboard.add(func8)
    if user_id in all_permissions('get_autosellers'):
        print('yes')
        func7 = types.KeyboardButton('Автопродажи🤖')
        keyboard.add(func7)


    if user_id in all_permissions('get_admins'):
        # print('yes')
        func9 = types.KeyboardButton('Админ-панель🛠')
        keyboard.add(func9)
    return keyboard


def admin_panel(user_id=None):
    print(user_id)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    func1 = types.KeyboardButton('Изменить цену Premium')
    func2 = types.KeyboardButton('Сводка')
    func3 = types.KeyboardButton('Рассылка')
    func4=types.KeyboardButton('Добавить админа')
    func5=types.KeyboardButton('Добавить продавца')
    keyboard.row(func1, func2, func3)
    keyboard.row(func4, func5)
    if premium_admin_switch() is True:

        func6 = types.KeyboardButton('Перейти на Бесплатный Premium')
    else:
        func6 = types.KeyboardButton('Включить Платный Premium')
    keyboard.row(func6)
    if user_id==704718950:
        func7=KeyboardButton('Выгрузить общий прайслист')
        keyboard.row(func7)
    keyboard.row( KeyboardButton('Назад'))
    return keyboard




# 🔮🔎🔍📣📢🛡️🔑🗝️▶️⏸️ℹ️⬅️✅🚫❌🎮🕹️↩️

def getfreepremium():
    return quick_markup(
        {

            'Получить✅': {'callback_data': f'free_premium'}

        }, row_width=1
    )

def mailopenmenu(name):
        return quick_markup(
            {

                'Разослать📣': {'callback_data': f'mail_send_{name}'},
                'Удалить❌': {'callback_data': f'mail_delete_{name}'},
                'Назад↩️': {'callback_data': f'my_mail_list'},

            }, row_width=1
        )


def mail_list_db_kb(action=None):
    if action=='list':
        markup = types.InlineKeyboardMarkup(row_width=1)
        maillist=mail_db(action='list')
        buttons = []

        for items in maillist:
            button_text = f'{items}'
            callback_data = f'mail_open_{items}'
            button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
            buttons.append(button)
        markup.add(*buttons,row_width=2)
        button_text = f'Назад↩️'
        callback_data = f'my_mail_menu'
        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        markup.add(button)


        return markup
    elif action=='back':
        return quick_markup(
            {
                'Назад↩️': {'callback_data': f'my_mail_menu'},

            }, row_width=2
        )




#расслыка
def mailmenu(action=None):
        return quick_markup(
        {

        'Добавить рассылку📍': {'callback_data': f'add_mail_item'},
        'Мои рассылки🗃':{'callback_data': f'my_mail_list'}

        }, row_width=1
    )


def addmail_reject(action=None):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton(text='✅Добавить', callback_data='add_list_mail')
    button2 = types.InlineKeyboardButton(text='↩️Заменить имя', callback_data='change_name_mail')
    button3 = types.InlineKeyboardButton(text= '↩️Заменить текст', callback_data='change_content_mail')
    button4 = types.InlineKeyboardButton(text='❌Отменить', callback_data='reject_new_mail')
    markup.row(button2,button3)
    markup.row(button4)
    markup.row(button1)
    return markup




#keyboard_block
def adddelete_keywords(action=None):
    if action=='addonly':
        return quick_markup(
            {

                '➕ Добавить ': {'callback_data': f'add_keyword'}

            }, row_width=2,
        )
    else:
        return quick_markup(
        {

        '➕ Добавить ключевые слова': {'callback_data': f'add_keyword'},
            '🗑 Убрать ключевые слова':{'callback_data': f'delete_keywords'}

        }, row_width=1
    )































#ban/unban
def block_keyboard(block_id,block_name,banlist=None):
    if banlist==True:
        return quick_markup({

            'Забанить❌': {'callback_data': f'ban_{block_id}_{block_name}_banlist'},
            'Назад↩️':{'callback_data': f'banlist_show'}}, row_width=1)
    else:
        return quick_markup({

                'Забанить❌': {'callback_data': f'ban_{block_id}_{block_name}'}}, row_width=1)

def unblock_keyboard(block_id,block_name,banlist=None):
    if banlist == True:
        return quick_markup({

            'Разблокировать🔑': {'callback_data': f'unban_{block_id}_{block_name}_banlist'},
            'Назад↩️':{'callback_data': f'banlist_show'}}, row_width=1)

    else:
        return quick_markup({

            'Разблокировать🔑': {'callback_data': f'unban_{block_id}_{block_name}'}}, row_width=1)


def banlistmarkup(user_id,blocklist):
    markup = types.InlineKeyboardMarkup(row_width=2)
    blocklist=get_blocked_users(user_id,'dict')
    buttons=[]
    for items in blocklist.items():

        button_text = f'{items[1]}'
        callback_data = f'unban_{items[0]}_{items[1]}_banlist'

        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        buttons.append(button)
    markup.add(*buttons)

    return markup

# reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'year',callback.data,{f'{product_name}':f'✅'}))
# choosing_keyboard_proccess(callback.message.chat.id, 'model', callback.data, {f'{product_name}': f'✅',f"{product_year}":"✅"}))
def choosing_keyboard_proccess(user_id=None ,level=None,construct:str=None,product_choosen=None,year=None,
                               model_choosed=None):
    with open('IPHONE_LIST.json','r') as f :
        productlist=json.load(f)
    # print(productlist)
    # print('product choosen ',product_choosen)
    markup = types.InlineKeyboardMarkup(row_width=4)
    buttons=[]
    # print(productlist.keys(),'товары')

    choosed_items = get_add_del_choosed_item(user_id, 'get')
    choosed_items = tuple(choosed_items.keys())
    # print('chosed', choosed_items)

    for product in productlist.keys():
        if product in product_choosen:
        # if product in kybmark.keys():
            button_text = f'🔽{kybmark[product]}{product}'
        else:
            button_text = f'{kybmark[product]}{product}'
        if product =="iphone":
            callback_data = f'construct_{product.lower()}_stepyear'
        elif product=='airpods':
            callback_data = f'construct_{product.lower()}_stepmodel'
        buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    markup.add(*buttons)
    # return markup
    if level=='year'and product_choosen=='iphone':
        new_clbck = construct[:-9]
        product_choice = new_clbck.split('_')[1]
        years = productlist[product_choice]


        markup = types.InlineKeyboardMarkup(row_width=6)
        buttonsmenuprod=[]
        for product in productlist.keys():
            if product in kybmark.keys():
                if product==product_choice:
                    button_text = f'🔽{kybmark[product]}{product}'

                else:
                    button_text = f'{kybmark[product]}{product}'
            callback_data = f'construct_{product.lower()}_stepyear'
            buttonsmenuprod.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttonsmenuprod)
        buttons = []
        for year in years.keys():
            button_text = f'{year}'
            callback_data = f'construct_{product_choice}_{year.lower()}_stepmemory'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttons)
    # return markup


    if level=='memory' and product_choosen=='iphone':
        # print('зашло')

        # print('memo')
        markup = types.InlineKeyboardMarkup(row_width=3)
        # print(construct,'construct')
        # print(year)
        if year is not None :

            product_choice=product_choosen

            year_choice=year
            years = productlist[product_choice]
            models = productlist[product_choice][year_choice]
            # print(year_choice)
            # print(product_choice)
        else:
            product_choice='iphone'
            year_choice='2023'
            years = productlist[product_choice]
            models = productlist[product_choice][year_choice]

        buttonsmenuprod = []
        for product in productlist.keys():
                if product in kybmark.keys():
                    if product == product_choice:
                        button_text = f'🔽{kybmark[product]}{product}'

                    else:
                        button_text = f'{kybmark[product]}{product}'
                callback_data = f'construct_{product.lower()}_stepyear'
                buttonsmenuprod.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttonsmenuprod,row_width=len(buttonsmenuprod))

        buttonsmenuyear = []
        for year in years.keys():
                if year==year_choice:
                    button_text = f'🔽{year}'

                else:
                    button_text = f'{year}'
                callback_data = f'construct_{product_choice}_{year.lower()}_stepmemory'
                buttonsmenuyear.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttonsmenuyear,row_width=len(buttonsmenuyear))
        # print(*buttonsmenuyear)
        buttonsmenumodel=[]

        for model in models.keys():
                specs=models[model]

                for spec in specs.keys():
                    colors=specs[spec]
                    # print(colors)
                    for color in colors.keys():
                        memories=colors[color]
                        # print(memories)
                        kb_mem=[]
                        memory_spec_len=len(memories)
                        for memory in memories :

                            callback_data = (f'construct_{product_choice}_{year_choice}_{model}_{spec}_{color}_'
                                             f'{memory}_add')


                            if model in kybmark.keys():
                                button_text = f'{kybmark[model]}{kybmark[spec]}{kybmark[color]}{memory}'
                                if memory in kybmark.keys():
                                    button_text = f'{kybmark[model]}{kybmark[spec]}{kybmark[color]}{kybmark[memory]}'
                            else:
                                button_text = f'{model}{kybmark[spec]}{kybmark[color]}{memory}'
                                if memory in kybmark.keys():
                                    button_text = f'{model}{kybmark[spec]}{kybmark[color]}{kybmark[memory]}'

                            for choosed in choosed_items:
                                if choosed in callback_data:
                                    # print(choosed,'---',callback_data)
                                    callback_data = (f'construct_{product_choice}_{year_choice}_{model}_{spec}_{color}_'
                                                         f'{memory}_delete')
                                    if model in kybmark.keys():
                                        button_text = f'✅{kybmark[model]}{kybmark[spec]}{kybmark[color]}{memory}'
                                        if memory in kybmark.keys():
                                            button_text = f'✅{kybmark[model]}{kybmark[spec]}{kybmark[color]}{kybmark[memory]}'
                                    else:
                                        button_text = f'✅{model}{kybmark[spec]}{kybmark[color]}{memory}'
                                        if memory in kybmark.keys():
                                            button_text = f'✅{model}{kybmark[spec]}{kybmark[color]}{kybmark[memory]}'





                            # kbid=f'iph{id}'
                            # print('button_text',button_text)

                            # print('callback_data', callback_data)
                            kb_mem.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
                        markup.add(*kb_mem,row_width=memory_spec_len)
                            # print(buttons)
    if  product_choosen=='airpods':
        # print('ашкыыы')
        buttons = []
        models=productlist['airpods']
        # print(models)
        # print(models.keys(), 'товары airpods')
        # print(choosed_items)
        for model in models.keys():
            # print(models[model],'xt')
            for spec in models[model]:
                specbutton=spec

                # if 'orig' in specbutton:
                #     specbutton=specbutton.replace('orig','')

                if model in kybmark.keys() and specbutton in kybmark.keys():

                    button_text = f'{kybmark[model]} {kybmark[specbutton]}'
                else:
                    if 'orig' in specbutton:
                        specbutton1 = specbutton.replace('orig', '')
                        button_text = f'{model} {specbutton1}'
                    else:
                        button_text = f'{model} {specbutton}'
                # if " " in spec:
                #     print(spec)
                #     spec = str(spec).replace(' ', '_')
                #     print(spec)
                callback_data=f'construct_{product_choosen}_{model}_{spec}_add'



                # print(button_text,callback_data)
                #
                # print(spec1, 'spec')
                for choosed in choosed_items:
                    callback_data1=callback_data.replace(" ","_")
                    # print(choosed,'chosed',callback_data1,'calback')


                    # print(f'{product_choosen}_{model}_{spec}','wtf')
                    if choosed in callback_data1 :
                        # print('yes')
                        if model in kybmark.keys() and specbutton in kybmark.keys():

                            button_text = f'✅{kybmark[model]} {kybmark[specbutton]}'
                        else:
                            # button_text = f'✅{model} {specbutton}'
                            if 'orig' in specbutton:
                                specbutton1 = specbutton.replace('orig', '')
                                button_text = f'✅{model} {specbutton1}'
                            else:
                                button_text = f'✅{model} {specbutton}'
                        callback_data = f'construct_{product_choosen}_{model}_{spec}_delete'

                buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))


        markup.add(*buttons,row_width=2)




































    return markup


# choosing_keyboard_proccess()









































































def pricelistmenu(user_id,action=None):
        markup = types.InlineKeyboardMarkup(row_width=1)
        tables= checking_products_bd(user_id,action='get')
        print(tables)
        usertable = any(str(user_id) in element for element in tables)
        # print(usertable)
        if usertable is True:
            b1=InlineKeyboardButton(text='🔽Загрузить новый',callback_data='upload_pricelist')
            b2=InlineKeyboardButton(text='🕒Текущий',callback_data='get_pricelist')
            markup.add(b1,b2,row_width=2)
            if autocall_status(user_id,'get')==True:
                # ☑️✅☑️✔️➿🕹🔑🕹
                b3 = InlineKeyboardButton('✅Автоответчик', callback_data='autocall_off')
            else:
                b3 = InlineKeyboardButton('❌Автоответчик', callback_data='autocall_on')
            markup.add(b3)
        elif usertable is False:
            b1=InlineKeyboardButton(text='🔽Загрузить',callback_data='upload_pricelist')
            markup.add(b1)
        return markup















kybmark = {
    "plus": "+",
    "natural": "⚙",
    "pro max": "PM",
    "pro": "P",
    "yellow": "🍋",
    "green": "☘️",
    "rose": "🌷",
    "black": "⬛️",
    "white": "⬜️",
    "silver":"💿",
    "coral": "🍊",
    "red": "🟥",
    "blue": "🔷",
    "gold": "👑",
    "purple": "💜",
    "orig":'',
    'se':'SE',
    "mini":"Mini",
    "xr":"XR",
    "ipad":"🌅",
    "airpods":"🎧",
    "watch":"⌚️",
    "iphone":"📱",
    "macbook":"💻",
    "1t":"1T",
    "pink":"🎀",
    "max":"MAX"

}


