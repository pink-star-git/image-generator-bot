# timer | 2023
# by SapeNeCo

import aiosqlite
import datetime
import asyncio

async def get_time():
    curent_day = datetime.datetime.now()
    return curent_day.strftime('%H:%M:%S')

async def timer():
    while True:
        print('Нынещнее время: ' + await get_time())
        if await get_time() == '12:00:00':
            print('Начинаю обновление базы данных...')
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                async with db.execute("""SELECT id, days, level FROM users""") as cursor:
                    users = await cursor.fetchall()
            for user in users:
                if int(user[2]) == 777 or int(user[2]) == 0:
                    continue
                else:
                    if int(user[1]) > 0:
                        async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                            await db.execute("""UPDATE users SET days = ? WHERE id = ?""", (int(user[1])-1, int(user[0])))
                            await db.commit()
                    elif int(user[1]) == 1:
                        async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                            await db.execute("""UPDATE users SET days = ? WHERE id = ?""", (0, int(user[0])))
                            await db.execute("""UPDATE users SET level = ? WHERE id = ?""", (0, int(user[0])))
                            await db.commit()
                    elif int(user[1]) == 0:
                        async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                            await db.execute("""UPDATE users SET level = ? WHERE id = ?""", (0, int(user[0])))
                            await db.commit()
            print('Успешно!')
        await asyncio.sleep(1)

asyncio.run(timer())