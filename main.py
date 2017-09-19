#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 2
# pylint: disable=C1001
from telegram.ext import Updater, CommandHandler, MessageHandler
from bot_actions import BotActions
from message_filter import HappyFilter, NotHappyFilter, BotijoReaction

def main():
    updater = Updater('TOKEN')
    happy_filter = HappyFilter()
    unhappy_filter = NotHappyFilter()
    botijo = BotijoReaction()
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
    updater.dispatcher.add_handler(CommandHandler('pole', BotActions.pole))
    updater.dispatcher.add_handler(CommandHandler('porro', BotActions.hora_porro))
    updater.dispatcher.add_handler(CommandHandler('pi', BotActions.horacio_pi))
    updater.dispatcher.add_handler(MessageHandler(happy_filter, BotActions.happy))
    updater.dispatcher.add_handler(MessageHandler(unhappy_filter, BotActions.not_happy))
    updater.dispatcher.add_handler(MessageHandler(botijo, BotActions.botijo_react))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
