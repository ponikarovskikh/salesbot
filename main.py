import asyncio

from botcheck import *
from userbotscript import *







async def main():
    mainbottask=asyncio.create_task(mainbot(bot))
    userbottask=asyncio.create_task(userbot(app.run()))

    await asyncio.gather(mainbottask,userbottask)

if __name__ == "__main__":
    asyncio.run(main())