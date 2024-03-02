# from telebot import TeleBot
# from telebot import types
# from telebot.types import *
# import config
# bot=TeleBot(token=config.super_test)
#
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     # Создание клавиатуры
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button_hello = types.KeyboardButton("Привет")
#     keyboard.add(button_hello)
#
#     # Отправка приветственного сообщения с клавиатурой
#     bot.send_message(message.chat.id, "Привет! Нажми кнопку ниже:", reply_markup=keyboard)
#
#
# # Обработчик нажатия на кнопку "Привет"
# @bot.message_handler(func=lambda message: message.text == "Привет")
# def hello_message(message):
#     bot.send_message(message.chat.id, "Привет! Как дела?",reply_markup=ReplyKeyboardRemove())
#
#
# # Запуск бота
# bot.polling()

# r_nom_monthly = 0.12
#
# # Периоды начисления
# n_monthly = 12
# n_quarterly = 4
#
# # Перевод в эффективную ставку
# r_eff = (1 + r_nom_monthly / n_monthly)**n_monthly - 1
#
# # Перевод обратно в номинальную ставку при ежеквартальном начислении
# r_nom_quarterly = n_quarterly * ((1 + r_eff)**(1/n_quarterly) - 1)
#
# print(r_eff)
# print(r_nom_quarterly)


from scipy.optimize import fsolve

# Заданные параметры
# PV = 460000  # Полученная сумма
# FV = 500000  # Сумма векселя
# n_months = 5  # Срок векселя в месяцах
# n_years = n_months / 12  # Перевод срока в годы
#
# # Функция для определения корня уравнения
# def find_r(r):
#     return PV - FV / ((1 + r)**n_years)
#
# # Начальное приближение ставки
# initial_guess = 0.1
#
# # Решение уравнения
# r_solution = fsolve(find_r, initial_guess)[0]
#
# print(r_solution, r_solution * 100)

# FV = 5000000  # Будущая стоимость кредита
# r1, r2, r3, r4, r5 = 0.19, 0.20, 0.205, 0.21, 0.21  # Ставки процентов по годам
#
# # Расчет современной величины кредита
# PV = FV / ((1 + r1) * (1 + r2) * (1 + r3) * (1 + r4) * (1 + r5))
# print(PV)