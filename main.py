# main | 2023
# by SapeNeCo, zebra
import telebot
from telebot.async_telebot import AsyncTeleBot
import markup
import asyncio
from conflib import Configs, Config
# import emoji

configs = Configs()
configs.add_config('main', 'main', '')
main_conf = configs.get_config('main')

token = main_conf.cfg_d['token']
bot = AsyncTeleBot(token)

#Встреча Users
@bot.message_handler(content_types=['text'])
async def message_handler(message):
    match message.text:
        case '/start':
            await markup.insert_user(message)
            await markup.main_menu(bot, message)
        case '/menu' | '/sells' | 'Sells':
            await markup.main_menu(bot, message)
        case '/help':
            await markup.send_message(bot, message, markup.messages['help'])
        case '/bot_help':
            await markup.send_message(bot, message, 'Информация по работе Бота:', input_buttons=['menu', 'buy_packs'])
        case '/property':
            await markup.send_my_property(bot, message)
        case '/modelslist':
            await markup.model_menu(bot, message)
        case '/get_id':
            id:int = await markup.get_value_from_bd("""id""", message.chat.id)
            user_id:int = await markup.get_value_from_bd("""user_id""", message.chat.id)
            await markup.send_message(bot, message, f'👾┃ Откладка для персонала \n┃Chat ID:{id} \n┃ User ID:{user_id}')
        case _:
            if ' ' in message.text:
                await markup.configure(bot, message)
            else:
                await markup.send_message(bot, message, markup.messages['resend'])

#Слушаем Юзера
@bot.callback_query_handler(func=lambda call: True)
async def message_callback(call):
    print(call.data)
    match call.data:
        case 'packs':
            await markup.edit_message(bot, call.message, markup.messages['sells'],  buy_buttons=True,)
        case 'buy_packs':
            await markup.edit_message(bot, call.message, 'Информация по работе Бота:',  input_buttons=['menu'], )
        case 'low':
            await markup.edit_message(bot, call.message, markup.messages['low'], 'low', ['buy', 'menu'],  )
        case 'medium':
            await markup.edit_message(bot, call.message, markup.messages['medium'],  'medium', ['buy', 'menu'], )
        case 'premium':
            await markup.edit_message(bot, call.message,  markup.messages['premium'], 'premium', ['buy', 'menu'], )
        case 'buy':
            await markup.buy(bot, call.message)
        case 'check':
            await markup.check(bot, call.message)
        case 'help':
            await markup.edit_message(bot, call.message, markup.messages['help'], parse_mode="Markdown")
        case 'start':
            await markup.main_menu_edit(bot, call.message)
        case 'my_property':
            await markup.get_my_property(bot, call.message)
        case '':
            for button in markup.buttons:
                if call.data == markup.buttons[f'{button}'].callback_data: 
                    markup.buttons['']
                else:
                    pass
        case _:
            if '/model ' in call.data:
                await markup.model_set(bot, call)
            else:
                await markup.edit_message(bot, call.message, markup.messages['resend'])

asyncio.run(markup.init_bd())
asyncio.run(bot.polling(none_stop=True))