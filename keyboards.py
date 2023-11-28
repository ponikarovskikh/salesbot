from telebot import *
from telebot.types import *
from telebot.util import quick_markup
from sql import *

def menu_keyboard_1stage():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,one_time_keyboard=True)
    play_button = types.KeyboardButton('Продавать товар')

    keyboard.add(play_button)

    return keyboard


def menu_keyboard_2stage(user_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    func1 = types.KeyboardButton('Главное меню')
    func2=types.KeyboardButton('Выбрать товары')
    func3=types.KeyboardButton('Premium-тариф')
    func4=types.KeyboardButton('Блок-лист')
    func5=types.KeyboardButton('Ключевые слова')
    if getchangeplaystatus(user_id) in [1,'1']:
        func6=types.KeyboardButton('Продажи на паузу ')
    else:
        func6= types.KeyboardButton('Возобновить продажи')
    func7= types.KeyboardButton("FAQ")
    keyboard.add(func1)
    keyboard.row(func2,func3)
    keyboard.row(func4,func5)
    keyboard.row(func6,func7)
    return keyboard





def getfreepremium():
    return quick_markup(
        {

            'Получить✅': {'callback_data': f'free_premium'}

        }, row_width=1
    )












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

            'Забанить': {'callback_data': f'ban_{block_id}_{block_name}_banlist'},
            'Назад':{'callback_data': f'banlist_show'}}, row_width=1)
    else:
        return quick_markup({

                'Забанить': {'callback_data': f'ban_{block_id}_{block_name}'}}, row_width=1)

def unblock_keyboard(block_id,block_name,banlist=None):
    if banlist == True:
        return quick_markup({

            'Разблокировать человека🔑': {'callback_data': f'unban_{block_id}_{block_name}_banlist'},
            'Назад':{'callback_data': f'banlist_show'}}, row_width=1)

    else:
        return quick_markup({

            'Разблокировать человека🔑': {'callback_data': f'unban_{block_id}_{block_name}'}}, row_width=1)


def banlistmarkup(user_id,blocklist):
    markup = types.InlineKeyboardMarkup(row_width=2)
    blocklist=get_blocked_users(user_id,'dict')

    for items in blocklist.items():

        button_text = f'{items[1]}'
        callback_data = f'unban_{items[0]}_{items[1]}_banlist'

        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        markup.add(button)

    return markup

# reply_markup=choosing_keyboard_proccess(callback.message.chat.id,'year',callback.data,{f'{product_name}':f'✅'}))
# choosing_keyboard_proccess(callback.message.chat.id, 'model', callback.data, {f'{product_name}': f'✅',f"{product_year}":"✅"}))
def choosing_keyboard_proccess(user_id=None ,level=None,construct:str=None,product_choosen:dict()=None):
    with open('IPHONE_LIST.json','r')as f :
        productlist=json.load(f)
        print(productlist)
    markup = types.InlineKeyboardMarkup(row_width=6)
    if level=='product':
        buttons=[]
        for product in productlist.keys():
            print(product)
            button_text = f'{product}'
            callback_data = f'construct_{product.lower()}_stepyear'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttons)
        return markup
    elif level=='year':

        markup = types.InlineKeyboardMarkup(row_width=6)

        new_clbck=construct[:-9]
        product_choice=new_clbck.split('_')[1]
        years=productlist[product_choice]
        buttons = []
        for year in years.keys():
            button_text = f'{year}'
            callback_data = f'construct_{product_choice}_{year.lower()}_stepmemory'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttons)
        return markup
    elif level=='memory':
        print('memo')
        markup = types.InlineKeyboardMarkup(row_width=3)

        new_clbck = construct[:-11]
        product_choice=new_clbck.split('_')[1]
        year_choice=new_clbck.split('_')[2]
        models = productlist[product_choice][year_choice]
        buttons=[]

        for model in models.keys():
            specs=models[model]
            print(specs)
            for spec in specs.keys():
                colors=specs[spec]
                print(colors)
                for color in colors.keys():
                    memories=colors[color]
                    print(memories)

                    for memory in memories:
                        if model in kybmark.keys():
                            button_text = f'{kybmark[model]}{kybmark[spec]}{kybmark[color]}{memory}'
                        else:
                            button_text = f'{model}{kybmark[spec]}{kybmark[color]}{memory}'

                        print('button_text',button_text)
                        callback_data = (f'construct_{product_choice}_{year_choice}_{model}_{spec}_{color}_'
                                         f'{memory}_choosen')
                        print('callback_data', callback_data)
                        buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.add(*buttons)
                        # print(buttons)
        return markup




kybmark = {
    "plus": "+",
    "natural": "🔗",
    "pro max": "M",
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
    "xr":"XR"

}


