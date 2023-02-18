from telebot.async_telebot import AsyncTeleBot
import markup
import asyncio

token = '5414533028:AAHMccLySMnGHXcb2r65iI7qQn3tghpnvB8'
bot = AsyncTeleBot(token)

#Встреча Users
@bot.message_handler(content_types=['text'])
async def message_handler(message):
    match message.text:
        case '/start':
            await markup.insert_user(message.chat.id)
            await markup.main_menu(bot, message.chat.id)
        case '/menu' | '/sells' | 'Sells':
            await markup.main_menu(bot, message.chat.id)
        case '/help':
            await bot.send_message(message.chat.id, markup.messages['help'])
        case '/property':
            await markup.edit_message(bot, message, 'Затычка конфиг ссылки', input_buttons=['menu'])
        case _:
            if '_' in message.text:
                match message.text.split(' ')[0]:
                    case '/model':
                        pass
                    case '/CFG':
                        pass
                    case '/weight':
                        pass
                    case '/countpic':
                        pass
                    case '/sampler':
                        pass
                    case '/prompts' | '/generate':
                        pass
            else: await bot.send_message(message.chat.id, markup.messages['resend'])

#Слушаем Юзера
@bot.callback_query_handler(func=lambda call: True)
async def message_callback(call):
    match call.data:
        case 'packs':
            await markup.edit_message(bot, call.message, markup.messages['sells'], buy_buttons=True)
        case 'buy_packs':
            await markup.edit_message(bot, call.message, 'Затычка конфиг ссылки', input_buttons=['menu'])
        case 'low':
            await markup.edit_message(bot, call.message, markup.messages['low'], 'low', ['buy', 'menu'])
        case 'medium':
            await markup.edit_message(bot, call.message, markup.messages['low'], 'medium', ['buy', 'menu'])
        case 'premium':
            await markup.edit_message(bot, call.message, markup.messages['low'], 'premium', ['buy', 'menu'])
        case 'buy':
            await markup.buy(bot, call.message)
        case 'check':
            await markup.check(bot, call.message)
        case 'help':
            await markup.edit_message(bot, call.message, markup.messages['help'])
        case 'start':
            await markup.main_menu_edit(bot, call.message)
        case _:
            await markup.edit_message(bot, call.message, markup.messages['resend'])

asyncio.run(markup.init_bd())
asyncio.run(bot.polling(none_stop=True))

#Created by SapeNeCo 2023y.