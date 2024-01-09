import asyncio
from pyrogram import Client

api_id = 23911133
api_hash = "44b5d0a060440c5cfcf3f554bf5650f7"


async def main():
    async with Client("Gorbushkin_resender", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())