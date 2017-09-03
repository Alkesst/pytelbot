#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
from telegram.ext import Updater, CommandHandler

def main():
    def start(bot, update):
        update.message.reply_text('Hello World!')

    def hello(bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    updater = Updater('YOUR TOKEN HERE')

if __name__ == "__main__":
    main()