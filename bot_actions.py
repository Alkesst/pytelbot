#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
# pylint: disable=C0111
# pylint: disable=C0412
# pylint: disable=C0301
"""Methods for the CommandHandler"""
import random
import os
from os import listdir
from time import gmtime
from os.path import isfile, join
from telegram_tweet import TweetFromTelegram
from special_actions import SpecialActions


class BotActions():
    """Makes actions with the bot"""
    @staticmethod
    def start(update):
        """Initialize the bot"""
        update.message.reply_text('Hola, mundo!')

    @staticmethod
    def hola(update):
        """Reply with a cordial salute"""
        update.message.reply_text('Hola, {}!'.format(update.message.from_user.first_name))

    @staticmethod
    def macho(bot, update):
        """Reply if you are altered"""
        chat_id = update.message.chat.id
        bot.send_audio(chat_id=chat_id, audio=open('/home/pi/Documentos/pytel_stuff/macho.mp3', 'rb'))

    @staticmethod
    def send_memes(bot, update):
        """Reply with a random meme"""
        chat_id = update.message.chat.id
        file_name = BotActions.random_file_name('/home/pi/Documentos/pytel_stuff/Memes')
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def random_file_name(path):
        """Search a random file inside a path"""
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f != '.DS_Store']
        lines = len(onlyfiles)
        random_file = int(round(random.random()*lines, 0))
        return path + "/" + onlyfiles[random_file]

    @staticmethod
    def ping(bot, update):
        """Reply with a pong."""
        bot.send_message(chat_id=update.message.chat.id, text="Pong!")

    @staticmethod
    def prueba(bot, update):
        bot.send_message(chat_id=update.message.chat.id, text=str(type(update.message.text)))

    @staticmethod
    def id_user(bot, update):
        if update.message.from_user.id == 67849121:
            chat_id = update.message.chat.id
            bot.send_message(chat_id=chat_id, text='ahora por gracioso no te doy la id a ti :)',
                             reply_to_message_id=update.message.message_id)
        else:
            chat_id = update.message.chat.id
            bot.send_message(chat_id=chat_id, text='`' + str(update.message.from_user.id) +
                             '`', reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def id_chat(bot, update):
        chat_id = update.message.chat.id
        bot.send_message(chat_id=chat_id, text='`' + str(chat_id) + '`',
                         reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def help(bot, update):
        help_text = BotActions.help_commands()
        bot.send_message(chat_id=update.message.from_user.id, text=help_text)

    @staticmethod
    def animals(bot, update):
        """Reply with a random animal image"""
        chat_id = update.message.chat.id
        file_name = BotActions.random_file_name('/home/pi/Documentos/pytel_stuff/Animals')
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def help_commands():
        help_text = "/start     Inicializa el bot\n"
        help_text += "/ping     Comprueba si el bot está encendido\n"
        help_text += "/hola     Te saluda cordialmente\n"
        help_text += "/macho    Te manda un audio para que te vayas a la mierda\n"
        help_text += "/nudes    Te manda un meme aleatorio de un repertorio de memes\n"
        help_text += "/animals  Te manda un animal aleatorio de un repertorio de aniamlitos\n"
        help_text += "/id       Manda el ID del usuario que ha ejecutado el comando\n"
        help_text += "/id_c     Manda el ID del chat en el que se ha ejecutado el comando\n"
        help_text += "/search   Manda un meme con el texto que le introduzcas\n"
        help_text += "/sad      Manda un meme de sad reacts only\n"
        help_text += "/tweet    @pytwe_bot manda un tweet con el texto tras el comando, ahora con soporte de utf-8\n"
        help_text += "/pole     Le da la pole a aquella persona que consiga mandar un mensaje a las M:S == 00:00"
        help_text += " Puede haber más de una persona con pole"
        return help_text

    @staticmethod
    def tweet(bot, update):
        list_id = BotActions.read_ids_from_file("ids.txt")
        if update.message.from_user.id in list_id:
            to_twitter = TweetFromTelegram()
            text_to_tweet = update.message.text[7:len(update.message.text)]
            text_to_tweet = text_to_tweet.encode('utf-8')
            link = to_twitter.new_tweet(text_to_tweet)
            if link == "error":
                bot.send_message(chat_id=update.message.chat.id,
                                 text="Intenta no poner carácteres especiales :)",
                                 reply_to_message_id=update.message.message_id)
            else:
                mensaje = "Ya he publicado tu tweet: " + link
                BotActions.tweet_to_log(link, update.message.from_user.first_name)
                bot.send_message(chat_id=update.message.chat.id, text=mensaje,
                                 reply_to_message_id=update.message.message_id)
        else:
            bot.send_message(chat_id=update.message.chat.id,
                             text="Creo que no se te permite enviar tweets... :s",
                             reply_to_message_id=update.message.message_id)

    @staticmethod
    def tweet_media(bot, update):
        # not finished method
        pass

    @staticmethod
    def tweet_to_log(link, user_name):
        opened_file = open("tweets.log", "a")
        hour = str(gmtime().tm_hour + 2)
        minute = str(gmtime().tm_min)
        secs = str(gmtime().tm_sec)
        month = str(gmtime().tm_mon)
        day = str(gmtime().tm_mday)
        year = str(gmtime().tm_year)
        log_string = hour + ":" + minute + ":" + secs + " at " + day + "/" + month + "/" + year + ": "
        log_string += user_name + ", " + link + "\n"
        opened_file.write(log_string)

    @staticmethod
    def read_ids_from_file(file_name):
        opened_file = open(file_name, 'r')
        ids = []
        has_next = True
        while has_next:
            line = opened_file.readline()
            if not line:
                has_next = False
            else:
                ids.append(int(line))
        return ids

    @staticmethod
    def search(bot, updater):
        # si en el grupo hay más de un bot hay que arreglar la mención de /search@PyTel_bot
        text = updater.message.text[8:len(updater.message.text)]
        text = text.encode('utf-8')
        SpecialActions.create_image_search("meme_template_search.png", text)
        bot.send_photo(chat_id=updater.message.chat.id,
                       photo=open("generated_meme_search.png", 'rb'),
                       reply_to_message_id=updater.message.message_id)
        os.remove("generated_meme_search.png")

    @staticmethod
    def sad_reactions(bot, updater):
        video = open("/home/pi/Documentos/pytel_stuff/sad_reactions_only.mp4", 'rb')
        bot.send_video(chat_id=updater.message.chat.id,
                       reply_to_message_id=updater.message.message_id,
                       video=video, caption="sad reacts only")

    @staticmethod
    def pole(bot, updater):
        if updater.message.date.strftime('%M:%S') == '00:00':
            bot.send_message(chat_id=updater.message.chat.id,
                             reply_to_message_id=updater.message.message_id,
                             text="Muy bien crack has hecho la pole")
        else:
            bot.send_message(chat_id=updater.message.chat.id,
                             reply_to_message_id=updater.message.message_id,
                             text="nice try pole, máquina")

    @staticmethod
    def happy(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="cállate ya macho",
                         reply_to_message_id=update.message.message_id)
