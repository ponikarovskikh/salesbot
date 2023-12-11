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
    print(message)
    if int(message.from_user.id)!=6825936798:
        if int(message.chat.id) != -1001869659170:


            CANAL=message.chat.title
            user_id=message.from_user.id
            text=message.text
            resolve=json.loads  (str(message.from_user))

            if 'username' in resolve.keys():
                if 'bot' not in text.lower() and "True"  not in str(resolve['is_bot']):
                    usrnm = message.from_user.username

                    print('-------------\n',resolve['username'])
                    print(message.text)
                    app.send_message(text=f'{CANAL}\n\n    set_@_{user_id}_@_{usrnm}_@_set' \
                                          f'{message.text}', chat_id=-1001869659170)




    # Запуск бота в бесконечном цикле
app.run()
