from telebot import TeleBot
from telebot import types
from telebot.types import *
import config
bot=TeleBot(token=config.super_test)


@bot.message_handler(commands=['start'])
def start_message(message):
    # Создание клавиатуры
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_hello = types.KeyboardButton("Привет")
    keyboard.add(button_hello)

    # Отправка приветственного сообщения с клавиатурой
    bot.send_message(message.chat.id, "Привет! Нажми кнопку ниже:", reply_markup=keyboard)


# Обработчик нажатия на кнопку "Привет"
@bot.message_handler(func=lambda message: message.text == "Привет")
def hello_message(message):
    bot.send_message(message.chat.id, "Привет! Как дела?",reply_markup=ReplyKeyboardRemove())


# Запуск бота
bot.polling()