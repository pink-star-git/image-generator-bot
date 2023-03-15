# markup | 2023
# by SapeNeCo, zebra

import aiosqlite
from telebot import types
from pyqiwip2p import QiwiP2P
from PIL import Image
from conflib import Configs, Config
from req import Req2neuro
import random 
from random import random, randrange, randint
# QIWI_PRIV_KEY = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImdiMjB4Zy0wMCIsInVzZXJfaWQiOiI3OTUwNTE3NDg2MiIsInNlY3JldCI6IjdkMmIzNDk1ZDVlZDI5NjQ1N2MzYmJhMWE3NjU5NDgzYzdkYjg3ODk4NDdmODczZDUyYTY3MWQxMGY0MDljZTYifX0='

configs = Configs()
configs.add_config('main', 'main', '')
main_conf = configs.get_config('main')

p2p = QiwiP2P(auth_key = main_conf.cfg_d['QIWI_PRIV_KEY'])

messbutton = types.InlineKeyboardMarkup()

barsbutton = types.ReplyKeyboardMarkup()


async def init_bd():
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT,
            id BIGINT,
            bill_id TEXT,
            buy_channel TEXT,
            level INT,
            days INT,
            model TEXT,
            cfg REAL,
            size_height INT,
            size_width INT,
            countpic INT,
            sampler TEXT
        )""")
        await db.commit()

all_buy = 'У вас максимальный тарифный план'

buttons = {
    'packs':       types.InlineKeyboardButton(text='💸┃ Купить/Улучшить тариф', callback_data='packs'),
    'packs_info':  types.InlineKeyboardButton(text='ℹ️┃ Тарифы', url='https://v-v.host/tariffs/'),
    'buy_packs':   types.InlineKeyboardButton(text='ℹ️ ┃Как работает бот', url='https://v-v.host/how_work_bot/'),
    'my_property': types.InlineKeyboardButton(text='ℹ️ ┃ Ваши настройки', callback_data='my_property'),
    'buy':      types.InlineKeyboardButton(text='Купить', callback_data='buy'),
    'low':      types.InlineKeyboardButton(text=' ✨🌝┃ Stable Diffusion Low | 250p', callback_data='low'),
    'medium':   types.InlineKeyboardButton(text=' 🌗┃Stable Diffusion Medium | 600p', callback_data='medium'),
    'premium':  types.InlineKeyboardButton(text=' 🌚✨┃Stable Diffusion Premium | 1200p', callback_data='premium'),
    'check':    types.InlineKeyboardButton(text='🔃┃Проверить платёж', callback_data='check'),
    'menu':     types.InlineKeyboardButton(text='ℹ️┃Главное меню', callback_data='start'),

    #models button
    'StableDiffusion-1.5':  types.InlineKeyboardButton(text='StableDiffusion-1.5', callback_data='/model StableDiffusion-1.5'),
    'StableDiffusion-2.0':  types.InlineKeyboardButton(text='StableDiffusion-2.0', callback_data='/model StableDiffusion-2.0'),
    'StableDiffusion-2.1':  types.InlineKeyboardButton(text='StableDiffusion-2.1', callback_data='/model StableDiffusion-2.1'),
    'DreamLike-0-2':        types.InlineKeyboardButton(text='DreamLike-0-2', callback_data='/model DreamLike-0-2'),
    'DreamLike-0-1':        types.InlineKeyboardButton(text='DreamLike-0-1', callback_data='/model DreamLike-0-1'),
    'PastelMix':            types.InlineKeyboardButton(text='PastelMix', callback_data='/model PastelMix'),
    'EimisAnimeDiffusion':  types.InlineKeyboardButton(text='EimisAnimeDiffusion', callback_data='/model EimisAnimeDiffusion'),
    'Deliberate':           types.InlineKeyboardButton(text='Deliberate', callback_data='/model Deliberate'),
    'Realistic-vision-v13': types.InlineKeyboardButton(text='Realistic-vision-v13', callback_data='/model Realistic-vision-v13'),
    'ChilloutMix':          types.InlineKeyboardButton(text='ChilloutMix', callback_data='/model ChilloutMix'),
    'Grapefruit':           types.InlineKeyboardButton(text='Grapefruit', callback_data='/model Grapefruit'),
    'Project-Unreal':       types.InlineKeyboardButton(text='Project-Unreal', callback_data='/model Project-Unreal'),
    'Wlop':                 types.InlineKeyboardButton(text='wlop', callback_data='/model Wlop'),
    'Ayonimix':             types.InlineKeyboardButton(text='ayonimix', callback_data='/model Ayonimix'),
    'Kotosmix':             types.InlineKeyboardButton(text='kotosmix', callback_data='/model Kotosmix'),
    'Furtasticv':           types.InlineKeyboardButton(text='Furtasticv', callback_data='/model Furtasticv'),
    'FutaGen':              types.InlineKeyboardButton(text='FutaGen', callback_data='/model FutaGen'),
}

messages = {
    'hello': 'О, здрввствуйте! Вы из [паблика "Я влюбился в нейросеть"](https://vk.com/iloveyouneyroweb)?\nЯ ваша нейросеть и я умею генерировать картинки за месячную подписку. \n\nДавай пройдёмся, по тому, какие картинки тебе нужны и сколько это выйдет в месяц.\n[Вот список тарифов^^](http://example.com/link)',
    'hello_client': 'Главное меню \n 🌟┃ Тебя что-то интересует, солнце?',
    'sells': 'Чтож, у меня, есть такой вот ассортимент тарифов, что тебе подходит?',
    'resend': '❓┃ Я тебя, увы, не понимаю. \nПроверьте написание команды/аргуметов. Или напишите /help.',
    'help': '❓┃ Чтобы получить список тарифов напиши мне `/sells` \nЧтобы получить информацию по работе бота введи /bot_help',
    'low': 'ℹ️ ┃ Стандартная модель стэбла с NSFW и Неограниченным количеством прокруток,\nВсего за 250р/мес', 
    'medium': 'ℹ️ ┃ Расширенная Версия Бота с широким выбором моделей, NSFW и неограниченным количеством круток \n600р/мес',
    'premium': 'ℹ️ ┃ Расширенная Версия Бота с широким выбором моделей, Все NSFW модели, Гор, Фурри, Фута и прочие страшные вещи.\n1200р/мес'
}

prices = {
    'low': 250,
    'medium': 600,
    'premium': 1200
}

max_height = {
    'low': 728,
    'medium': 1024,
    'premium': 2048
}

max_width = {
    'low': 728,
    'medium': 1024,
    'premium': 2048
}

min_height = {
    'low': 0,
    'medium': 0,
    'premium': 0
}

min_width = {
    'low': 0,
    'medium': 0,
    'premium': 0
}

min_countpic = {
    'low': 1,
    'medium': 1,
    'premium': 1
}

max_countpic = {
    'low': 4,
    'medium': 8,
    'premium': 12
}

#Ключи моделей | models key

models_low = [
    'StableDiffusion-1.5',
    'StableDiffusion-2.0',
    'StableDiffusion-2.1',
    'DreamLike-0-1',
    'DreamLike-0-2',
    'PastelMix',
    'EimisAnimeDiffusion'
]

models_medium = [
    'StableDiffusion-1.5',
    'StableDiffusion-2.0',
    'StableDiffusion-2.1',
    'DreamLike-0-1',
    'DreamLike-0-2',
    'PastelMix',
    'EimisAnimeDiffusion',
    'Deliberate',
    'Realistic-vision-v13',
    'ChilloutMix',
    'Grapefruit'
]

models_premium = [
    'StableDiffusion-1.5',
    'StableDiffusion-2.0',
    'StableDiffusion-2.1',
    'DreamLike-0-1',
    'DreamLike-0-2',
    'PastelMix',
    'EimisAnimeDiffusion',
    'Deliberate',
    'Realistic-vision-v13',
    'ChilloutMix',
    'Grapefruit',
    'Project-Unreal',
    'Wlop',
    'Ayonimix',
    'Kotosmix',
    'Furtasticv'
]

models = {
    'StableDiffusion-1.5':  'StableDiffusion-1-5.ckpt',
    'StableDiffusion-2.0':  'StableDiffusion-2-0.ckpt',
    'StableDiffusion-2.1':  'StableDiffusion-2-1.ckpt',
    'DreamLike-0-2':        'DreamLike-0-2.ckpt',
    'DreamLike-0-1':        'DreamLike-0-1.ckpt',
    'PastelMix':            'PastelMix.safetensors',
    'EimisAnimeDiffusion':  'EimisAnimeDiffusion.safetensors',
    'Deliberate':           'Deliberate.safetensors',
    'Realistic-vision-v13': 'Realistic-vision-v13.safetensors',
    'ChilloutMix':          'ChilloutMix.safetensors',
    'Grapefruit':           'grapefruit-hentai-model.safetensors',
    'Project-Unreal':       'project-unreal-engine-5.ckpt',
    'Wlop':                 'wlop.ckpt',
    'Ayonimix':             'ayonimix.safetensors',
    'Kotosmix':             'kotosmix.safetensors',
    'Furtasticv':           'furtasticv11.safetensors',
    'FutaGen' :             'futagen.safetensors'
}


#Меню оплаты
async def buy(bot, message):
    channel = await get_value_from_bd("""buy_channel""", message.chat.id)
    comment = str(message.chat.id) + '_' + channel
    bill = p2p.bill(amount = prices[channel], lifetime = 15, comment = comment)
    await set_value_in_bd("""bill_id""", bill.bill_id, message.chat.id)
    buy_btn = types.InlineKeyboardButton(text = "Купить", url = bill.pay_url)
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buy_btn)
    messbutton.add(buttons['check'])
    messbutton.add(buttons['menu'])
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Вы приобретаете тариф **Stable Diffusion** Тариф.План\nОзнакомится с получаемыми возможностями, вы можете здесь Placeholder for Price List',  reply_markup=messbutton)

#Проверить платёж
async def check(bot, message):
    bill = await get_value_from_bd("""bill_id""", message.chat.id)
    status = p2p.check(bill_id=bill).status
    match status:
        case 'WAITING':
            await send_message(bot, message, '❓┃ Вы ещё не оплатили')
        case 'REJECTED':
            await set_value_in_bd("""bill_id""", '', message.chat.id)
            await set_value_in_bd("""buy_channel""", '', message.chat.id)
            await edit_message(bot, message, '❌┃ Счёт откланён, начните оплату сначала',  input_buttons=['packs'])
        case 'EXPIRED':
            await set_value_in_bd("""bill_id""", '', message.chat.id)
            await set_value_in_bd("""buy_channel""", '', message.chat.id)
            await edit_message(bot, message, '❌┃Время счёта истекло, начните оплату сначала',  input_buttons=['packs'])
        case 'PAID':
            match get_value_from_bd("""buy_channel""", message.chat.id):
                case 'low':
                    await set_value_in_bd("""level""", 1, message.chat.id)
                case 'medium':
                    await set_value_in_bd("""level""", 2, message.chat.id)
                case 'premium':
                    await set_value_in_bd("""level""", 3, message.chat.id)
            await set_value_in_bd("""bill_id""", '', message.chat.id)
            await set_value_in_bd("""buy_channel""", '', message.chat.id)
            await set_value_in_bd("""days""", 31, message.chat.id)
            await edit_message(bot, message, '✅┃ Спасибо за покупку. С возможностями вашего тарфного плана, вы можете ознакомится здесь',  input_buttons=['buy_packs', 'packs', 'menu'])

#Конфигурация бота
async def configure(bot, message):
    print(message.text)
    match int(await get_value_from_bd("""level""", message.chat.id)):
        case 0:
            await send_message(bot, message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
        case 1:
            match message.text.split(' ')[0]:
                case '/model':
                    if message.text.split(' ')[1] in models_low:
                        await set_value_in_bd("""model""", models[message.text.split(' ')[1]], message.chat.id)
                        await send_message(bot, message, '✅┃ Конфигураци `model` поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/cfg':
                    if message.text.split(' ')[1] >= 0:
                        await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, '✅┃ Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Введите, пожалуйста положительное число, или 0. Рекомендую от 6 - 7.5 - 8. Работает эффективно',  input_buttons=['buy_packs', 'menu'])
                case '/size':
                    if len(message.text.split(' ')) == 3:
                        height = int(message.text.split(' ')[1])
                        width = int(message.text.split(' ')[2])
                        if height >= min_height['low'] and height <= max_height['low'] and width >= min_width['low'] and width <= max_width['low']:
                            await set_value_in_bd("""size_height""", height, message.chat.id)
                            await set_value_in_bd("""size_width""", width, message.chat.id)
                            await send_message(bot, message, '✅┃ Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
                        else:
                            await send_message(bot, message, '❌┃ Вам не доступны такие размеры изображения. \nПочитайте возможности конфигурации для вашего тарифа',   input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❗┃ Введите пожалуйста размеры желательного изображения в формате `/size [height] [width]`',  parse_mode="Markdown")
                case '/countpic':
                    if int(message.text.split(' ')[1]) >= min_countpic['low'] and int(message.text.split(' ')[1]) <= max_countpic['low']:
                        await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, f'✅┃ Конфигурация `/countpic` поставлена на значение {message.text.split(" ")[1]}',  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/sampler':
                    await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
                    await send_message(bot, message, '✅┃ Конфигураци `sampler` поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                case '/generate' | '/prompts':
                    await generate(bot, message)
                case _:
                    await send_message(bot, message, messages['resend'])
        #Stable Diffusion Medium
        case 2:
            match message.text.split(' ')[0]:
                case '/model':
                    if message.text.split(' ')[1] in models_medium:
                        await set_value_in_bd("""model""",  models[message.text.split(' ')[1]], message.chat.id)
                        await send_message(bot, message, '✅┃ Конфигураци `model` поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/cfg':
                    if message.text.split(' ')[1] >= 0:
                        await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, '✅┃ Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Введите, пожалуйста положительное число, или 0. Рекомендую от 6 - 7.5 - 8. Работает эффективно',  input_buttons=['buy_packs', 'menu'])
                case '/size':
                    if len(message.text.split(' ')) == 3:
                        height = int(message.text.split(' ')[1])
                        width = int(message.text.split(' ')[2])
                        if height >= min_height['medium'] and height <= max_height['medium'] and width >= min_width['medium'] and width <= max_width['medium']:
                            await set_value_in_bd("""size_height""", height, message.chat.id)
                            await set_value_in_bd("""size_width""", width, message.chat.id)
                            await send_message(bot, message, '✅┃ Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
                        else:
                            await send_message(bot, message, '❌┃ Вам не доступны такие размеры изображения. \nПочитайте возможности конфигурации для вашего тарифа',   input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❗┃ Введите пожалуйста размеры желательного изображения в формате `/size [height] [width]`',  parse_mode="Markdown")
                case '/countpic':
                    if int(message.text.split(' ')[1]) >= min_countpic['medium'] and int(message.text.split(' ')[1]) <= max_countpic['medium']:
                        await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, f'✅┃ Конфигурация `/countpic` поставлена на значение {message.text.split(" ")[1]}',  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, '❌┃ Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/sampler':
                    await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
                    await send_message(bot, message, '✅┃ Конфигураци `sampler` поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                case '/generate' | '/prompts':
                    await generate(bot, message)
                case _:
                    await send_message(bot, message, messages['resend'])
        case 3 | 777:
            match message.text.split(' ')[0]:
                case '/model':
                    if message.text.split(' ')[1] in models_premium:
                        await set_value_in_bd("""model""",  models[message.text.split(' ')[1]], message.chat.id)
                        await send_message(bot, message, 'Конфигураци model поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, 'Нет такой модели, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/cfg':
                    if message.text.split(' ')[1] >= 0:
                        await set_value_in_bd("""cfg""", float(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, 'Конфигураци cfg поставлена на ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, 'Введите, пожалуйста положительное число, или 0',  input_buttons=['buy_packs', 'menu'])
                case '/size':
                    if len(message.text.split(' ')) == 3:
                        height = int(message.text.split(' ')[1])
                        width = int(message.text.split(' ')[2])
                        if height >= min_height['premium'] and height <= max_height['premium'] and width >= min_width['premium'] and width <= max_width['premium']:
                            await set_value_in_bd("""size_height""", height, message.chat.id)
                            await set_value_in_bd("""size_width""", width, message.chat.id)
                            await send_message(bot, message, 'Конфигураци size поставлена на значения ' + message.text.split(' ')[1] + ' ' + message.text.split(' ')[2],  input_buttons=['buy_packs', 'menu'])
                        else:
                            await send_message(bot, message, 'Вам не доступны такие размеры изображения, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, 'Введите пожалуйста размеры желательного изображения в формате /size [height] [width]')
                case '/countpic':
                    if int(message.text.split(' ')[1]) >= min_countpic['premium'] and int(message.text.split(' ')[1]) <= max_countpic['premium']:
                        await set_value_in_bd("""countpic""", int(message.text.split(' ')[1]), message.chat.id)
                        await send_message(bot, message, 'Конфигураци countpic поставлена на значение ' + int(message.text.split(' ')[1]),  input_buttons=['buy_packs', 'menu'])
                    else:
                        await send_message(bot, message, 'Вам не доступно такое количество картинок на обработку, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])
                case '/sampler':
                    await set_value_in_bd("""sampler""", message.text.split(' ')[1], message.chat.id)
                    await send_message(bot, message, 'Конфигураци sampler поставлена на значение ' + message.text.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
                case '/generate' | '/prompts':
                    await generate(bot, message)
                case _:
                    await send_message(bot, message, messages['resend'])

async def send_modelslist(bot, message):
    match int(await get_value_from_bd("""level""", message.chat.id)):
        case 0:
                    await send_message(bot, message, "❗┃ Вы ещё не приобрели тариф, вам не доступна эта команда")
        case 1:
                    await send_message(bot, message, f'┬'+'\n├'.join(models_low))
        case 2:
                    await send_message(bot, message, f'┬'+'\n├'.join(models_medium))
        case 3 | 777:
                    await send_message(bot, message, f'┬'+'\n├'.join(models_premium))

#Меню встречи
async def main_menu(bot, message): 
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buttons['packs'], buttons['packs_info'])
    message_local = messages['hello']
    if int(await get_value_from_bd("""level""", message.chat.id)) != 0:
        messbutton.add(buttons['buy_packs'])
        messbutton.add(buttons['my_property'])
        message_local = messages['hello_client']
    await bot.send_message(message.chat.id, message_local,  reply_markup = messbutton, parse_mode="Markdown")

#Меню встречи через изменение последнего сообщения
async def main_menu_edit(bot, message): 
    messbutton = types.InlineKeyboardMarkup()
    messbutton.add(buttons['packs'])
    message_local = messages['hello']
    if int(await get_value_from_bd("""level""", message.chat.id)) != 0:
        messbutton.add(buttons['buy_packs'])
        messbutton.add(buttons['my_property'])
        message_local = messages['hello_client']
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_local, parse_mode="Markdown",  reply_markup = messbutton)

#Изменение сообщения
async def edit_message(bot, message, text, channel='', input_buttons = [], buy_buttons=False, ):
    if channel != '':
        async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
            await db.execute("""UPDATE users SET buy_channel = ? WHERE id = ?""", (channel, message.chat.id,))
            await db.commit()
    if buy_buttons == True:
        match int(await get_value_from_bd("""level""", message.chat.id)):
            case 0:
                await edit_message(bot, message, text, input_buttons=['low', 'medium', 'premium', 'menu', 'packs_info'])
            case 1:
                await edit_message(bot, message, text, input_buttons=['medium', 'premium', 'menu', 'packs_info'])
            case 2:
                await edit_message(bot, message, text, input_buttons=['premium', 'menu', 'packs_info'])
            case 3:
                await edit_message(bot, message, all_buy)
    elif input_buttons != []:
        messbutton = types.InlineKeyboardMarkup()
        for button in input_buttons:
            messbutton.add(buttons[button])
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=messbutton)
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)



#Отправка сообщения
async def send_message(bot, message, text, input_buttons = []):
    if input_buttons != []:
        messbutton = types.InlineKeyboardMarkup()
        for button in input_buttons:
            messbutton.add(buttons[button])
        await bot.send_message(message.chat.id, text, reply_markup=messbutton)
    else:
        await bot.send_message(message.chat.id, text)

#Отправка фото
async def send_photo(bot, message, img:Image=None):
        await bot.send_photo(message.chat.id, photo=img)

#Добавление пользователя в бд
async def insert_user(message):
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute("""SELECT * FROM users WHERE id = ?""", (message.chat.id,)) as cursor:
            if await cursor.fetchone() is None:
                await db.execute("""INSERT INTO users (user_id, id, bill_id, buy_channel, level, days, model, cfg, size_height, size_width, countpic, sampler) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                                    (message.from_user.id, message.chat.id, '', '', 0, 0, 'PastelMix.ckpt', 7.5, 256, 256, 2, 'DPM2'))
                await db.commit()

#Получаем значение из бд по колонке и id чата
async def get_value_from_bd(colum, id): #значение colum ВСЕГДА должно идти в тройных двойных ковычках, тоесть """[colum]"""
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        async with db.execute(f"""SELECT {colum} FROM users WHERE id = ?""", (id,)) as cursor:
            colum_ans = await cursor.fetchone()
    return colum_ans[0]

#Ставим значение в бд по колонке и id чата
async def set_value_in_bd(colum, value, id): #значение colum ВСЕГДА должно идти в тройных двойных ковычках, тоесть """[colum]"""
    async with aiosqlite.connect('bot.db', check_same_thread=False) as db:
        await db.execute(f"""UPDATE users SET {colum} = ? WHERE id = ?""", (value, id,))
        await db.commit()

#получение конфигурации пользователя
async def get_my_property(bot, message):
    height = await get_value_from_bd("""size_height""", message.chat.id)
    width = await get_value_from_bd("""size_width""", message.chat.id)
    model = await get_value_from_bd("""model""", message.chat.id)
    cfg_scale = await get_value_from_bd("""cfg""", message.chat.id)
    n_iter = await get_value_from_bd("""countpic""", message.chat.id)
    sampler = await get_value_from_bd("""sampler""", message.chat.id)
    await edit_message(bot, message, text= f"ℹ️ ┃ Ваши настройки:\n\nРазмеры картинки:\n ┃ {height} x {width}\n\nМодель:\n ┃ {model}\n\nКоэфициент точности:\n ┃ {cfg_scale}\n\nКоличество картинок:\n ┃ {n_iter}\n\nСэмплер:\n ┃ {sampler}")


#Отправка конфигурации пользователя /property
async def send_my_property(bot, message):
    height = await get_value_from_bd("""size_height""", message.chat.id)
    width = await get_value_from_bd("""size_width""", message.chat.id)
    model = await get_value_from_bd("""model""", message.chat.id)
    cfg_scale = await get_value_from_bd("""cfg""", message.chat.id)
    n_iter = await get_value_from_bd("""countpic""", message.chat.id)
    sampler = await get_value_from_bd("""sampler""", message.chat.id)
    await send_message(bot, message, text= f"ℹ️ ┃ Ваши настройки:\n\nРазмеры картинки:\n /size\n ┃ {height} x {width}\n\nМодель:\n /model\n ┃ {model}\n\nКоэфициент точности:\n /cfg\n ┃ {cfg_scale}\n\nКоличество картинок:\n /countpic\n ┃ {n_iter}\n\nСэмплер:\n/sampler \n ┃ {sampler}")




async def model_menu(bot, message):
    level = int(await get_value_from_bd("""level""", message.chat.id))
    match level:
        case 0:
            await send_message(bot, message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
        case 1 | 2 | 3 | 777:
            await send_message(bot, message, text= f"Ваш список моделей", input_buttons=(models_low if level == 1 else models_medium if level == 2 else models_premium if level == 3 else models_premium if level == 777 else 'fuck'))

async def model_set(bot, call):
    level = int(await get_value_from_bd("""level""", call.message.chat.id))
    match level:
        case 0:
            await send_message(bot, call.message, '❌┃ Вам пока не доступна настройка бота, купите тариф для того, чтобы пользоваться нашим ботом',  input_buttons=['packs', 'menu'])
        case 1 | 2 | 3 | 777:
            if call.data.split(' ')[1] in (models_low if level == 1 else models_medium if level == 1 else models_premium if level == 3 else models_premium if level == 777 else 'fuck'):
                await set_value_in_bd("""model""",  models[call.data.split(' ')[1]], call.message.chat.id)
                await send_message(bot, call.message, '✅┃ Конфигураци `model` поставлена на ' + call.data.split(' ')[1],  input_buttons=['buy_packs', 'menu'])
            else:
                await send_message(bot, call.message, '❌┃ Нет такой модели или вам она недоступна, почитайте возможности конфигурации',  input_buttons=['buy_packs', 'menu'])

#генерация запроса в нейросеть
async def generate(bot, message):
    height:int = await get_value_from_bd("""size_height""", message.chat.id)
    width:int = await get_value_from_bd("""size_width""", message.chat.id)
    model:str = await get_value_from_bd("""model""", message.chat.id)
    cfg_scale:float = await get_value_from_bd("""cfg""", message.chat.id)
    n_iter:int = await get_value_from_bd("""countpic""", message.chat.id)
    sampler:str = await get_value_from_bd("""sampler""", message.chat.id)
    pr:str = ' '.join([i for n,i in enumerate(message.text.split(' ')) if n > 0])
    prompt:str = pr
    negative_prompt:str = ''
    if '!' in pr:
        prompts = pr.split('!')
        prompt = prompts[0]
        negative_prompt = prompts[1]
    
    message_num = randint(1, 3)
    if message_num == 1:
        message_local = "🔃┃ Дай подумать, что-то покажу"
    elif message_num == 2:
        message_local = "🔃┃ Подожди, я думаю. Как будет готово, покажу(^3^)"
    elif message_num == 3:
        message_local = "🔃┃ В оброботке, подожди чуток"
    await send_message(bot, message, message_local)
    await Req2neuro(url_=main_conf.cfg_d['url_sd_server'], prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, cfg_scale=cfg_scale, model=model, sampler=sampler, n_iter=n_iter, steps=25, func=send_photo, bot=bot, message=message)

    if message_num == 1:
        message_local = "✅┃ Всё готово, смотри"
    elif message_num == 2:
        message_local = "✅┃ Ого, что приготовилось!:з"
    elif message_num == 3:
        message_local = "✅┃ Вот ваш заказ"
    await send_message(bot, message, message_local, parse_mode="Markdown")