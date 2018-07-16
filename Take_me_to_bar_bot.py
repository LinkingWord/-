import logging
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import telegram

import bot_settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}


bars = None
bar_counter = 0
has_bot_stoped = False


def start_bot(bot, update):
    
    first_greeting = 'Привет, {}!'.format(update.message.chat.first_name, '/start')
    update.message.reply_text(first_greeting)

    button_list = [
        [telegram.InlineKeyboardButton(bars[0]['Cells']['Name'] + ': ' + bars[0]['Cells']['Address'], callback_data=first_greeting)],
        [telegram.InlineKeyboardButton(bars[1]['Cells']['Name'] + ': ' + bars[1]['Cells']['Address'], callback_data=first_greeting)],
        [telegram.InlineKeyboardButton(bars[2]['Cells']['Name'] + ': ' + bars[2]['Cells']['Address'], callback_data=first_greeting)],
        [telegram.InlineKeyboardButton(bars[3]['Cells']['Name'] + ': ' + bars[3]['Cells']['Address'], callback_data=first_greeting)],
        [telegram.InlineKeyboardButton('Завершить', callback_data='/stop'), 
        telegram.InlineKeyboardButton('Продолжить', callback_data='/next')]
        ]

    reply_markup = telegram.InlineKeyboardMarkup(button_list)
    bot.send_message(chat_id=74175815, text='Выбери свои любимые бары!', reply_markup=reply_markup)

    global bar_counter
    bar_counter = 0

    next_bot(bot, update)

    
def next_bot(bot, update):

    global bar_counter

    if has_bot_stoped:
        return 

    next_bars_list = update.message.chat, '/next'
   
    bar_info_list = []
    for bar in bars[0 + bar_counter:4 + bar_counter]:
        bar_name = bar['Cells']['Name']
        bar_address = bar['Cells']['Address']
        bar_info = bar_name + ': ' + bar_address
        bar_info_list.append(bar_info)
    message = '\n'.join(bar_info_list)
    update.message.reply_text(message)

    bar_counter += 4


def stop_bot(bot, update):
    complited = 'Отлично! Бары записаны!'.format(update.message.chat, '/stop')
    update.message.reply_text(complited) 

    global has_bot_stoped
    has_bot_stoped = True


def main():
    mybot = Updater(bot_settings.TAKE_ME_BOT_APIKEY, request_kwargs=PROXY)
    mybot.dispatcher.add_handler(CommandHandler('start', start_bot))
    mybot.dispatcher.add_handler(CommandHandler('next', next_bot))
    mybot.dispatcher.add_handler(CommandHandler('stop', stop_bot))
    # mybot.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    mybot.start_polling()
    mybot.idle()    


if __name__ == '__main__':
    logging.info('Bot started')
    with open('bars.json', 'r') as file_reader:
        bars = json.load(file_reader)
    main()