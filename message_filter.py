#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 2
# pylint: disable=C1001
from telegram.ext import BaseFilter


class HappyFilter(BaseFilter):
    def filter(self, message):
        return message.text == ':)'

class NotHappyFilter(BaseFilter):
    def filter(self, message):
        return message.text == ':('

class BotijoReaction(BaseFilter):
    def filter(self, message):
        return 'botijo' in message.text

class CuandoTePasaReact(BaseFilter):
    def filter(self, message):
        return 'cuando te pasa' in message.text

class EasyReact(BaseFilter):
    def filter(self, message):
        return 'easy' in message.text

class InsultoReact(BaseFilter):
    def filter(self, message):
        return message.text[0:10] == 'insulta a'
