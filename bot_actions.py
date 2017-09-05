#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
"""Methods for the CommandHandler"""

class BotActions():
    """Makes actions with the bot"""
    def __init__(self, updater):
        pass

    @staticmethod
    def start(updater):
        """Initializes the bot"""
        updater.message.reply_text('Hola, mundo!')

    @staticmethod
    def hola(updater):
        """Replies with a cordial salute"""
        updater.message.reply_text('Hola, {}!'.format(updater.message.first_name))

    @staticmethod
    def macho(updater):
        """Replies if you are altered"""
        pass
