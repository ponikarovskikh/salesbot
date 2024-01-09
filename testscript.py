# import types
#
# from telebot import asyncio_filters
# from telebot.asyncio_storage import StateMemoryStorage as STM
# from telebot.async_telebot import AsyncTeleBot
# from telebot.asyncio_handler_backends import StatesGroup as STSGR,State as ste
# from Text_of_messages import *
# from config import *
# from keyboards import *
# from sqlfile import *
# import asyncio
# from pyrogram import Client
# global app
# import pandas as pd
# global bot
# bot=TeleBot(token='6841670926:AAG-1wrHdVfP7FP3NjhV96bUVwKXB3AZzno')
#
# # @bot.message_handler(func=lambda message: True,content_types=['document'])
# # def handle_docs_photo(message):
# #         chat_id = message.chat.id
# #         file_info = bot.get_file(message.document.file_id)
# #         downloaded_file = bot.download_file(file_info.file_path)
# #         # print(Document)
# #         # Сохранение файла локально
# #         with open('temp.xlsx', 'wb') as new_file:
# #             new_file.write(downloaded_file)
# #
# #         # Обработка файла Excel
# #         df = pd.read_excel('temp.xlsx')
# #
# #         # Вывод каждой строки файла
# #         for index, row in df.iterrows():
# #             print(f"Строка {index}: {row.tolist()}")
# #
# #         # Удаление временного файла
# #         os.remove('temp.xlsx')
# #
# #         bot.send_message(chat_id, "Данные файла Excel обработаны.")
# #
# #
# # bot.polling(non_stop=True)
#
#
# # bot = telebot.TeleBot('YOUR_BOT_TOKEN')
#
#
#
#
#
# @bot.message_handler(content_types=['document'])
# def handle_document(message):
#     chat_id = message.chat.id
#     user_id = message.from_user.id
#     file_info =await bot.get_file(msg.document.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#
#     file_name = 'temp.xlsx'
#     with open(file_name, 'wb') as new_file:
#         new_file.write(downloaded_file)
#
#
#     try:
#         df = pd.read_excel(file_name, usecols='A:B')
#         print(df,'df')
#         data = [(row) for index, row in df.iterrows()]
#         print(data,'писок')
#         create_table_and_insert_data(user_id, data)
#         bot.send_message(chat_id, "Данные из файла Excel сохранены в базу данных.")
#     except Exception as e:
#         print(e)
#         # bot.send_message(chat_id, f"Ошибка при обработке файла: {e}")
#
#     if os.path.exists(file_name):
#         os.remove(file_name)
#
#
#
#
# def format_products_data(data):
#     message = " Актуальный Список продуктов и цен:\n"
#     for product, price in data:
#         message += f"{product}: {int(price)}\n"
#     return message
#
# @bot.message_handler(commands=['getdata'])
# def send_products_data(message:Message):
#     data = get_products_data(message.from_user.id)
#     formatted_message = format_products_data(data)
#     bot.send_message(message.chat.id, formatted_message)
#
# bot.polling()
#
# bot.polling()
#


list1 = ["текст1", "текст2", "текст3"]
list2 = ["другой текст1", "текст2 встречается здесь", "еще один текст"]

# Создаем новый список, содержащий элементы из list1, которые есть в элементах list2
new_list = [element for element in list2 if any(sub in element for sub in list1)]


print(new_list)