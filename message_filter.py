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
        return 'botijo' in message.text.lower()


class CuandoTePasaReact(BaseFilter):
    def filter(self, message):
        return 'cuando te pasa' in message.text.lower()


class EasyReact(BaseFilter):
    def filter(self, message):
        return 'easy' in message.text.lower()


class Insulto(BaseFilter):
    def filter(self, message):
        return message.text[0:9].lower() == u'insulta a'


class Thicc(BaseFilter):
    def filter(self, message):
        return 'thicc' in message.text


class AVeces(BaseFilter):
    def filter(self, message):
        return 'a veces' in message.text or "habeces" in message.text


class Gracias(BaseFilter):
    def filter(self, message):
        return message.text == 'gracias @pytel_bot' or message.text == '@pytel_bot gracias'