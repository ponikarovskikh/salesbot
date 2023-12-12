import sqlite3
import json
import sqlite3
from datetime import datetime, timedelta

def createtable_users():
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()

    # Создание таблицы для хранения данных пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            keywords TEXT,
            premium BOOLEAN DEFAULT FALSE,
            blocklist TEXT,
            keywords_limit INTEGER DEFAULT 1,
            play INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_users_field(user_id,username,chat_id):
    conn = sqlite3.connect('bot_db.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    # print(existing_user)
    if existing_user is None:
        # Если пользователя нет в базе данных, добавляем его
        cursor.execute(
            'INSERT INTO users (user_id, username, keywords,premium, blocklist, keywords_limit,play,chat_id,'
            'purchase_date,expiration_date,choosed_items) VALUES (?,?, ?, ?, ?, ?,?,?,?,?,?)',
            (user_id, username,'[]', 0, '[]',1,1,chat_id,0,0,"{}"))
        conn.commit()

        return 'new added'

    else:
        conn.close()
        return 'already exists'

def get_blocked_users(user_id:int,action:str):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT blocklist FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    print('get_blocked_users=',result)
    if result is not None:
        print(1,'Длина',len(result[0]))
        if action =='len':
            blocklist = json.loads(result[0])
            if blocklist=={}:
                return len(result[0])
        elif action =='dict' and len(result[0])!=0 :
            blocklist = json.loads(result[0])
            return blocklist
        elif action =='dict' and len(result[0])==0:
            return  {}
    elif result==None:
        return None
    elif result == None:
        return None
# print(get_blocked_users(704718950,'dict'))

#добавить забаненого в список забаненых
def add_delete_get_clear_blocked_users(block_id:int=0,block_name:str=None, user_id:int=0,action:str='getall'):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT blocklist FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    # print(result)
    if result is not None:
        blocklist = result[0]
        blocklist = dict(json.loads(blocklist))
        # print(blocklist)
        if action =='add':
            blocklist[block_id]=block_name
            blocklist = json.dumps(blocklist)
            cursor.execute('UPDATE users SET blocklist = ? WHERE user_id = ?', (blocklist, user_id))
            conn.commit()
            #'user has been banned'
            return 1
        elif action=='delete':
            print(4)
            # Преобразование строки JSON в объект Python (в данном случае, в список)
            blocklist.pop(str(block_id))
            print(blocklist)
            blocklist = json.dumps(blocklist,ensure_ascii=False)
            cursor.execute('UPDATE users SET blocklist = ? WHERE user_id = ?', (blocklist, user_id))
            conn.commit()
            #'user has been unbanned'
            return 2
        elif action=='getall':
            # print(blocklist)

            blocklist_tuple=tuple( (int(id[0]),str(id[1])) for id in blocklist.items())
            print(blocklist_tuple)
            return blocklist_tuple
        elif action=='clear':
            blocklist={}
            blocklist = json.dumps(blocklist)
            cursor.execute('UPDATE users SET blocklist = ? WHERE user_id = ?', (blocklist, user_id))
            conn.commit()
            #3 'blocklist has been cleared'
            return 3
    else:
        return 0








# утилита для создания поля
def createfield():
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    # Выполнение операции добавления нового поля
    cursor.execute('ALTER TABLE users ADD COLUMN chat_id INTEGER;')
    conn.commit()
#словарь юзери и их ключевые слова
def get_users_and_keywords():
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, keywords FROM users")
    rows = cursor.fetchall()
    # Создание словаря
    user_keywords_dict = {user_id: keywords for user_id, keywords in rows}
    conn.commit()
    print(user_keywords_dict)

# get_users_and_keywords()
# добавить слово для пользователя в формате списка для каждого пользователя соответственоо

def add_delete_keyword(user_id:int,keyword=None,action:str=None):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keywords,keywords_limit,premium FROM users WHERE user_id = ?', (user_id,))
    result=cursor.fetchone()
    print(result)
    if action=='add':
        if len(result)>0:
            keywords = json.loads(result[0])
            keywords_limit=int(result[1])
            premium=bool(result[2])
            print(keywords,keywords_limit,premium)
            if premium is True :
                print(1)
                keywords.append(keyword)
                keywords=json.dumps(keywords)
                cursor.execute('UPDATE users SET keywords = ? WHERE user_id = ?', (keywords, user_id))
                conn.commit()
                return 'added'
            else:
                if len(keywords) == 0 :
                    keywords.append(keyword)
                    keywords = json.dumps(keywords)
                    cursor.execute('UPDATE users SET keywords = ? WHERE user_id = ?', (keywords, user_id))
                    conn.commit()
                    return 'added'
                elif len(keywords) == keywords_limit :
                    return 'limit_increase'
    # elif action=='del':
    #     keywords = list(json.loads(result[0]))
    #     if keyword in keywords:
    #             keywords.remove(keyword)
    #     else:
    #         return 'word not there exists '
    #     keywords = json.dumps(keywords)
    #     cursor.execute('UPDATE users SET keywords = ? WHERE user_id = ?', (keywords, user_id))
    #     conn.commit()
    #     return 'word was deleted'
    elif action == 'clear_list':
        print('clear')
        keywords=[]
        keywords = json.dumps(keywords)
        cursor.execute('UPDATE users SET keywords = ? WHERE user_id = ?', (keywords, user_id))
        conn.commit()
        print('keywords_cleear')
        return 'keywords_clear'
    elif action =='1remain':
        if len(result)>0:
            keywords = json.loads(result[0])
            keywords_limit=0
            premium=bool(result[2])
            print(keywords,keywords_limit,premium)
            if len(keywords)>1:
                first_key=keywords[0]
                keywords.clear()
                keywords.append(first_key)
                keywords = json.dumps(keywords)
                cursor.execute('UPDATE users SET keywords = ? WHERE user_id = ?', (keywords, user_id))
                conn.commit()
                return '1remain'
            else:
                return '1remain'


# print( add_delete_keyword(704718950,None,action='1remain'))



# скрипт внесения инфы какие товары выбрал пользоват ченрез клаву и что сейчас ищет также можно удалить

def get_add_del_choosed_item(user_id=None,action=None,item=None):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT choosed_items FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    # print(result)
    if action=='get':
        if len(result) > 0:
            choosed_items = json.loads(result[0])
            return choosed_items
            # print(choosed_items,type(choosed_items))
    elif action=='add':
        if len(result) > 0:
            choosed_items = json.loads(result[0])
            # print(choosed_items,type(choosed_items))

            control_items=tuple (item.items())[0]
            # print(control_items)
            choosed_items[control_items[0]]=control_items[1]
            # print(choosed_items.keys())
            choosed_items = json.dumps(choosed_items)
            # print(choosed_items)
            cursor.execute('UPDATE users SET choosed_items = ? WHERE user_id = ?', (choosed_items, user_id))
            conn.commit()
            return 'added'
    elif action=='del':
        if len(result) > 0:
            choosed_items = json.loads(result[0])
            # print(choosed_items,type(choosed_items))
            # control_items=tuple (item.items())[0]
            # print(control_items)
            choosed_items.pop(item)
            choosed_items = json.dumps(choosed_items)
            # print(choosed_items)
            cursor.execute('UPDATE users SET choosed_items = ? WHERE user_id = ?', (choosed_items, user_id))
            conn.commit()
            return 'deleted'
    elif action == '1remain':
        if len(result) > 0:
            choosed_items = json.loads(result[0])
            if len(choosed_items)==0:
                return 'cleared'

            else:

                print(len(choosed_items))

                first_item=tuple(choosed_items.items())[0]
                print(first_item)

                choosed_items.clear()
                choosed_items[first_item[0]]=first_item[1]
                choosed_items = json.dumps(choosed_items)
                # print(choosed_items)
                cursor.execute('UPDATE users SET choosed_items = ? WHERE user_id = ?', (choosed_items, user_id))
                conn.commit()
                return 'cleared'



# print(get_add_del_choosed_item(704718950,'1left',{"iphone_12_pro":["iphone","14","pro"]}))













# функция для просмотра юзером сколько осталось времени действия подписки подписки
def premium_alive_period(user_id:int,action:str):
    # Подключение к базе данных SQLite
        conn = sqlite3.connect('bot_db.db')
        cursor = conn.cursor()
        current_datetime = datetime.now()
        if action=='set_time':
        # Установка даты покупки
            cursor.execute("UPDATE users SET purchase_date = ? WHERE user_id = ?", (current_datetime.date(), user_id))
        # Вычисление и установка даты окончания срока действия премиума (30 суток)
            expiration_date = current_datetime + timedelta(days=30)
            cursor.execute("UPDATE users SET expiration_date = ? WHERE user_id = ?", (expiration_date.date(), user_id))
            conn.commit()
            return 'премиум активен 30 дней'
        elif action=='remain_time':
            cursor.execute("SELECT expiration_date FROM users WHERE user_id = ?", (user_id,))
            expiration_date = cursor.fetchone()[0]
            if expiration_date !=0:
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
                remaining_days = (expiration_date - current_datetime).days

                return remaining_days
            else:
                return 0
        elif action=='null_time':
            cursor.execute("UPDATE users SET purchase_date = ? WHERE user_id = ?", (0, user_id))

            conn.commit()
    # Вычисление и установка даты окончания срока действия премиума (30 суток)
            cursor.execute("UPDATE users SET expiration_date = ? WHERE user_id = ?", (0, user_id))
            conn.commit()
            return 'time has been nulled'

def controling_premium(user_id:int,new_premium_status:bool):
    # 1-limit
    # 0-endless

    # status premium
    # 1-'you already have premium'
    # 2-"you've got premium"
    # 3-"premium has been deactivacted"
    # 4-"premium was already being False "

    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keywords_limit,premium FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    # print(result)
    keywords_limit=int(result[0])
    premium = bool(result[1])
    if new_premium_status is True  :
        if premium is True :
            # print(premium)
            if keywords_limit !=0:
                keywords_limit=0
            cursor.execute('UPDATE users SET keywords_limit = ?,premium=? WHERE user_id = ?',
                           (keywords_limit, premium, user_id))
            conn.commit()
            return 1
        else:
            premium=True
            keywords_limit=0
            cursor.execute('UPDATE users SET keywords_limit = ?,premium=? WHERE user_id = ?',
                           (keywords_limit, premium, user_id))
            conn.commit()
            premium_alive_period(user_id,'set_time')
            return 2
    else:
        if premium is True:
            premium = False
            keywords_limit = 1

            cursor.execute('UPDATE users SET keywords_limit = ?,premium=? WHERE user_id = ?',
                           (keywords_limit, premium, user_id))
            conn.commit()
            if  premium_alive_period(user_id, 'null_time') =='time has been nulled':
                print('yes')
                if get_add_del_choosed_item(user_id,action='1remain') =='cleared':
                    print('yes')
                    if  add_delete_keyword(user_id,0,'1remain')=='1remain':
                        print('yes')
                        return 3

# print( controling_premium(user_id=704718950,new_premium_status=False    ))




def prem_status(user_id):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT premium FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result[0]==1:
        return True
    else:
        return False


def out_premium_check(user_id,action=None):
    # premium=prem_status(user_id)
    period = premium_alive_period(user_id,'remain_time')
    print(type(period))

    if period !=0 and period>0:
        if action is not None:
            return period
        else:
            return 'skip_prem'
    elif period <= 0 :
        print(period)
        if prem_status(user_id)==True:
           if controling_premium(user_id, False) == 3:
               print('зашел')
               return 'premium_out'
        else:
            return 'skip_notprem'






# print(out_premium_check(704718950))











def getchangeplaystatus(user_id=None,action=None):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT play FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if action=='get' or action is None :
        return result[0]
    elif action == 1 and result[0]==0:
        cursor.execute('UPDATE users SET play = ?WHERE user_id = ?',
                       (1, user_id))
        conn.commit()
        return 1
    elif action == 0 and  result[0]==1 :
        cursor.execute('UPDATE users SET play = ?WHERE user_id = ?',
                       (0 ,user_id))
        conn.commit()
        return 0

# print(getchangeplaystatus(704718950,1))









def get_user_and_keywords(user_id,checking=None):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keywords FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if len(result) >0:
        if checking is None :
            result=json.loads(result[0])
            return result
        else:
            keywords=json.loads(result[0])
            # print(keywords)
            choosed_items=list(get_add_del_choosed_item(user_id,'get').values())
            # print(choosed_items)
            keywords=keywords+choosed_items
            print(keywords)
            tuple_userid_kwrd=(user_id,keywords)
            print(tuple_userid_kwrd)
            return tuple_userid_kwrd
    else:
        if checking is None :
            result=json.loads(result[0])
            return result
        else:
            return tuple()




# print(get_user_and_keywords(704718950,True))





# 1111 1111 1111 1026 12 22 000
# print(prem_status(704718950))

# print(getfreepremium())
def get_users_without_sendusermsg_in_blocklist(block_id:int):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()

    query = "SELECT user_id FROM users WHERE NOT blocklist LIKE ?"
    cursor.execute(query, ('%' + str(block_id) + '%',))
    result = cursor.fetchall()
    # print(result)


    return tuple(user_id[0] for user_id in result)

    # Пример использования функции


# print(get_users_without_sendusermsg_in_blocklist('1'))
#


russiandict={
   "про": "pro",
    "макс":"max",
    'мини':'mini',
    "плюс":"plus",
    "айфон":"iphone",
    "натурал":"natural",
    "вайт":"white",
    "блэк":"black",
    "грин":"green"

}