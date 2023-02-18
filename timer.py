import aiosqlite
import datetime
import asyncio

async def get_time():
    curent_day = datetime.datetime.now()
    # return curent_day.strftime('%H %M %S')
    return curent_day.strftime('%S')

async def timer():
    while True:
        print(await get_time())
        if await get_time() == '00':
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                async with db.execute("""SELECT id, days FROM users""") as cursor:
                    users = await cursor.fetchall()
            for user in users:
                if int(user[1]) > 0:
                    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                        await db.execute("""UPDATE users SET days = ? WHERE id = ?""", (int(user[1])-1, int(user[0])))
                        await db.commit()
        await asyncio.sleep(1)

asyncio.run(timer())