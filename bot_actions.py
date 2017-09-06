#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
"""Methods for the CommandHandler"""
import random


class BotActions():
    """Makes actions with the bot"""
    @staticmethod
    def start(updater):
        """Initialize the bot"""
        updater.message.reply_text('Hola, mundo!')

    @staticmethod
    def hola(updater):
        """Reply with a cordial salute"""
        updater.message.reply_text('Hola, {}!'.format(updater.message.from_user.first_name))

    @staticmethod
    def macho(bot, updater):
        """Reply if you are altered"""
        chat_id = updater.message.chat.id
        bot.send_audio(chat_id=chat_id, audio=open('macho.mp3', 'rb'))

    @staticmethod
    def send_memes(bot, updater):
        """Reply with a random meme"""
        chat_id = updater.message.chat.id
        file_name = BotActions.random_meme_template("meme_list.txt")
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def random_meme_template(file_name):
        """Search a random meme in a list of memes"""
        num_lines = sum(1 for line in open(file_name, 'r'))
        random_file_pos = int(random.random()*num_lines)
        file_opened = open(file_name, 'r')
        linea = 0
        has_next = True
        while has_next and linea < random_file_pos:
            line = file_opened.readline()
            linea += 1
            if not line:
                has_next = False
        return file_opened.readline()

    @staticmethod
    def ping(bot, updater):
        """Reply with a pong."""
        bot.send_message(chat_id=updater.message.chat.id, "Pong!")
