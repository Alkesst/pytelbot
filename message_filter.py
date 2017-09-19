from telegram.ext import BaseFilter


class CustomFilter(BaseFilter):
    def filter(self, message):
        return message.text == ':)'