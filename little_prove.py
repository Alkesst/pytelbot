#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
from telegram.ext import Updater, CommandHandler
from bot_actions import BotActions

def main():
    updater = Updater('YOUR TOKEN HERE')
    updater.dispatcher.add_handler(CommandHandler('start', BotActions.start))
    updater.dispatcher.add_handler(CommandHandler('hola', BotActions.hola))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
