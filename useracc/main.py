import json

import asyncio
import time

from pyrogram import Client

#
# async def main():
#     async with Client("salesbot") as app:
#         await app.send_message("me", "Greetings from **Pyrogram**! agagin")
#
#
# asyncio.run(main())
app = Client("salesbot")
async def bot(app):
    print('pfgeo')


    # Замените "TARGET_GROUP" на username или ID вашей группы
    # TARGET_GROUP = "-1001946865525"

    async def send_message_with_interval(app, chat_id, text, interval):
        await asyncio.sleep(interval)
        await app.send_message(chat_id=chat_id, text=text)



    @app.on_message()
    async def forward_to_private_chat(app, message):

        if int(message.from_user.id)!=6724529493:
            if int(message.chat.id) != -1001869659170:
                CANAL=message.chat.title
                user_id=message.from_user.id
                text=message.text
                resolve=json.loads  (str(message.from_user))

                if 'username' in resolve.keys():
                    if 'bot' not in text.lower() and "True"  not in str(resolve['is_bot']):
                        usrnm = message.from_user.username
                        if 'куплю' or 'предложите' or 'ищу' in text.lower() :
                            # print('-------------\n',resolve['username'])
                            # print(message.text)

                            task_list.append(send_message_with_interval(app, -1001869659170,f'set_@_{user_id}_@'
                                                                                             f'_{usrnm}_@_set'
                                                                                                                 f''
                                                                                            f'{message.text}', 2))



                            # await  app.send_message(text=f'set_@_{user_id}_@_{usrnm}_@_set' \
                            #                       f'{message.text}', chat_id=-1001869659170)
                            # except Exception as e:
                            #     print(e)

async def checking ():
    while True:

        await asyncio.sleep(1)
        print(task_list,len(task_list))
        if len(task_list)>=30:
            for task in task_list:
                await task
            task_list.clear()
async def main():
    global task_list
    task_list=[]
    await asyncio.gather (asyncio.create_task(checking()),asyncio.create_task(bot(await app.start())))


    # Запуск бота в бесконечном цикле
if __name__ == '__main__':
    app.run(main())
