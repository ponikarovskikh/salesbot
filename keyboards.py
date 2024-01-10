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
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    func2=types.KeyboardButton('Выбрать товары🕹️')
    func3=types.KeyboardButton('Premium-тариф🔮')
    func4=types.KeyboardButton('Блок-лист❌')
    func5=types.KeyboardButton('Ключевые слова🔍')
    if getchangeplaystatus(user_id) == 1:
        func6=types.KeyboardButton('Продажи на паузу ⏸️')
    else:
        func6= types.KeyboardButton('Возобновить продажи▶️')
    func7= types.KeyboardButton("Руководство📚")
    keyboard.row(func2,func3)
    keyboard.row(func4,func5)
    keyboard.row(func6,func7)
    func10=types.KeyboardButton("Статистика запросов📈")
    func12 = types.KeyboardButton('Автопродажи')
    keyboard.row(func12)
    keyboard.row(func10)
    if user_id in all_admins():
        func8 = types.KeyboardButton('Изменить цену Premium')
        func9 = types.KeyboardButton('Сводка')
        func11 = types.KeyboardButton('Рассылка')
        keyboard.row(func8,func11,func9)



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

                '➕ Добавить ключевые слова': {'callback_data': f'add_keyword'}

            }, row_width=1
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
def choosing_keyboard_proccess(user_id=None ,level=None,construct:str=None,product_choosen:dict()=None):
    with open('IPHONE_LIST.json','r') as f :
        productlist=json.load(f)
        # print(productlist)
    markup = types.InlineKeyboardMarkup(row_width=3)

    if level=='product':
            buttons=[]
            for product in productlist.keys():
                if product in kybmark.keys():
                    button_text = f'{kybmark[product]}{product}'
                callback_data = f'construct_{product.lower()}_stepyear'
                buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
            markup.add(*buttons)
            return markup
    elif level=='year':
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
        return markup

    elif level=='memory':
        choosed_items=get_add_del_choosed_item(user_id,'get')
        choosed_items=tuple(choosed_items.keys())
        # print('chosed',choosed_items)
        # print('memo')
        markup = types.InlineKeyboardMarkup(row_width=3)
        # print(construct)
        if construct is not None:
            new_clbck = construct[:-11]
            product_choice=new_clbck.split('_')[1]

            year_choice=new_clbck.split('_')[2]
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
                        pos_len=len(memories)
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
                            buttonsmenumodel.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttonsmenumodel,row_width=pos_len)
                            # print(buttons)
        return markup

def pricelistmenu(user_id,action=None):
        markup = types.InlineKeyboardMarkup(row_width=1)
        tables= checking_products_bd(user_id,'get')
        print(tables)
        usertable = any(str(user_id) in element for element in tables)
        print(usertable)
        if usertable is True:
            b1=InlineKeyboardButton(text='🔽Загрузить новый',callback_data='upload_pricelist')
            b2=InlineKeyboardButton(text='🕒Текущий',callback_data='get_pricelist')
            markup.add(b1,b2,row_width=2)
            if autocall_status(user_id,'get')==True:
                # ☑️✅✔️➿.
                b3 = InlineKeyboardButton('✅Автоответчик', callback_data='autocall_off')
            else:
                b3 = InlineKeyboardButton('Автоответчик', callback_data='autocall_on')
            markup.add(b3)
        elif usertable is False:
            b1=InlineKeyboardButton(text='🔽Загрузить',callback_data='upload_pricelist')
            markup.add(b1)
        return markup















kybmark = {
    "plus": "+",
    "natural": "🔗",
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
    "1t":"1T"

}


