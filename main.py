from app import MafiaApp
from game import Game
import asyncio


async def te(app,name):
    await asyncio.sleep(2)
    await  app.cout(name)

async def main():
    ap=MafiaApp()
    Game.app=ap
    task1=asyncio.create_task(ap.async_run())
    task2=asyncio.create_task(Game.run(3,3,3))
    await task1
    await task2
asyncio.run(main())


