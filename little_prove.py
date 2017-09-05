#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
from telegram.ext import Updater, CommandHandler

def main():
    def start(bot, update):
        update.message.reply_text('¡Hola, mundo!')

    def hello(bot, update):
        update.message.reply_text(
            'Hola, {} !'.format(update.message.from_user.first_name))

    updater = Updater('YOUR TOKEN HERE')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hola', hello))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
