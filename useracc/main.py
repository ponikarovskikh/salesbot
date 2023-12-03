import asyncio
import json

from pyrogram import *
from pyrogram.types import *
from pyrogram.methods.messages import *
import pyrogram.methods.messages.forward_messages
# api_id = "21438603"
# api_hash = "2267e0fd55c1de4472fa5fadf4d4f451"

# from telebot import *
app = Client("salebot")


# async def main():
#     async with app:
#         await app.send_message("me", "Hiwwww!")
#
#         @app.on_message(filters.command(["start", "help"]))
#         async def my_handler(client, message):
#             print(message)
#
#
# app.run(main())


# api_id = "YOUR_API_ID"
# api_hash = "YOUR_API_HASH"
# bot_token = "YOUR_BOT_TOKEN"

app = Client("salebot")

# Замените "TARGET_GROUP" на username или ID вашей группы
# TARGET_GROUP = "-1001946865525"


@app.on_message(filters)
def forward_to_private_chat(app, message):
    if message.from_user.id!=6304024040:
        print(message)

        user_id=message.from_user.id
        text=message.text
        # print(message.chat.id)
        message_id=message.id
        # print(message_id)
        # Замените "YOUR_PRIVATE_CHAT_ID" на ваш ID личной беседы
        # private_chat_id = "6825936798"
        # try :
        #         chat_member = str(app.get_chat_member(chat_id=message.chat.id, user_id=user_id))
        #         chat_member = json.loads(chat_member)['user']
        #
        # except Exception as e:
        #         print('Жопа с правами')
        # # chat_member=json.loads(chat_member)['user']
        # print(chat_member.keys())
        resolve=json.loads(str(message.from_user))

        if 'username' in resolve.keys():
                usrnm = message.from_user.username

                print('-------------\n',resolve['username'])
                print(message.text)
                app.send_message(text=f'set_@_{user_id}_@_{usrnm}_@_set' \
                                      f'{message.text}', chat_id=-1001901838848)
                pass
        else:
                pass

        # print(chat_member)
        # username=chat_member['username']
        # user_id=chat_member['id']
        # username,user_id
        # chat_member=str(chat_member)
        # chat_member=dict(chat_member)
        # print(chat_member)
        # if 'username' in chat_member.keys():


        # app.forward_messages(chat_id= -4031390915,from_chat_id=message.from_user.id,message_ids=[message.id])

# Запуск бота в бесконечном цикле
app.run()
