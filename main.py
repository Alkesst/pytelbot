#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
from telegram.ext import Updater, CommandHandler
from bot_actions import BotActions


def main():
    updater = Updater('TOKEN')
    updater.dispatcher.add_handler(CommandHandler('start', BotActions.start))
    updater.dispatcher.add_handler(CommandHandler('hola', BotActions.hola))
    updater.dispatcher.add_handler(CommandHandler('macho', BotActions.macho))
    updater.dispatcher.add_handler(CommandHandler('nudes', BotActions.send_memes))
    updater.dispatcher.add_handler(CommandHandler('ping', BotActions.ping))
    updater.dispatcher.add_handler(CommandHandler('id', BotActions.id_user))
    updater.dispatcher.add_handler(CommandHandler('id_c', BotActions.id_chat))
    updater.dispatcher.add_handler(CommandHandler('help', BotActions.help))
    updater.dispatcher.add_handler(CommandHandler('animals', BotActions.animals))
    updater.dispatcher.add_handler(CommandHandler('tweet', BotActions.tweet))
    updater.dispatcher.add_handler(CommandHandler('sad', BotActions.sad_reactions))
    updater.dispatcher.add_handler(CommandHandler('search', BotActions.search))
    updater.dispatcher.add_handler(CommandHandler('prueba', BotActions.prueba))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
