import json

import asyncio
from pyrogram import Client

#
# async def main():
#     async with Client("salesbot") as app:
#         await app.send_message("me", "Greetings from **Pyrogram**! agagin")
#
#
# asyncio.run(main())



app = Client("salesbot")

# Замените "TARGET_GROUP" на username или ID вашей группы
# TARGET_GROUP = "-1001946865525"


@app.on_message(filters=['group'])
def forward_to_private_chat(app, message):

    if int(message.from_user.id)!=6724529493:
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
                    app.send_message(text=f'set_@_{user_id}_@_{usrnm}_@_set' \
                                          f'{message.text}', chat_id=-1001869659170)




    # Запуск бота в бесконечном цикле
app.run()
