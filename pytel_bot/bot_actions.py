#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
# pylint: disable=C0111
# pylint: disable=C0412
# pylint: disable=C0301
# pylint: disable=R0904
"""Methods for the CommandHandler"""
import subprocess
import random
import os
import logging
from math import ceil
from pathlib import Path
from os import listdir
from time import gmtime
from os.path import isfile, join
from threading import Timer
from pytel_bot.telegram_tweet import TweetFromTelegram
from pytel_bot.special_actions import SpecialActions
from pytel_bot.almacenamiento import Almacenamiento, User, UserGroup, Group, UselessData
from pytel_bot.lastfm_connection import LastFM


def with_db(func):
    def wrapped(*args, **kwargs):
        db = BotActions.get_data_base()
        ret_val = func(db, *args, **kwargs)
        db.close()
        return ret_val

    return wrapped


class BotActions(object):
    """Makes actions with the bot"""
    dict_tcp_connections = {}
    dict_pole = {}
    dict_porro = {}
    dict_pi = {}
    stickers = ['CAADBAADJQADuE-EEuya2udZTudYAg', 'CAADBAADLAADuE - EElvaPQABlkaHMAI', 'CAADBAADQAADuE-EEs7AEGXnB5sOAg']
    logging.basicConfig(format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', filename="botActions.log",
                        level=logging.WARNING)
    logging.getLogger().addHandler(logging.StreamHandler())
    ids = None
    pytel_path = os.environ.get("PYTEL_PATH", "../pytel_stuff")
    py_last = LastFM()

    # CAADBAADJQADuE-EEuya2udZTudYAg reverted
    # CAADBAADLAADuE - EElvaPQABlkaHMAI
    # CAADBAADQAADuE-EEs7AEGXnB5sOAg

    @staticmethod
    def get_data_base():
        return Almacenamiento(f"{BotActions.pytel_path}/data.db")

    @staticmethod
    def get_disturb_status_from_db():
        #  TODO GET FROM ALL GROUPS THE DISTURB STATUS!
        pass

    @staticmethod
    def syn(bot, update):
        """Initialize the bot"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        text = ''
        if BotActions.dict_tcp_connections.get(chat_id) is not None:
            if BotActions.dict_tcp_connections[chat_id]:
                text = 'TCP connection already stablished!'
        else:
            text = 'SYN=1;ACK=1;'
            BotActions.dict_tcp_connections[chat_id] = True
        bot.send_message(text=text, chat_id=chat_id)

    @staticmethod
    def ack(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if BotActions.dict_tcp_connections.get(chat_id) is not None:
            if BotActions.dict_tcp_connections[chat_id]:
                text = 'TCP connection finished'
                BotActions.dict_tcp_connections[chat_id] = False
            else:
                text = 'TCP connection stablished'
                BotActions.dict_tcp_connections[chat_id] = True
        else:
            text = 'TCP connection stablished'
            BotActions.dict_tcp_connections[chat_id] = True
        bot.send_message(text=text, chat_id=chat_id)

    @staticmethod
    def fin(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if BotActions.dict_tcp_connections.get(chat_id) is not None:
            text = 'FIN=1;ACK=1;'
            BotActions.dict_tcp_connections[chat_id] = False
        else:
            text = 'You cannot end a connection that was never stablished!'
        bot.send_message(text=text, chat_id=chat_id)

    @staticmethod
    def hola(bot, update):
        """Reply with a cordial salute"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='Hola, {}!'.format(update.message.from_user.first_name))

    @staticmethod
    def common_process(chat_id, user_id):
        if chat_id != user_id:
            BotActions.add_chat_group(chat_id)
        BotActions.add_user(user_id, chat_id)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    def macho(bot, update):
        """Reply if you are altered"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_voice(chat_id=chat_id, voice=open(f'{BotActions.pytel_path}/macho.mp3', 'rb'))

    @staticmethod
    def send_memes(bot, update):
        # WORKING
        """Reply with a random meme"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        BotActions.incrementa_nudes(user_id, chat_id)
        file_name = BotActions.random_file_name(f'{BotActions.pytel_path}/Memes')
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def random_file_name(path):
        """Search a random file inside a path"""
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f != '.DS_Store']
        lines = len(onlyfiles)
        random_file = int(round(random.random() * lines, 0))
        return path + "/" + onlyfiles[random_file]

    @staticmethod
    def ping(bot, update):
        # WORKING
        """Reply with a pong."""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=update.message.chat.id, text="Pong!")
        BotActions.incrementa_ping(user_id, chat_id)

    @staticmethod
    def id_user(bot, update):
        # WORKING
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='`' + str(update.message.from_user.id) + '`',
                         reply_to_message_id=update.message.message_id, parse_mode='Markdown')

    @staticmethod
    def id_chat(bot, update):
        # WORKING
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='`' + str(chat_id) + '`', reply_to_message_id=update.message.message_id,
                         parse_mode='Markdown')

    @staticmethod
    def help(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        help_text = BotActions.help_commands()
        if chat_id != user_id:
            bot.send_message(chat_id=chat_id, text="Te he mandado la ayuda por privado :p",
                             reply_to_message_id=update.message.message_id)
        bot.send_message(chat_id=user_id, text=help_text)

    @staticmethod
    def animals(bot, update):
        # WORKING
        """Reply with a random animal image"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        BotActions.incrementa_animales(user_id, chat_id)
        file_name = BotActions.random_file_name(f'{BotActions.pytel_path}/Animals')
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'))

    @staticmethod
    def help_commands():
        help_text = "/start     Inicializa el bot\n"
        help_text += "/ping     Comprueba si el bot está encendido\n"
        help_text += "/dnd      Desactiva las intervenciones del bot en un grupo determinado\n"
        help_text += "/disturb  Reactiva las intervenciones del bot en un grupo determinado\n"
        help_text += "/hola     Te saluda cordialmente\n"
        help_text += "/macho    Te manda un audio para que te vayas a la mierda\n"
        help_text += "/nudes    Te manda un meme aleatorio de un repertorio de memes\n"
        help_text += "/animals  Te manda un animal aleatorio de un repertorio de animalitos\n"
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
        help_text += "/comunist     Te manda el mejor meme comunista actual\n"
        help_text += "/current_status [unidad]     Te manda la información actual de la raspberry pi,"
        help_text += "/current_status MB, lo manda en megaBytes, /current_status B lo manda en bytes.\n"
        help_text += "/thicc     Te manda un thicc human\n"
        help_text += "/cocaine   Manda un video sobre porqué no deberías tomar cocaína\n"
        help_text += "/barman    Le pides un Dyc al barman\n"
        help_text += "/gustar    Buen copy paste twittero\n"
        help_text += "/dato      Te manda datos curiosos para ampliar tu cultura general\n"
        help_text += "/insults   Te insulta en un lenguaje arcaico\n"
        help_text += "/vallecas  Te dice si duele hacerse un tatuaje en la zona de vallecas\n"
        help_text += "Además interactúa con: :), :(, botijos, xd, sad, etc...\n"
        return help_text

    @staticmethod
    def tweet(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        list_id = BotActions.read_ids_from_file("ids.txt")
        if update.message.from_user.id in list_id:
            to_twitter = TweetFromTelegram()
            text_to_tweet = update.message.text[7:]
            text_to_tweet = text_to_tweet
            link = to_twitter.new_tweet(text_to_tweet)
            mensaje = "Ya he publicado tu tweet: " + link
            BotActions.tweet_to_log(link, update.message.from_user.first_name)
            bot.send_message(chat_id=update.message.chat.id, text=mensaje,
                             reply_to_message_id=update.message.message_id)
        else:
            bot.send_message(chat_id=update.message.chat.id, text="Creo que no se te permite enviar tweets... :s",
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
        if Path(file_name).exists():
            opened_file = open(file_name, 'rb')
            ids = []
            has_next = True
            while has_next:
                line = opened_file.readline()
                if not line:
                    has_next = False
                else:
                    ids.append(int(line))
        else:
            ids = [int(strs) for strs in os.environ.get('PYTEL_ADMIN_IDS', '').split(',')]
        return ids

    @staticmethod
    def search(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        # si en el grupo hay más de un bot hay que arreglar la mención de /search@PyTel_bot
        text = update.message.text[8:]
        SpecialActions.create_image_search(f"{BotActions.pytel_path}/meme_template_search.png",
                                           f"{BotActions.pytel_path}/generated_meme_search.png", text)
        bot.send_photo(chat_id=chat_id, photo=open(f"{BotActions.pytel_path}/generated_meme_search.png", 'rb'),
                       reply_to_message_id=update.message.message_id)
        os.remove(f"{BotActions.pytel_path}/generated_meme_search.png")

    @staticmethod
    def sad_reacts(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        video = open(f"{BotActions.pytel_path}/sad_reactions_only.mp4", 'rb')
        bot.send_video(chat_id=chat_id, reply_to_message_id=update.message.message_id, video=video,
                       caption="sad reacts only")

    @staticmethod
    def pole(bot, update):
        # Working
        current_time = update.message.date
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if chat_id != user_id:
            if current_time.hour == 0 and (0 <= current_time.minute < 15):
                if update.message.chat.id not in BotActions.dict_pole:
                    if not BotActions.dict_pole:
                        # Cuando pasen las 00:15:10, se borrará el diccionario
                        remaining_time = (15 - current_time.minute) * 60 + 60 - current_time.second + 10
                        Timer(remaining_time, BotActions.delete_pole).start()
                    BotActions.dict_pole[chat_id] = user_id
                    BotActions.incrementa_pole(user_id, chat_id)
                    pole_text = "Muy bien crack has hecho la pole"
                    twitter_acc = BotActions.get_twitter_acc(user_id)
                    if twitter_acc:
                        to_twitter = TweetFromTelegram()
                        text_to_tweet = "¡La pole se la ha llevado "
                        text_to_tweet += twitter_acc
                        text_to_tweet += " desde el grupo "
                        text_to_tweet += update.message.chat.title + "!"
                        text_to_tweet = text_to_tweet
                        to_twitter.new_tweet(text_to_tweet)
                    else:
                        pole_text += "\nDesafortunadamente no tienes cuenta de twitter así que no se publicará" \
                                     "en twitter :( /sad"
                else:
                    pole_text = "nice try, máquina"
            else:
                pole_text = "No estás en horario de pole... :S"
        else:
            pole_text = "Esta macro solo funciona en grupos"
        bot.send_message(chat_id=chat_id, reply_to_message_id=update.message.message_id, text=pole_text)

    @staticmethod
    def delete_pole():
        BotActions.dict_pole = {}
        logging.info("El diccionario de poles se ha reiniciado")

    @staticmethod
    def delete_pi():
        BotActions.dict_pi = {}
        logging.info("El diccionario de poles se ha reiniciado")

    @staticmethod
    def delete_porro():
        BotActions.dict_porro = {}
        logging.info("El diccionario de poles se ha reiniciado")

    @staticmethod
    def happy(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=update.message.chat.id, text="cállate ya macho",
                             reply_to_message_id=update.message.message_id)

    @staticmethod
    def not_happy(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=update.message.chat.id, text="alegra esa cara de comepollas que tienes",
                             reply_to_message_id=update.message.message_id)

    @staticmethod
    def botijo_react(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=update.message.chat.id, text="like! ;)",
                             reply_to_message_id=update.message.message_id)

    @staticmethod
    def hora_porro(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        current_time = update.message.date
        if chat_id != user_id:
            # https://en.wikipedia.org/wiki/420_(cannabis_culture)
            if current_time.hour == 16 and current_time.minute == 20:
                if update.message.chat.id not in BotActions.dict_porro:
                    if not BotActions.dict_porro:
                        # Cuando pasen las 04:21:10 se borrará el diccionario
                        remaining_time = 60 - current_time.second + 10
                        Timer(remaining_time, BotActions.delete_porro).start()
                    BotActions.dict_porro[chat_id] = user_id
                    BotActions.incrementa_porro(user_id, chat_id)
                    porro_text = "Vaya fiera, te has llevado la hora porro bro"
                    twitter_acc = BotActions.get_twitter_acc(user_id)
                    if twitter_acc:
                        to_twitter = TweetFromTelegram()
                        text_to_tweet = "¡La hora porro se la lleva "
                        text_to_tweet += twitter_acc
                        text_to_tweet += " desde el grupo "
                        text_to_tweet += update.message.chat.title + "!"
                        text_to_tweet = text_to_tweet
                        to_twitter.new_tweet(text_to_tweet)
                    else:
                        porro_text += "\nDesafortunadamente no tienes cuenta de twitter así que no se publicará" \
                                      "en twitter :( /sad"
                else:
                    porro_text = "Ya se han llevado la hora porro ;)"
            else:
                porro_text = "No estás en el horario necesario... >_<"
        else:
            porro_text = "Esta macro solo funciona en grupos"
        bot.send_message(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, text=porro_text)

    @staticmethod
    def horacio_pi(bot, update):
        current_time = update.message.date
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if chat_id != user_id:
            if current_time.hour == 3 and current_time.minute == 14:
                if update.message.chat.id not in BotActions.dict_pi:
                    if not BotActions.dict_pi:
                        # Cuando pasen las 03:15:10 se borrará el diccionario
                        remaining_time = 60 - current_time.second + 10
                        Timer(remaining_time, BotActions.delete_pi).start()
                    BotActions.dict_pi[chat_id] = user_id
                    BotActions.incrementa_pi(user_id, chat_id)
                    twitter_acc = BotActions.get_twitter_acc(user_id)
                    pi_text = "Te acabas de llevar la horacio pi :O"
                    if twitter_acc:
                        to_twitter = TweetFromTelegram()
                        text_to_tweet = "¡La hora pi se la lleva "
                        text_to_tweet += twitter_acc
                        text_to_tweet += " desde el grupo "
                        text_to_tweet += update.message.chat.title + "!"
                        text_to_tweet = text_to_tweet
                        to_twitter.new_tweet(text_to_tweet)
                    else:
                        pi_text += "\nDesafortunadamente no tienes cuenta de twitter así que no se publicará" \
                                   "en twitter :( /sad"
                else:
                    pi_text = "Fuiste demasiado lento para la horacio pi :/"
            else:
                pi_text = "Que te jodan, no estás en horario pi"
        else:
            pi_text = "Esa macro solo funciona en grupos :("
        bot.send_message(chat_id=update.message.chat.id, reply_to_message_id=update.message.message_id, text=pi_text)

    @staticmethod
    def comunist_meme(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        video = open(f"{BotActions.pytel_path}/comunist_meme.mp4", 'rb')
        bot.send_video(chat_id=chat_id, reply_to_message_id=update.message.message_id, video=video,
                       caption="communism will prevail!")

    @staticmethod
    @with_db
    def add_user(data, user_id, chat_id):
        # WORKING
        """Add a new user into the Data Base. It also creates the communication between this class and the Data Base"""
        user = User(user_id)
        if data.obtener_usuario(user) is None:
            data.insertar_usuario(user)
        if chat_id != user_id:
            user = UserGroup(user_id, chat_id)
            if data.obtener_usuario_del_grupo(user) is None:
                data.insertar_usuario_del_grupo(user)

    @staticmethod
    def mensajes_callback(_, update):
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        BotActions.common_process(chat_id, user_id)

    @staticmethod
    @with_db
    def incrementa_mensajes(data, user_id, chat_id):
        if chat_id != user_id:
            user = UserGroup(user_id, chat_id)
            data.aumentar_message_number(user)

    @staticmethod
    @with_db
    def incrementa_nudes(data, user_id, chat_id):
        user = User(user_id)
        data.aumentar_nude_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    @with_db
    def incrementa_ping(data, user_id, chat_id):
        # Work
        user = User(user_id)
        data.aumentar_ping_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    @with_db
    def incrementa_porro(data, user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        data.aumentar_porro_number(user)

    @staticmethod
    @with_db
    def incrementa_pole(data, user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        data.aumentar_pole_number(user)

    @staticmethod
    @with_db
    def incrementa_pi(data, user_id, chat_id):
        user = UserGroup(user_id, chat_id)
        data.aumentar_pi_number(user)

    @staticmethod
    @with_db
    def incrementa_animales(data, user_id, chat_id):
        user = User(user_id)
        data.aumentar_animal_number(user)
        BotActions.incrementa_mensajes(user_id, chat_id)

    @staticmethod
    @with_db
    def add_twitter_account(data, bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if chat_id != user_id:
            text = "Este comando solo se puede usar en un chat privado"
        else:
            twitter_acc = update.message.text[12:]
            if not twitter_acc:
                text = u'No es un formato válido para una cuenta de twitter :('
            elif twitter_acc[0] != '@':
                text = u'No es un formato válido para una cuenta de twitter :('
            else:
                user = BotActions.get_user(user_id)
                user.twitter_user = twitter_acc
                data.modificar_usuario(user)
                text = u'Se ha añadido la cuenta de twitter ' + twitter_acc
        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def get_twitter_acc(user_id):
        """Return the twitter account from de Data Base"""
        user = BotActions.get_user(user_id)
        return user.twitter_user

    @staticmethod
    @with_db
    def get_user_group(data, user_id, chat_id):
        # WORK
        """Return the User Group from the Data Base"""
        user = UserGroup(user_id, chat_id)
        user = data.obtener_usuario_del_grupo(user)
        return user

    @staticmethod
    @with_db
    def get_user(data, user_id):
        # WORK
        """Return the user from the Data Base"""
        user = User(user_id)
        user = data.obtener_usuario(user)
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

    @staticmethod
    def info_user_group(bot, update):
        # WORKING
        """Send a message with all the info from the user group"""
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        if chat_id != user_id:
            BotActions.common_process(chat_id, user_id)
            user_name = update.message.from_user.first_name + "\n"
            info_text_group = BotActions.info_text(user_id, chat_id)
            info_text_personal = BotActions.info_text_personal(user_id)
            message_text = "Estas son las estadísticas grupales de " + user_name + info_text_group
            message_text += "Estas son las estadísticas personales de " + user_name + info_text_personal
            message_text = message_text
        else:
            message_text = "Este comando solo se puede usar en un grupo :("
        bot.send_message(chat_id=chat_id, text=message_text)

    @staticmethod
    def info_text(user_id, chat_id):
        # WORKING
        info_text_group = BotActions.get_messages(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_pole(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_porro(user_id, chat_id) + "\n"
        info_text_group += BotActions.get_pi(user_id, chat_id) + "\n"
        return info_text_group

    @staticmethod
    def info_text_personal(user_id):
        # WORKING
        info_text_personal = BotActions.get_nudes(user_id) + "\n"
        info_text_personal += BotActions.get_pings(user_id) + "\n"
        info_text_personal += BotActions.get_animals(user_id) + "\n"
        info_text_personal += BotActions.get_all_messages(user_id) + "\n"
        return info_text_personal

    @staticmethod
    def get_nudes(user_id):
        # WORKING
        user = BotActions.get_user(user_id)
        nude_number = user.nude_number
        nudes_text = "Has usado " + str(nude_number) + " el comando /nudes!"
        return nudes_text

    @staticmethod
    def get_pings(user_id):
        # WORKING
        user = BotActions.get_user(user_id)
        ping_number = user.ping_number
        ping_text = "Has usado " + str(ping_number) + " el comando /ping!"
        return ping_text

    @staticmethod
    def get_animals(user_id):
        # WORKING
        user = BotActions.get_user(user_id)
        animal_number = user.animal_number
        animal_text = "Has usado " + str(animal_number) + " el comando /animals!"
        return animal_text

    @staticmethod
    @with_db
    def get_all_messages(data, user_id):
        user = BotActions.get_user(user_id)
        total_messages = data.calcular_total_mensajes(user)
        mensaje_total = "En total has enviado " + str(total_messages) + " mensajes en todos los grupos!"
        return mensaje_total

    @staticmethod
    def send_twitter_acc(bot, update):
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        user = BotActions.get_user(user_id)
        twitter_account = user.twitter_user
        if not twitter_account:
            text = "No hay ninguna cuenta asociada actualmente :("
        else:
            text = "Ésta es la cuenta que tienes asociada actualmente: " + twitter_account
        bot.send_message(chat_id=user_id, text=text)

    @staticmethod
    def easy_command(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=chat_id, text="que es facil", reply_to_message_id=update.message.message_id)

    @staticmethod
    def insulto_method(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        name = update.message.text[10:]
        insulto = BotActions.get_random_insult("insultos.txt")
        bot.send_message(chat_id=chat_id, text=name + " eres un " + insulto)

    @staticmethod
    def get_random_insult(file_name):
        insults = BotActions.read_lines(file_name)
        lines = len(insults)
        random_pos = int(round(random.random() * lines, 0))
        return insults[random_pos][0:-1]

    @staticmethod
    def read_lines(file_name):
        list_ret = []
        opened_file = open(file_name, 'rb')
        has_next = True
        while has_next:
            line = opened_file.readline().lower().decode('utf-8')
            if not line:
                has_next = False
            else:
                list_ret.append(line)
        return list_ret

    @staticmethod
    def gracias_react(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=chat_id, text='de nada supollita', reply_to_message_id=update.message.message_id)

    @staticmethod
    def when_te_pasa(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text="si xD", reply_to_message_id=update.message.message_id)

    @staticmethod
    def current_status(bot, update, args):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text=BotActions.status_message(args))

    @staticmethod
    def status_message(args):
        """ Reprogramado por @melchor629 """
        current_uptime = subprocess.check_output(["uptime", "-p"]).decode('utf-8')[3:]
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as sys_temp:
          current_temp = float(sys_temp.read()) / 1000
        free_output = None
        memory_units = None
        if len(args) > 0 and (args[0].lower() == 'mb' or args[0].lower() == 'm'):
            free_output = subprocess.check_output(['free', '-m']).decode('utf-8').splitlines()
            memory_units = 'MB'
        elif len(args) > 0 and args[0].lower() == 'b':
            free_output = subprocess.check_output(['free', '-b']).decode('utf-8').splitlines()
            memory_units = 'B'
        else:
            free_output = subprocess.check_output(['free']).decode('utf-8').splitlines()
            memory_units = 'KB'
        free_output = dict(zip(free_output[0].split(), free_output[1].split()[1:]))
        message = "Current RPI 3 status:\nUsed Memory: {}{u} + {}{u}\nFree Memory: {}{u}\nTotal Memory: {}{" \
                  "u}\nTemperature: {}Uptime: {} "
        message = message.format(free_output['used'], free_output['buff/cache'], free_output['free'],
                                 free_output['total'], current_temp, current_uptime, u=memory_units)
        return message

    @staticmethod
    def thicc_boi(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_photo(chat_id=chat_id, photo=open(f'{BotActions.pytel_path}/192.png', 'rb'),
                       reply_to_message_id=update.message.message_id)

    @staticmethod
    def thicc_react(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=chat_id, text='thicc boi', reply_to_message_id=update.message.message_id)

    @staticmethod
    def spain(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_photo(chat_id=chat_id, photo=open(f'{BotActions.pytel_path}/spainreact.jpg', 'rb'),
                       reply_to_message_id=update.message.message_id)

    @staticmethod
    def cocaine(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_video(chat_id=chat_id, video=open(f'{BotActions.pytel_path}/cocaine.mp4', 'rb'),
                       reply_to_message_id=update.message.message_id)

    @staticmethod
    def sad(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text="sad reacts only", reply_to_message_id=update.message.message_id)

    @staticmethod
    def reverte(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        rnd = int(round(random.random() * len(BotActions.stickers), 0)) - 1
        bot.sendSticker(chat_id=chat_id, sticker=BotActions.stickers[rnd],
                        reply_to_message_id=update.message.message_id)

    @staticmethod
    def reverted(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_photo(chat_id=chat_id, photo=open(f'{BotActions.pytel_path}/reverted.png', 'rb'))

    @staticmethod
    def xd_react(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=chat_id, text="que te jodan, macho", reply_to_message_id=update.message.message_id)

    @staticmethod
    def habeces(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        if chat_id != user_id and BotActions.is_dnd_disabled(chat_id):
            BotActions.common_process(chat_id, user_id)
            bot.send_message(chat_id=chat_id, text="a veces", reply_to_message_id=update.message.message_id)

    # @staticmethod
    # def calculator(bot, update):
    #     chat_id = update.message.chat.id
    #     user_id = update.message.from_user.id
    #     BotActions.common_process(chat_id, user_id)
    # TODO calculadora;

    @staticmethod
    def facts(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        dato = BotActions.get_random_facts()
        bot.send_message(chat_id=chat_id, text=dato, reply_to_message_id=update.message.message_id)

    @staticmethod
    def barman(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='`Póngame un Dyc`', parse_mode='Markdown',
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def gustar(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='`ＳＩ　ＥＬ　ＴＲＵＣＯ　ＰＡＲＡ'
                                               '　ＧＵＳＴＡＲＬＥ　Ａ　ＡＬＧＵＩＥＮ　ＥＳ　ＰＡＳＡＲ　ＤＥ'
                                               '　ＥＳＡ　ＰＥＲＳＯＮＡ　ＣＲＥＯ　ＱＵＥ　ＴＯＤＯ　ＥＬ　ＭＵＮＤＯ'
                                               '　ＥＳＴＡ　ＥＮＡＭＯＲＡＤＯ　ＤＥ　ＭＩ`', parse_mode='Markdown',
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def vallecas(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        cad = '`ME \nVIENE \nUN \nTIO \nQUE\nSE\nQUIERE\nHACER\nUN\nTATUAJE\nY\nME ' \
              '\nPREGUNTA\nSI\nDUELE\nY\nLE\nDIGO:\nDEPENDE\nDE\nLA\nZONA\nY\nME\nDICE:\nDE\nLA\nZONA\nDE\nVALLECAS`'
        bot.send_message(chat_id=chat_id, text=cad, parse_mode='Markdown',
                         reply_to_message_id=update.message.message_id)

    @staticmethod
    def insults(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        insult = u''
        insult += BotActions.get_random_insult("insults.txt")
        bot.send_message(chat_id=chat_id, text=u'Ets un ' + insult)

    @staticmethod
    def bumper_cars(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        voice = open(f"{BotActions.pytel_path}/bumper_cars.mp3", 'rb')
        bot.send_voice(chat_id=chat_id, reply_to_message_id=update.message.message_id, voice=voice)

    @staticmethod
    def add_fact(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        list_id = BotActions.read_ids_from_file("ids.txt")
        if update.message.from_user.id in list_id:
            data_descr = update.message.text[10:]
            if len(data_descr) == 0:
                reply_text = "El texto no debe estar vacío!"
            else:
                BotActions.new_fact(data_descr)
                reply_text = "Se ha añadido correctamente el dato!"
        else:
            reply_text = "Lo siento, no se te permite usar esta característica."
        bot.send_message(chat_id=chat_id, text=reply_text)

    @staticmethod
    def print_all_facts(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        text = 'Estos son todos los datos en almacenados: \n'
        for facts in BotActions.get_all_facts():
            text += str(facts.data_id) + ': ' + facts.data_text + '\n'
        messages = []
        for i in range(0, int(ceil(len(text) / 4096))):
            messages.append(text[(i * 4096):(i + 1) * 4096])
        for message in messages:
            bot.send_message(chat_id=chat_id, text=message)

    @staticmethod
    def delete_data(bot, update, args):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        try:
            data_id = int(args[0])
            BotActions.eliminar_dato(data_id)
            text = 'Dato borrado correctamente...'
        except ValueError:
            text = 'No has insertado correctamente el id'
        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    @with_db
    def not_disturb(data: Almacenamiento, bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if chat_id != user_id:
            chat_group = data.obtener_grupo(chat_id)
            chat_group.no_disturb = True
            data.modificar_grupo(chat_group)
            text_to_send = "El bot se ha modificado para que no moleste en este grupo!"
        else:
            text_to_send = "Este comando se tiene que usar en un grupo!!"
        bot.send_message(chat_id=chat_id, reply_to_message_id=update.message.message_id,
                         text=text_to_send)

    @staticmethod
    @with_db
    def disturb(data: Almacenamiento, bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if chat_id != user_id:
            chat_group = data.obtener_grupo(chat_id)
            chat_group.no_disturb = False
            data.modificar_grupo(chat_group)
            text_to_send = "El bot se ha modificado para que moleste en este grupo!"
        else:
            text_to_send = "Este comando se tiene que usar en un grupo!!"
        bot.send_message(chat_id=chat_id, reply_to_message_id=update.message.message_id,
                         text=text_to_send)

    @staticmethod
    @with_db
    def add_chat_group(data, chat_id):
        chat_group = Group(chat_id)
        if data.obtener_grupo(chat_group.group_id) is None:
            data.insertar_grupo(chat_group)

    @staticmethod
    @with_db
    def is_dnd_disabled(data: Almacenamiento, chat_id) -> bool:
        chat_group = data.obtener_grupo(chat_id)
        return False if chat_group is None else not chat_group.no_disturb

    @staticmethod
    @with_db
    def new_fact(data: Almacenamiento, text: str):
        data.insertar_dato(UselessData(text))

    @staticmethod
    @with_db
    def eliminar_dato(data: Almacenamiento, data_id: int):
        data.eliminar_dato(data_id)

    @staticmethod
    @with_db
    def get_random_facts(data: Almacenamiento) -> str:
        return data.obtener_un_dato().data_text

    @staticmethod
    @with_db
    def get_all_facts(data: Almacenamiento) -> [UselessData]:
        return data.obtener_todos_datos()

    @staticmethod
    def unknown(bot, update):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_message(chat_id=chat_id, text='No he entendido ese comando :(')

    @staticmethod
    def last_tracks(bot, update, args):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if len(args) >= 2:
            try:
                track_number = int(args[0])
                if track_number > 0:
                    if track_number < 50:
                        text = BotActions.py_last.get_last_tracks(track_number, args[1])
                    else:
                        text = 'El numero tiene que ser menor que 50!'
                else:
                    text = 'El numero tiene que ser positivo!'
            except ValueError:
                text = 'El formato debe ser /last_tracks cantidad usuario. cantidad debe ser un numero'
        else:
            text = 'Necesito el número de canciones y el usuario!'
        bot.send_message(chat_id, text=text)

    @staticmethod
    def listening(bot, update, args):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if len(args) >= 1:
            text = BotActions.py_last.get_now_playing(args[0])
        else:
            text = 'Necesito el usuario!'
        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def total_scrobbled(bot, update, args):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if len(args) >= 1:
            text = BotActions.py_last.get_playcount(args[0])
        else:
            text = 'Necesito el usuario!'
        bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    def vosvone(bot, update):
        """Reply if you are altered"""
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        bot.send_voice(chat_id=chat_id, voice=open(f'{BotActions.pytel_path}/vosvone.opus', 'rb'))

    @staticmethod
    # trae la alegría del viernes al grupo
    def viernes(bot, update):
        current_time = update.message.date
        current_weekday = current_time.isoweekday()
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        BotActions.common_process(chat_id, user_id)
        if current_weekday is 5:
            text = "OOOOOLE LOS VIERNEEEEES!!\nhttps://www.youtube.com/watch?v=1p3-w7O4pVE"
        else:
            text = "Hoy no es viernes :("
        bot.send_message(chat_id=chat_id, text=text)