#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
import re
from telegram.ext import BaseFilter


class HappyFilter(BaseFilter):
    def filter(self, message):
        return message.text == ':)' or message.text == ':-)'


class NotHappyFilter(BaseFilter):
    def filter(self, message):
        return message.text == ':(' or message.text == ':-('


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
        return message.text[0:9].lower() == 'insulta a'


class Thicc(BaseFilter):
    def filter(self, message):
        text = message.text.lower()
        return 'thicc' in text or 't h i c c' in text


class AVeces(BaseFilter):
    def filter(self, message):
        return 'a veces' in message.text or "habeces" in message.text


class Gracias(BaseFilter):
    def filter(self, message):
        text = message.text.lower()
        return 'gracias ' in message.text.lower() or \
               message.text.endswith('gracias') or \
               message.text.endswith('gracias.')

class SadReacts(BaseFilter):
    def filter(self, message):
        return " sad " in message.text.lower() or \
                message.text.lower() == 'sad' or \
                'sad ' in message.text.lower() or \
                ' sad' in message.text.lower()


class BuenosDias(BaseFilter):
    def filter(self, message):
        text = message.text.lower()
        return "buenos dias españa" in text or \
               "buenos días españa" in text or \
               "buenos días, españa" in text or \
               "buenos dias, españa" in text


class RevertedReact(BaseFilter):
    def filter(self, message):
        text = message.text.lower()
        return 'reverted' in text or \
            'arturo perez reverted' in text or \
            'perez reverted' in text


class ReverteReact(BaseFilter):
    def filter(self, message):
        text = message.text.lower()
        return 'arturo pérez-reverte' in text or \
            'arturo perez-reverte' in text or \
            'arturo parez reverte' in text or \
            'perez reverte' in text or \
            'pérez-reverte' in text or \
            'perez-reverte' in text or \
            'reverte' in text


class Xdd(BaseFilter):
    def filter(self, message):
        return 'xd' in message.text


class BumperCars(BaseFilter):
    def filter(self, message):
        return 'coches de choque' in message.text.lower() or \
               'coches chocones' in message.text.lower()
