import telebot.types
from telebot import *
from telebot.types import (LabeledPrice,Message,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardMarkup,
                           PreCheckoutQuery,SuccessfulPayment)
import config
from sql import *
from keyboards import *
bot =telebot.TeleBot(token=config.token_GorbushkinService)

oplata=0

@bot.message_handler(commands=['start'])
def welcome(msg:Message):

    bot.send_invoice(msg.chat.id,'оплата премиума','вау оплата ', f'buy_premium_{msg.from_user.id}',
                     config.token_yukassa_payment_GorbushkinService,'RUB',[LabeledPrice(
        'купить премиум',100*100)])
    bot.send_message(msg.from_user.id ,f'Наличие премиума у {msg.from_user.username} -'
                                       f' {prem_status(msg.from_user.id) }')






@bot.message_handler(content_types=['text'])
def kb(msg:Message):
    if msg.text=='тест':
        bot.send_message(msg.chat.id,'test',reply_markup=choosing_keyboard_proccess(msg.from_user.id,'product'))


















@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,error_message='error')



@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(msg:Message):
    # print('successful_payment')
    print(msg)
    # message=json.dumps(message,ensure_ascii=False)
    if str(msg.from_user.id).lower() in  str(msg.successful_payment.invoice_payload):
        if controling_premium(msg.from_user.id,new_premium_status=True) ==2:
            bot.send_message(msg.chat.id,
                         f'<b>Оплата прошла успешно!</b> Премиум-тариф будет '
                            f'активен '
                            '30 '
                            'дней\n\n'
                            'Обратная связь по работе бота @SparaOlives',
                            parse_mode='HTML')





@bot.message_handler(content_types=['location'])
def loc(message:Message):
    print(message.location)























bot.polling(non_stop=True)