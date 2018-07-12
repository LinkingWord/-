import logging
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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


def start_bot(bot, update):
    # print(update)
    first_greeting = 'Привет, {}!'.format(update.message.chat.first_name, '/start')

    update.message.reply_text(first_greeting)



def chat(bot, update):
    # if ''.format(update.message.text '/next'):
    #     update.message.reply_text(message)
    complited = 'Отлично! Бары записаны!'.format(update.message.chat, '/stop')
    update.message.reply_text(complited)

    user_text = update.message.text
    logging.info(user_text)
  
    bar_info_list = []
    for bar in bars[0 + bar_counter:4 + bar_counter]:
        bar_name = bar['Cells']['Name']
        bar_address = bar['Cells']['Address']
        bar_info = bar_name + ': ' + bar_address
        bar_info_list.append(bar_info)
    message = '\n'.join(bar_info_list)
    update.message.reply_text(message)

    global bar_counter
    bar_counter += 4
   


def main():
    mybot = Updater(bot_settings.TAKE_ME_BOT_APIKEY, request_kwargs=PROXY)
    mybot.dispatcher.add_handler(CommandHandler('start', start_bot))
    mybot.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    mybot.start_polling()
    mybot.idle()    


if __name__ == '__main__':
    logging.info('Bot started')
    with open('bars.json', 'r') as file_reader:
        bars = json.load(file_reader)
    main()