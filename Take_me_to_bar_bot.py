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

    # button_list = [
    #     [telegram.InlineKeyboardButton(bars[0]['Cells']['Name'], callback_data='Паб «ШемроК»')],
    #     [telegram.InlineKeyboardButton(bars[1]['Cells']['Name'], callback_data='Кафе Бар Бульвар')],
    #     [telegram.InlineKeyboardButton(bars[2]['Cells']['Name'], callback_data='НООКАН')],
    #     [telegram.InlineKeyboardButton(bars[3]['Cells']['Name'], callback_data='Чайхана')],
    #     [telegram.InlineKeyboardButton('Завершить', callback_data='/stop'), 
    #     telegram.InlineKeyboardButton('Продолжить', callback_data='/next')]
    #     ]

    # reply_markup = telegram.InlineKeyboardMarkup(button_list)
    # bot.send_message(chat_id=74175815, text='Выбери свои любимые бары!', reply_markup=reply_markup)

    global bar_counter
    bar_counter = 0

    next_bot(bot, update)

    # next_bot(bot, update)

    print(update)


# def buttons(bot, update):

#     button_list = [
#         [telegram.InlineKeyboardButton(bars[0]['Cells']['Name'], callback_data='Паб «ШемроК»')],
#         [telegram.InlineKeyboardButton(bars[1]['Cells']['Name'], callback_data='Кафе Бар Бульвар')],
#         [telegram.InlineKeyboardButton(bars[2]['Cells']['Name'], callback_data='НООКАН')],
#         [telegram.InlineKeyboardButton(bars[3]['Cells']['Name'], callback_data='Чайхана')],
#         [telegram.InlineKeyboardButton('Завершить', callback_data='/stop'), 
#         telegram.InlineKeyboardButton('Продолжить', callback_data='/next')]
#         ]

#     reply_markup = telegram.InlineKeyboardMarkup(button_list)
#     bot.send_message(chat_id=74175815, text='Выбери свои любимые бары!', reply_markup=reply_markup)

#     print(update)

        
def next_bot(bot, update):

    global bar_counter

    if has_bot_stoped:
        return 

    next_bars_list = update.message.chat, '/next'

    bar_info_list = []   
    # button_list = [
    #     [telegram.InlineKeyboardButton(bar_info_list)],
    #     [telegram.InlineKeyboardButton('Завершить', callback_data='/stop'), 
    #     telegram.InlineKeyboardButton('Продолжить', callback_data='/next')]
    #     ]
    for bar in bars[0 + bar_counter:4 + bar_counter]:
        bar_name = bar['Cells']['Name']
        bar_address = bar['Cells']['Address']
        bar_info = bar_name + ': ' + bar_address
        bar_button = [telegram.InlineKeyboardButton(bar_info, callback_data=bar_name)]
        bar_info_list.append(bar_button)
    bar_info_list.append(
        [
            telegram.InlineKeyboardButton('Завершить', callback_data='/stop'), 
            telegram.InlineKeyboardButton('Продолжить', callback_data='/next')
        ]
    )
    # message = [telegram.InlineKeyboardButton(bar_info_list)]
    reply = telegram.InlineKeyboardMarkup(bar_info_list)
    bot.send_message(chat_id=74175815, text='Выбери свои любимые бары!', reply_markup=reply)

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
    mybot.dispatcher.add_handler(MessageHandler(Filters.text, next_bot))
    mybot.dispatcher.add_handler(CallbackQueryHandler(next_bot))
    mybot.start_polling()
    mybot.idle()    


if __name__ == '__main__':
    logging.info('Bot started')
    with open('bars.json', 'r') as file_reader:
        bars = json.load(file_reader)
    main()