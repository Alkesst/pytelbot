#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 2
# pylint: disable=C1001
# pylint: disable=C0111
# pylint: disable=C0412
# pylint: disable=C0301
# pylint: disable=R0904
"""Methods for the CommandHandler"""
import random
import os
from datetime import datetime
from os import listdir
from time import gmtime
from os.path import isfile, join
from telegram_tweet import TweetFromTelegram
# from special_actions import SpecialActions
from almacenamiento import Almacenamiento, User, UserGroup



class BotActions():
    """Makes actions with the bot"""
    dict_pole = {}
    dict_porro = {}
    dict_pi = {}
    data = None

    @staticmethod
    def start(bot, update):
        """Initialize the bot"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(text='Hola, mundo!', chat_id=chat_id)

    @staticmethod
    def hola(bot, update):
        """Reply with a cordial salute"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=chat_id, text='Hola, {}!'.format(update.message.from_user.first_name))

    @staticmethod
    def macho(bot, update):
        """Reply if you are altered"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_audio(chat_id=chat_id, audio=open('/home/pi/Documentos/pytel_stuff/macho.mp3', 'rb'))

    @staticmethod
    def send_memes(bot, update):
        # WORKING
        """Reply with a random meme"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_nudes(user_id, chat_id)
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
        # WORKING
        """Reply with a pong."""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        bot.send_message(chat_id=update.message.chat.id, text="Pong!")
        BotActions.incrementa_ping(user_id, chat_id)

    @staticmethod
    def id_user(bot, update):
        # WORKING
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=chat_id, text='`' + str(update.message.from_user.id) +
                         '`', reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def id_chat(bot, update):
        # WORKING
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=chat_id, text='`' + str(chat_id) + '`',
                         reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def help(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        help_text = BotActions.help_commands()
        bot.send_message(chat_id=user_id, text=help_text)

    @staticmethod
    def animals(bot, update):
        # WORKING
        """Reply with a random animal image"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_animales(user_id, chat_id)
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
        help_text += "/pole     Le da la pole a aquella persona que consiga mandar el primer mensaje del día\n"
        help_text += "/porro    Le da la hora porro al primero en usar el comando en la hora porro ;)\n"
        help_text += "/pi       Le da la horacio pi al primero en usar el comando en la horacio pi :O\n"
        help_text += "/set_tw_acc   Agrega a la base de datos un usuario de twitter con el formato @Twitter_User\n"
        help_text += "/info     Te manda toda la información acerca de tu cuenta\n"
        help_text += "/twitter_acc  Te manda por privado la cuenta que tienes puesta de twitter actualmente\n"
        help_text += "Además interactúa con: :), :(, botijos...\n"
        return help_text

    @staticmethod
    def tweet(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
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
    def search(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        # si en el grupo hay más de un bot hay que arreglar la mención de /search@PyTel_bot
        text = update.message.text[8:len(update.message.text)]
        text = text.encode('utf-8')
        SpecialActions.create_image_search("meme_template_search.png", text)
        bot.send_photo(chat_id=chat_id,
                       photo=open("generated_meme_search.png", 'rb'),
                       reply_to_message_id=update.message.message_id)
        os.remove("generated_meme_search.png")

    @staticmethod
    def sad_reacts(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        video = open("/home/pi/Documentos/pytel_stuff/sad_reactions_only.mp4", 'rb')
        bot.send_video(chat_id=chat_id,
                       reply_to_message_id=update.message.message_id,
                       video=video, caption="sad reacts only")

    @staticmethod
    def pole(bot, update):
        current_time = update.message.date
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        if chat_id != user_id:
            if current_time.hour == 0 and (current_time.minute >= 0 and current_time.minute < 15):
                if update.message.chat.id not in BotActions.dict_pole:
                    BotActions.dict_pole[update.message.chat.id] = update.message.from_user.id
                    BotActions.incrementa_pole(user_id, chat_id)
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="Muy bien crack has hecho la pole")
                    to_twitter = TweetFromTelegram()
                    text_to_tweet = "¡La pole se la ha llevado "
                    text_to_tweet += BotActions.get_twitter_acc(update.message.fro_user.id)
                    text_to_tweet += " desde el grupo "
                    text_to_tweet += update.message.chat.title + "!"
                    text_to_tweet = text_to_tweet.encode('utf-8')
                    to_twitter.new_tweet(text_to_tweet)
                    # THREAD
                else:
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="nice try pole, máquina")
            else:
                bot.send_message(chat_id=update.message.chat.id,
                                 reply_to_message_id=update.message.message_id,
                                 text="No estás en horario de pole... :S")
        else:
            bot.send_message(chat_id=user_id, text="Esta macro solo funciona en grupos")

    @staticmethod
    def happy(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=update.message.chat.id,
                         text="cállate ya macho",
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def not_happy(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=update.message.chat.id,
                         text="alegra esa cara de comepollas que tienes",
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def botijo_react(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        bot.send_message(chat_id=update.message.chat.id,
                         text="like! ;)",
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def hora_porro(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        current_time = update.message.date
        if chat_id != user_id:
            if current_time.hour == 4 and current_time.minute == 20:
                if update.message.chat.id not in BotActions.dict_porro:
                    BotActions.dict_porro[update.message.chat.id] = update.message.from_user.id
                    BotActions.incrementa_porro(user_id, chat_id)
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="Vaya fiera, te has llevado la hora porro bro")
                    to_twitter = TweetFromTelegram()
                    text_to_tweet = "¡La hora porro se la lleva "
                    text_to_tweet += BotActions.get_twitter_acc(update.message.from_user.id)
                    text_to_tweet += " desde el grupo "
                    text_to_tweet += update.message.chat.title + "!"
                    text_to_tweet = text_to_tweet.encode('utf-8')
                    to_twitter.new_tweet(text_to_tweet)
                else:
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="Ya se han llevado la hora porro ;)")
            else:
                bot.send_message(chat_id=update.message.chat.id,
                                 reply_to_message_id=update.message.message_id,
                                 text="No estás en el horario necesario... >_<")
        else:
            bot.send_message(chat_id=user_id, text="Esta macro solo funciona en grupos")

    @staticmethod
    def horacio_pi(bot, update):
        current_time = update.message.date
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        if chat_id != user_id:
            if current_time.hour == 3 and current_time.minute == 14:
                if update.message.chat.id not in BotActions.dict_pi:
                    BotActions.dict_pi[update.message.chat.id] = update.message.from_user.id
                    BotActions.incrementa_pi(user_id, chat_id)
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="Te acabas de llevar la horacio pi :O")
                    to_twitter = TweetFromTelegram()
                    text_to_tweet = "¡La hora pi se la lleva "
                    text_to_tweet += BotActions.get_twitter_acc(update.message.from_user.id)
                    text_to_tweet += " desde el grupo "
                    text_to_tweet += update.message.chat.title + "!"
                    text_to_tweet = text_to_tweet.encode('utf-8')
                    to_twitter.new_tweet(text_to_tweet)
                else:
                    bot.send_message(chat_id=update.message.chat.id,
                                     reply_to_message_id=update.message.message_id,
                                     text="Fuiste demasiado lento para la horacio pi :/")
            else:
                bot.send_message(chat_id=update.message.chat.id,
                                 reply_to_message_id=update.message.message_id,
                                 text="Fuck you fam, this is not the pi hour :@")
        else:
            bot.send_message(chat_id=user_id, text="Esta macro solo funciona en grupos")

    @staticmethod
    def comunism(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        video = open("/home/pi/Documentos/pytel_stuff/comunist_meme.mp4", 'rb')
        bot.send_video(chat_id=chat_id,
                       reply_to_message_id=update.message.message_id,
                       video=video, caption="communism will prevail")

    @staticmethod
    def add_user(user_id, chat_id):
        # WORKING
        """Add a new user into the Data Base. It also creates the communication between this class and the Data Base"""
        if BotActions.data is None:
            BotActions.data = Almacenamiento("/home/alkesst/Documentos/data.db")
        user = User(user_id)
        if BotActions.data.obtener_usuario(user) is None:
            BotActions.data.insertar_usuario(user)
        if chat_id != user_id:
            user = UserGroup(user_id, chat_id)
            if BotActions.data.obtener_usuario_del_grupo(user) is None:
                BotActions.data.insertar_usuario_del_grupo(user)
        current_time = datetime.now()
        if not BotActions.dict_pole and ((current_time.hour == 0 and current_time.minute >= 15) or current_time.hour > 0):
            BotActions.dict_pole = {}
        if not BotActions.dict_pi and ((current_time.hour == 3 and current_time.minute >= 14) or current_time.hour > 3):
            BotActions.dict_pi = {}
        if not BotActions.dict_porro and ((current_time.hour == 4 and current_time.minute >= 20) or current_time.hour > 4):
            BotActions.dict_porro = {}

    @staticmethod
    def mensajes_callback(bot, update):
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    def incrementa_mensajes(user_id, chat_id):
        # WORKING
        BotActions.add_user(user_id, chat_id)
        if chat_id != user_id:
            user = UserGroup(user_id, chat_id)
            BotActions.data.aumentar_message_number(user)

    @staticmethod
    def incrementa_nudes(user_id, chat_id):
        user = User(user_id)
        BotActions.data.aumentar_nude_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    def incrementa_ping(user_id, chat_id):
        # Work
        user = User(user_id)
        BotActions.data.aumentar_ping_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    def incrementa_porro(user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        BotActions.data.aumentar_porro_number(user)

    @staticmethod
    def incrementa_pole(user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        BotActions.data.aumentar_pole_number(user)

    @staticmethod
    def incrementa_pi(user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        BotActions.data.aumentar_pi_number(user)

    @staticmethod
    def incrementa_animales(user_id, chat_id):
        user = User(user_id)
        BotActions.data.aumentar_animal_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    def add_twitter_account(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        twitter_acc = update.message.text[12:len(update.message.text)]
        if not twitter_acc:
            text = 'No es un formato válido para una cuenta de twitter :('
        elif twitter_acc[0] != '@':
            text = 'No es un formato válido para una cuenta de twitter :('
        else:
            user = BotActions.get_user(user_id)
            user.twitter_user = twitter_acc
            BotActions.data.modificar_usuario(user)
            text = 'se ha añadido la cuenta de twitter ' + twitter_acc
        bot.send_message(chat_id=update.message.chat.id,
                         text=text)

    @staticmethod
    def get_twitter_acc(user_id):
        """Return the twitter account from de Data Base"""
        user = BotActions.get_user(user_id)
        return user.twitter_user

    @staticmethod
    def get_user_group(user_id, chat_id):
        # WORK
        """Return the User Group from the Data Base"""
        user = UserGroup(user_id, chat_id)
        user = BotActions.data.obtener_usuario_del_grupo(user)
        return user

    @staticmethod
    def get_user(user_id):
        # WORK
        """Return the user from the Data Base"""
        user = User(user_id)
        user = BotActions.data.obtener_usuario(user)
        return user

    @staticmethod
    def get_messages(user_id, chat_id):
        # WORK
        """Return a text with all the number of messages that sent that user"""
        user = BotActions.get_user_group(user_id, chat_id)
        mensajes = user.message_number
        message_text = "Has enviado " + str(mensajes) + " mensajes!"
        return message_text

    @staticmethod
    def get_pole(user_id, chat_id):
        # WORK
        """Return a text with all the number of poles that made that user"""
        user = BotActions.get_user_group(user_id, chat_id)
        poles = user.pole_number
        pole_text = "Has hecho " + str(poles) + " poles!"
        return pole_text

    @staticmethod
    def get_porro(user_id, chat_id):
        # WORK
        """Return a text with all the number of porros that made that user"""
        user = BotActions.get_user_group(user_id, chat_id)
        porros = user.porro_number
        porro_text = "Has hecho " + str(porros) + " horas porro!"
        return porro_text

    @staticmethod
    def get_pi(user_id, chat_id):
        # WORK
        """Return a text with all the number of pis that made that user"""
        user = BotActions.get_user_group(user_id, chat_id)
        pi_number = user.pi_number
        pi_text = "Has hecho " + str(pi_number) + " horas pi!"
        return pi_text

    # Añadir metodos para conseguir las estadísticas de /nudes, /ping etc

    @staticmethod
    def info_user_group(bot, update):
        # WORK
        """Send a message with all the info from the user group"""
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        BotActions.add_user(chat_id, user_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        user_name = update.message.from_user.first_name + "\n"
        info_text_group = BotActions.info_text(user_id, chat_id)
        info_text_personal = BotActions.info_text_personal(user_id)
        message_text = "Estas son las estadísticas grupales de " + user_name + info_text_group
        message_text += "Estas son las estadísticas personales de " + user_name + info_text_personal
        bot.send_message(chat_id=chat_id, text=message_text)

    @staticmethod
    def info_text(user_id, chat_id):
        info_text_group = BotActions.get_messages(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_pole(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_porro(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_pi(user_id, chat_id) + "\n"
        return info_text_group

    @staticmethod
    def info_text_personal(user_id):
        info_text_personal = BotActions.get_nudes(user_id) + "\n"
        info_text_personal += BotActions.get_pings(user_id) + "\n"
        info_text_personal += BotActions.get_animals(user_id) + "\n"
        return info_text_personal

    @staticmethod
    def get_nudes(user_id):
        user = BotActions.get_user(user_id)
        nude_number = user.nude_number
        nudes_text = "Has usado " + str(nude_number) + " el comando /nudes!"
        return nudes_text

    @staticmethod
    def get_pings(user_id):
        user = BotActions.get_user(user_id)
        ping_number = user.ping_number
        ping_text = "Has usado " + str(ping_number) + " el comando /ping!"
        return ping_text

    @staticmethod
    def get_animals(user_id):
        user = BotActions.get_user(user_id)
        animal_number = user.animal_number
        animal_text = "Has usado " + str(animal_number) + " el comando /animals!"
        return animal_text

    @staticmethod
    def send_twitter_acc(bot, update):
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)
        user = BotActions.get_user(user_id)
        twitter_account = user.twitter_user
        bot.send_message(chat_id=user_id, text="Esta es la cuenta que tienes puesta actualmente: " + twitter_account)
