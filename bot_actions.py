#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
"""Methods for the CommandHandler"""
import random
from os import listdir
from os.path import isfile, join


class BotActions():
    """Makes actions with the bot"""
    @staticmethod
    def start(bot, update):
        """Initialize the bot"""
        update.message.reply_text('Hola, mundo!')

    @staticmethod
    def hola(bot, update):
        """Reply with a cordial salute"""
        update.message.reply_text('Hola, {}!'.format(update.message.from_user.first_name))

    @staticmethod
    def macho(bot, update):
        """Reply if you are altered"""
        chat_id = update.message.chat.id
        bot.send_audio(chat_id=chat_id, audio=open('macho.mp3', 'rb'))

    @staticmethod
    def send_memes(bot, update):
        """Reply with a random meme"""
        chat_id = update.message.chat.id
        file_name = BotActions.random_meme_template()
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def random_meme_template():
        """Search a random meme in a list of memes"""
        onlyfiles = [f for f in listdir('/Users/alec/Desktop/Memes') if isfile(join('/Users/alec/Desktop/Memes', f)) and f != '.DS_Store']
        lines = len(onlyfiles)
        random_meme = int(round(random.random()*lines, 0))
        return '/Users/alec/Desktop/Memes/' + onlyfiles[random_meme]

    @staticmethod
    def ping(bot, update):
        """Reply with a pong."""
        bot.send_message(chat_id=update.message.chat.id, text="Pong!")

    @staticmethod
    def id(bot, update):
        chat_id = update.message.chat.id
        bot.send_message(chat_id=chat_id, text='`' + str(update.message.from_user.id) + '`', reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def show_error(bot, update, error):
        raise error

    @staticmethod
    def help(bot, update):
        pass
