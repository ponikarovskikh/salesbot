import asyncio
from pyrogram import *


async def main():
    async with Client("salebot") as app:


        @app.on_message()
        async def print(app,message):
            print(message)
            await app.send_message("me", "Greetings from **Pyrogram**!")

        await app.idle()


asyncio.run(main())
