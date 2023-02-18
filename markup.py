import aiosqlite
from telebot import types
from pyqiwip2p import QiwiP2P

QIWI_PRIV_KEY = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImdiMjB4Zy0wMCIsInVzZXJfaWQiOiI3OTUwNTE3NDg2MiIsInNlY3JldCI6IjdkMmIzNDk1ZDVlZDI5NjQ1N2MzYmJhMWE3NjU5NDgzYzdkYjg3ODk4NDdmODczZDUyYTY3MWQxMGY0MDljZTYifX0='

p2p = QiwiP2P(auth_key = QIWI_PRIV_KEY)

messbutton = types.InlineKeyboardMarkup()

barsbutton = types.ReplyKeyboardMarkup()

async def init_bd():
    con = await aiosqlite.connect('bot.db', check_same_thread=False)
    await con.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT,
        bill_id TEXT,
        buy_channel TEXT,
        level INT,
        days INT
    )""")
    await con.commit()
    await con.close()

all_buy = 'У вас максимальный тарифный план'

buttons = {
    'packs': types.InlineKeyboardButton(text='Купить/Улучшить тариф', callback_data='packs'),
    'buy_packs': types.InlineKeyboardButton(text='Как работает бот', callback_data='buy_packs'),
    'buy': types.InlineKeyboardButton(text='Купить', callback_data='buy'),
    'low': types.InlineKeyboardButton(text='Stable Diffusion Low', callback_data='low'),
    'medium': types.InlineKeyboardButton(text='Stable Diffusion Medium', callback_data='medium'),
    'premium': types.InlineKeyboardButton(text='Stable Diffusion Premium', callback_data='premium'),
    'check': types.InlineKeyboardButton(text='Проверить платёж', callback_data='check'),
    'menu': types.InlineKeyboardButton(text='Главное меню', callback_data='start')
}

messages = {
    'hello': 'Привет, я продаю паки, если ты хотел бы, что-то купить, я не против',
    'sells': 'Чтож, у нас с вами есть такой вот ассортимент паков',
    'resend': 'Я вас, увы, не понимаю. Напишите /help.',
    'help': 'Чтобы получить паки напиши мне "/sells"',
    'low': 'Стандартная модель стэбла с NSFW и Неограниченным количеством прокруток',
    'medium': 'Расширенная Версия Бота с широким выбором моделей, NSFW и неограниченным количеством круток',
    'premium': 'Расширенная Версия Бота с широким выбором моделей, Все NSFW модели, Гор, Фурри, Фута и прочие страшные вещи'
}

prices = {
    'low': 250,
    'medium': 600,
    'premium': 1200
}

#Меню оплаты
async def buy(bot, message):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT buy_channel FROM users WHERE id = ?""", (message.chat.id,)) as cursor:
            buy_channel = await cursor.fetchone()
    channel = buy_channel[0]
    comment = str(message.chat.id) + '_' + channel
    bill = p2p.bill(amount = prices[channel], lifetime = 15, comment = comment)
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute("""UPDATE users SET bill_id = ? WHERE id = ?""", (bill.bill_id, message.chat.id,))
        await db.commit()
    buy_btn = types.InlineKeyboardButton(text = "Купить", url = bill.pay_url)
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buy_btn)
    messbutton.add(buttons['check'])
    messbutton.add(buttons['menu'])
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Вы приобретаете тариф Stable Тариф.План\nОзнакомится с получаемыми возможностями, вы можете здесь\nPlaceholder for Price List', reply_markup=messbutton)

#Проверить платёжь
async def check(bot, message):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT bill_id FROM users WHERE id = ?""", (message.chat.id,)) as cursor:
            bill_id = await cursor.fetchone()
    bill = bill_id[0]
    status = p2p.check(bill_id=bill).status
    match status:
        case 'WAITING':
            await bot.send_message(message.chat.id, 'Вы ещё не оплатили')
        case 'REJECTED':
            messbutton = types.InlineKeyboardMarkup()
            messbutton.add(buttons['packs'])
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Счёт откланён, начните оплату сначала', reply_markup=messbutton)
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                await db.execute("""UPDATE users SET bill_id = ? WHERE id = ?""", ('', message.chat.id,))
                await db.execute("""UPDATE users SET buy_channel = ? WHERE id = ?""", ('', message.chat.id,))
                await db.commit()
        case 'EXPIRED':
            messbutton = types.InlineKeyboardMarkup()
            messbutton.add(buttons['packs'])
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Время счёта истекло, начните оплату сначала', reply_markup=messbutton)
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                await db.execute("""UPDATE users SET bill_id = ? WHERE id = ?""", ('', message.chat.id,))
                await db.execute("""UPDATE users SET buy_channel = ? WHERE id = ?""", ('', message.chat.id,))
                await db.commit()
        case 'PAID':
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                async with db.execute("""SELECT buy_channel FROM users WHERE id = ?""", (message.chat.id,)) as cursor:
                    buy_channel = await cursor.fetchone()
            channel = buy_channel[0]
            async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
                await db.execute("""UPDATE users SET bill_id = ? WHERE id = ?""", ('', message.chat.id,))
                await db.execute("""UPDATE users SET buy_channel = ? WHERE id = ?""", ('', message.chat.id,))
                await db.execute("""UPDATE users SET days = ? WHERE id = ?""", (31, message.chat.id,))
                match channel:
                    case 'low':
                        await db.execute("""UPDATE users SET level = ? WHERE id = ?""", (1, message.chat.id,))
                    case 'medium':
                        await db.execute("""UPDATE users SET level = ? WHERE id = ?""", (2, message.chat.id,))
                    case 'premium':
                        await db.execute("""UPDATE users SET level = ? WHERE id = ?""", (3, message.chat.id,))
                await db.commit()
            messbutton = types.InlineKeyboardMarkup()
            messbutton.add(buttons['buy_packs'])
            messbutton.add(buttons['packs'])
            messbutton.add(buttons['menu'])
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Благодарим за покупку. С возможностями вашего тарфного плана, вы можете ознакомится здесь', reply_markup=messbutton)

#Меню встречи
async def main_menu(bot, channel): 
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buttons['packs'])
    if await get_level(channel) != 0:
        messbutton.add(buttons['buy_packs'])
    await bot.send_message(channel, messages['hello'], reply_markup = messbutton)

#Меню встречи через изменение последнего сообщения
async def main_menu_edit(bot, message): 
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buttons['packs'])
    if await get_level(message.chat.id) != 0:
        messbutton.add(buttons['buy_packs'])
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=messages['hello'], reply_markup = messbutton)

#Изменение сообщения
async def edit_message(bot, message, text, channel='', input_buttons = [], buy_buttons=False):
    if channel != '':
        async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
            await db.execute("""UPDATE users SET buy_channel = ? WHERE id = ?""", (channel, message.chat.id,))
            await db.commit()
    if buy_buttons == True:
        match await get_level(message.chat.id):
            case 0:
                messbutton = types.InlineKeyboardMarkup()
                messbutton.add(buttons['low'])
                messbutton.add(buttons['medium'])
                messbutton.add(buttons['premium'])
                messbutton.add(buttons['menu'])
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
            case 1:
                messbutton = types.InlineKeyboardMarkup()
                messbutton.add(buttons['medium'])
                messbutton.add(buttons['premium'])
                messbutton.add(buttons['menu'])
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
            case 2:
                messbutton = types.InlineKeyboardMarkup()
                messbutton.add(buttons['premium'])
                messbutton.add(buttons['menu'])
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
            case 3:
                text = all_buy
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)
    elif input_buttons != []:
        messbutton = types.InlineKeyboardMarkup()
        for button in input_buttons:
            messbutton.add(buttons[button])
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)

#Добавление пользователя в бд
async def insert_user(user_id):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT * FROM users WHERE id = ?""", (user_id,)) as cursor:
            if await cursor.fetchone() is None:
                await db.execute("""INSERT INTO users (id, bill_id, buy_channel, level, days) VALUES (?, ?, ?, ?, ?)""", (user_id, '', '', 0, 0,))
                await db.commit()

#Возвращает уровень доступа пользователя
async def get_level(channel):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT level FROM users WHERE id = ?""", (channel,)) as cursor:
            level = await cursor.fetchone()
    return int(level[0])

#Created by SapeNeCo 2023y.