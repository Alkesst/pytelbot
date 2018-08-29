#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# made with python 3

""" Capa de persistencia para PyTel por @melchor629 y extendida por @alkesstt """

import sqlite3


class UselessData(object):
    """Update by @alkesst"""

    def __init__(self, data_text=None, data_id=None):
        super(UselessData, self).__init__()
        if isinstance(data_id, (sqlite3.Row, tuple)):
            self.__data_id = data_id[0]
            self.__data_text = data_id[1]
        else:
            self.__data_id = data_id
            self.__data_text = data_text

    @property
    def data_id(self) -> int:
        return self.__data_id

    @property
    def data_text(self) -> str:
        return self.__data_text

    @data_id.setter
    def data_id(self, data_id: int):
        self.__data_id = data_id

    @data_text.setter
    def data_text(self, text: str):
        self.__data_text = text

    def __str__(self):
        return 'UselessData(%d, %s)' % (self.__data_id, self.__data_text)


class User(object):
    """User es una clase que representa un usuario de la base de datos"""

    def __init__(self, userid=None, twitter_user=None, ping=0, nude=0, animal=0):
        super(User, self).__init__()
        if isinstance(userid, (sqlite3.Row, tuple)):
            self.__userid = userid[0]
            self.twitter_user = userid[1]
            self.__ping_number = userid[2]
            self.__nude_number = userid[3]
            self.__animal_number = userid[4]
        else:
            self.__userid = userid
            self.twitter_user = twitter_user
            self.__ping_number = ping
            self.__nude_number = nude
            self.__animal_number = animal

    @property
    def userid(self) -> int:
        return self.__userid

    @userid.setter
    def userid(self, val: int):
        self.__userid = val

    @property
    def ping_number(self) -> int:
        return self.__ping_number

    @ping_number.setter
    def ping_number(self, val: int):
        self.__ping_number = val

    @property
    def nude_number(self) -> int:
        return self.__nude_number

    @nude_number.setter
    def nude_number(self, val: int):
        self.__nude_number = val

    @property
    def animal_number(self) -> int:
        return self.__animal_number

    @animal_number.setter
    def animal_number(self, val: int):
        self.__animal_number = val

    def __str__(self):
        return 'User(%d, u"%s", %d, %d, %d)' % (
            self.userid, self.twitter_user, self.ping_number, self.nude_number, self.animal_number)


class Group(object):

        def __init__(self, group_id: int, dnd: bool=False):
            super(Group, self).__init__()
            if isinstance(group_id, (sqlite3.Row, tuple)):
                self.__group_id = group_id[0]
                self.__dnd = group_id[1]
            else:
                self.__group_id = group_id
                self.__dnd = dnd

        @property
        def no_disturb(self) -> bool:
            return self.__dnd

        @no_disturb.setter
        def no_disturb(self, dnd: bool):
            self.__dnd = dnd

        @property
        def group_id(self) -> int:
            return self.__group_id


class UserGroup(object):
    """UserGroup almacena la información de un usuario de la base de datos"""

    def __init__(self, userid, groupid, message_number=0, pole_number=0, porro=0, pi=0):
        super(UserGroup, self).__init__()
        if isinstance(userid, (sqlite3.Row, tuple)):
            self.__userid = userid[0]
            self.__groupid = userid[1]
            self.__message_number = userid[2]
            self.__pole_number = userid[3]
            self.__porro_number = userid[4]
            self.__pi_number = userid[5]
        else:
            self.__userid = userid
            self.__groupid = groupid
            self.__message_number = message_number
            self.__pole_number = pole_number
            self.__porro_number = porro
            self.__pi_number = pi

    @property
    def userid(self) -> int:
        return self.__userid

    @userid.setter
    def userid(self, val: int):
        self.__userid = val

    @property
    def groupid(self) -> int:
        return self.__groupid

    @groupid.setter
    def groupid(self, val: int):
        self.__groupid = val

    @property
    def message_number(self) -> int:
        return self.__message_number

    @message_number.setter
    def message_number(self, val: int):
        self.__message_number = val

    @property
    def pole_number(self) -> int:
        return self.__pole_number

    @pole_number.setter
    def pole_number(self, val: int):
        self.__pole_number = val

    @property
    def porro_number(self) -> int:
        return self.__porro_number

    @porro_number.setter
    def porro_number(self, val: int):
        self.__porro_number = val

    @property
    def pi_number(self) -> int:
        return self.__pi_number

    @pi_number.setter
    def pi_number(self, val: int):
        self.__pi_number = val

    def __str__(self):
        return f'UserGroup({self.userid}, {self.groupid}, {self.message_number},' \
               f' {self.pole_number}, {self.porro_number}, {self.pi_number},'


class Almacenamiento(object):
    """
    Almacenamiento es una clase que añade una capa de abstracción
    para la persistencia de datos en el bot de Telegram de Alkesst
    """

    def __init__(self, dbfile="tel.db"):
        super(Almacenamiento, self).__init__()
        self.dbfile = dbfile
        self.db = sqlite3.connect(self.dbfile)
        self.c = self.db.cursor()

        # https://stackoverflow.com/questions/5890250/on-delete-cascade-in-sqlite3
        self.c.execute('PRAGMA foreign_keys = ON')
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `user` (\n" +
            "  userid INTEGER PRIMARY KEY ASC,\n" + "  twitter_user TEXT,\n" +
            "  ping_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  nude_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  animal_number INTEGER NOT NULL DEFAULT 0\n" + ")")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `chat_group` (\n" +
            "   group_id INTEGER PRIMARY KEY," +
            "   do_not_disturb INTEGER NOT NULL DEFAULT 0" +
            ")")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `user_group` (\n" +
            "  userid INTEGER NOT NULL,\n" +
            "  groupid INTEGER NOT NULL,\n" +
            "  message_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  pole_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  porro_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  pi_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  CONSTRAINT user_group_pk PRIMARY KEY (userid ASC, groupid ASC),\n" +
            "  CONSTRAINT user_group_fk FOREIGN KEY (groupid) REFERENCES chat_group(group_id) ON DELETE CASCADE,\n" +
            "  CONSTRAINT user_id_fk FOREIGN KEY (userid) REFERENCES user(userid) ON DELETE CASCADE\n" + ")")

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `useless_data` (\n" + "  data_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,\n" +
            "  data_description VARCHAR NOT NULL" + ")")

        self.db.commit()

    def close(self):
        """Cierra la conexión con la base de datos"""
        self.db.close()

    @staticmethod
    def __checc(user):
        """__checc"""
        if not isinstance(user, User):
            raise AttributeError("El parámetro debe ser de tipo almacenamiento.User")

    @staticmethod
    def __clocc(user_group):
        """___clocc"""
        if not isinstance(user_group, UserGroup):
            raise AttributeError("El parámetro debe ser de tipo almacenamiento.UserGroup")

    def obtener_usuario(self, user):
        """Busca un usuario por id o por usuario de twitter"""
        Almacenamiento.__checc(user)
        userid = user.userid
        twitter_user = user.twitter_user
        res = None
        if userid is not None:
            self.c.execute("SELECT * FROM `user` WHERE `userid` = ?", (userid,))
            res = self.c.fetchall()
            return None if not res else User(res[0])
        elif twitter_user is not None:
            self.c.execute("SELECT * FROM `user` WHERE `twitter_user` = ?", (twitter_user,))
            return None if not res else User(res[0])
        else:
            raise AttributeError("No se ha declarado buscar por userid o por user de twitter")

    def insertar_usuario(self, user):
        """Inserta un usuario"""
        Almacenamiento.__checc(user)
        self.c.execute('INSERT INTO user VALUES (?,?,?,?,?)',
                       (user.userid, user.twitter_user, user.ping_number, user.nude_number, user.animal_number))
        self.db.commit()

    def eliminar_usuario(self, user):
        """Elimina un usuario. Solo es necesario el parámetro userid"""
        Almacenamiento.__checc(user)
        self.c.execute('DELETE FROM user WHERE userid = ?', (user.userid,))
        self.db.commit()
        return self.c.rowcount != 0

    def modificar_usuario(self, user):
        """Modifica un usuario"""
        Almacenamiento.__checc(user)
        old_user = self.obtener_usuario(user)
        if old_user.twitter_user != user.twitter_user:
            self.c.execute('UPDATE user SET twitter_user = ? WHERE userid = ?', (user.twitter_user, user.userid))
        if old_user.ping_number != user.ping_number:
            self.c.execute('UPDATE user SET ping_number = ? WHERE userid = ?', (user.ping_number, user.userid))
        if old_user.nude_number != user.nude_number:
            self.c.execute('UPDATE user SET nude_number = ? WHERE userid = ?', (user.nude_number, user.userid))
        if old_user.animal_number != user.animal_number:
            self.c.execute('UPDATE user SET animal_number = ? WHERE userid = ?', (user.animal_number, user.userid))
        self.db.commit()

    def aumentar_ping_number(self, user):
        """Aumenta el ping_number de un usuario. Obligatorio el campo userid, el resto no son
        necesarios"""
        Almacenamiento.__checc(user)
        full_u = self.obtener_usuario(user)
        full_u.ping_number += 1
        self.modificar_usuario(full_u)

    def aumentar_nude_number(self, user):
        """Aumenta el nude_number de un usuario. Obligatorio el campo userid, el resto no son
        necesarios"""
        Almacenamiento.__checc(user)
        full_u = self.obtener_usuario(user)
        full_u.nude_number += 1
        self.modificar_usuario(full_u)

    def aumentar_animal_number(self, user):
        """Aumenta el animal_number de un usuario. Obligatorio el campo userid, el resto no son
        necesarios"""
        Almacenamiento.__checc(user)
        full_u = self.obtener_usuario(user)
        full_u.animal_number += 1
        self.modificar_usuario(full_u)

    def obtener_usuario_del_grupo(self, user_group):
        """Busca un usuario del grupo por id"""
        Almacenamiento.__clocc(user_group)
        self.c.execute("SELECT * FROM `user_group` WHERE `userid` = ? AND `groupid` = ?",
                       (user_group.userid, user_group.groupid))
        res = self.c.fetchall()
        return None if not res else UserGroup(res[0], None)

    def insertar_usuario_del_grupo(self, user_group: UserGroup):
        """Inserta info de un usuario de un grupo"""
        Almacenamiento.__clocc(user_group)
        self.c.execute('INSERT INTO `user_group` VALUES (?,?,?,?,?,?)', (
            user_group.userid, user_group.groupid, user_group.message_number, user_group.pole_number,
            user_group.porro_number, user_group.pi_number))
        self.db.commit()

    def eliminar_usuario_del_grupo(self, user_group):
        """Elimina un usuario de un grupo. Solo es necesario el parámetro userid y el groupid"""
        Almacenamiento.__clocc(user_group)
        self.c.execute('DELETE FROM `user_group` WHERE userid = ? AND groupid = ?',
                       (user_group.userid, user_group.groupid))
        self.db.commit()
        return self.c.rowcount != 0

    def modificar_usuario_del_grupo(self, user_group):
        """Modifica info de un usuario de un grupo"""
        Almacenamiento.__clocc(user_group)
        old_user = self.obtener_usuario_del_grupo(user_group)
        if old_user.message_number != user_group.message_number:
            self.c.execute('UPDATE `user_group` SET message_number = ? WHERE userid = ? AND groupid = ?',
                           (user_group.message_number, user_group.userid, user_group.groupid))
        if old_user.pole_number != user_group.pole_number:
            self.c.execute('UPDATE `user_group` SET pole_number = ? WHERE userid = ? AND groupid = ?',
                           (user_group.pole_number, user_group.userid, user_group.groupid))
        if old_user.porro_number != user_group.porro_number:
            self.c.execute('UPDATE `user_group` SET porro_number = ? WHERE userid = ? AND groupid = ?',
                           (user_group.porro_number, user_group.userid, user_group.groupid))
        if old_user.pi_number != user_group.pi_number:
            self.c.execute('UPDATE `user_group` SET pi_number = ? WHERE userid = ? AND groupid = ?',
                           (user_group.pi_number, user_group.userid, user_group.groupid))
        self.db.commit()

    def aumentar_message_number(self, user_group):
        """Aumenta el message_number de un usuario en un grupo. Se requieren userid y groupid
        presentes en el objecto, el resto no"""
        Almacenamiento.__clocc(user_group)
        full_ug = self.obtener_usuario_del_grupo(user_group)
        full_ug.message_number += 1
        self.modificar_usuario_del_grupo(full_ug)

    def aumentar_pole_number(self, user_group):
        """Aumenta el pole_number de un usuario en un grupo. Se requieren userid y groupid
        presentes en el objecto, el resto no"""
        Almacenamiento.__clocc(user_group)
        full_ug = self.obtener_usuario_del_grupo(user_group)
        full_ug.pole_number += 1
        self.modificar_usuario_del_grupo(full_ug)

    def aumentar_porro_number(self, user_group):
        """Aumenta el porro_number de un usuario en un grupo. Se requieren userid y groupid
        presentes en el objecto, el resto no"""
        Almacenamiento.__clocc(user_group)
        full_ug = self.obtener_usuario_del_grupo(user_group)
        full_ug.porro_number += 1
        self.modificar_usuario_del_grupo(full_ug)

    def aumentar_pi_number(self, user_group):
        """Aumenta el pi_number de un usuario en un grupo. Se requieren userid y groupid
        presentes en el objecto, el resto no"""
        Almacenamiento.__clocc(user_group)
        full_ug = self.obtener_usuario_del_grupo(user_group)
        full_ug.pi_number += 1
        self.modificar_usuario_del_grupo(full_ug)

    def calcular_total_mensajes(self, user):
        """Calcula la cantidad de mensajes total enviados por un usuario entre todos los grupos.
        Puede devolver None si no hay mensajes almacenados para ese usuario."""
        Almacenamiento.__checc(user)
        self.c.execute("SELECT SUM(message_number) as total_messages FROM user_group WHERE userid = ?", (user.userid,))
        res = self.c.fetchall()
        return res[0][0] if res else None

    # Updated by @alkesst

    def insertar_dato(self, data: UselessData):
        self.c.execute('INSERT INTO useless_data (data_description) VALUES (?)', (data.data_text,))
        self.db.commit()

    # https://stackoverflow.com/questions/4114940/select-random-rows-in-sqlite
    def obtener_un_dato(self) -> UselessData:
        self.c.execute('SELECT * FROM useless_data WHERE data_id IN (SELECT data_id FROM useless_data ORDER BY RANDOM()'
                       ' LIMIT 1)')
        res = self.c.fetchall()
        return None if not res else UselessData(res[0][1], res[0][0])

    def obtener_todos_datos(self) -> [UselessData]:
        self.c.execute('SELECT * FROM useless_data')
        res = self.c.fetchall()
        list_res = [UselessData(data[1], data[0]) for data in res]
        return list_res

    def eliminar_dato(self, data_id: int) -> bool:
        self.c.execute('DELETE FROM useless_data WHERE data_id = ?', (data_id,))
        self.db.commit()
        return self.c.rowcount != 0

    def insertar_grupo(self, grupo: Group):
        self.c.execute('INSERT INTO chat_group VALUES (?,?)', (grupo.group_id, grupo.no_disturb))
        self.db.commit()

    def eliminar_grupo(self, grupo: Group):
        self.c.execute('DELETE FROM chat_group WHERE group_id = ?',
                       (grupo.group_id,))
        self.db.commit()
        return self.c.rowcount != 0

    def obtener_grupo(self, group_id: int) -> Group:
        self.c.execute("SELECT * FROM `chat_group` WHERE group_id = ?",
                       (group_id,))
        res = self.c.fetchall()
        return None if not res else Group(res[0])

    def modificar_grupo(self, grupo: Group):
        old_chat = self.obtener_grupo(grupo.group_id)
        if old_chat.no_disturb != grupo.no_disturb:
            self.c.execute('UPDATE `chat_group` SET do_not_disturb = ? WHERE group_id = ?',
                           (int(grupo.no_disturb), grupo.group_id))
        self.db.commit()
