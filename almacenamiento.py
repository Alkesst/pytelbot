#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Capa de persistencia para PyTel por @melchor629 """

import sqlite3

class User(object):
    """User es una clase que representa un usuario de la base de datos"""
    def __init__(self, userid=None, twitter_user=None, ping=0, nude=0, animal=0):
        super(User, self).__init__()
        if isinstance(userid, sqlite3.Row) or isinstance(userid, tuple):
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
    def userid(self):
        return self.__userid

    @userid.setter
    def userid(self, val):
        if isinstance(val, int):
            self.__userid = val
        else:
            raise AttributeError("Solo enteros")

    @property
    def ping_number(self):
        return self.__ping_number

    @ping_number.setter
    def ping_number(self, val):
        if isinstance(val, int):
            self.__ping_number = val
        else:
            raise AttributeError("Solo enteros")

    @property
    def nude_number(self):
        return self.__nude_number

    @nude_number.setter
    def nude_number(self, val):
        if isinstance(val, int):
            self.__nude_number = val
        else:
            raise AttributeError("Solo enteros")

    @property
    def animal_number(self):
        return self.__animal_number

    @animal_number.setter
    def animal_number(self, val):
        if isinstance(val, int):
            self.__animal_number = val
        else:
            raise AttributeError("Solo enteros")

    def __str__(self):
        return 'User(%d, u"%s", %d, %d, %d)' % (self.userid,
                                                self.twitter_user,
                                                self.ping_number,
                                                self.nude_number,
                                                self.animal_number)


class UserGroup(object):
    """UserGroup almacena la información de un usuario de la base de datos"""
    def __init__(self, userid, groupid, message_number=0, pole_number=0, porro=0, pi=0):
        super(UserGroup, self).__init__()
        if isinstance(userid, sqlite3.Row) or isinstance(userid, tuple):
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
    def userid(self):
        return self.__userid

    @userid.setter
    def userid(self, val):
        if isinstance(val, int):
            self.__userid = val
        else:
            raise AttributeError('Solo enteros')

    @property
    def groupid(self):
        return self.__groupid

    @groupid.setter
    def groupid(self, val):
        if isinstance(val, int):
            self.__groupid = val
        else:
            raise AttributeError('Solo enteros')

    @property
    def message_number(self):
        return self.__message_number

    @message_number.setter
    def message_number(self, val):
        if isinstance(val, int):
            self.__message_number = val
        else:
            raise AttributeError('Solo enteros')

    @property
    def pole_number(self):
        return self.__pole_number

    @pole_number.setter
    def pole_number(self, val):
        if isinstance(val, int):
            self.__pole_number = val
        else:
            raise AttributeError('Solo enteros')

    @property
    def porro_number(self):
        return self.__porro_number

    @porro_number.setter
    def porro_number(self, val):
        if isinstance(val, int):
            self.__porro_number = val
        else:
            raise AttributeError('Solo enteros')

    @property
    def pi_number(self):
        return self.__pi_number

    @pi_number.setter
    def pi_number(self, val):
        if isinstance(val, int):
            self.__pi_number = val
        else:
            raise AttributeError('Solo enteros')

    def __str__(self):
        return 'UserGroup(%d, %d, %d, %d, %d, %d)' % (self.userid,
                                                      self.groupid,
                                                      self.message_number,
                                                      self.pole_number,
                                                      self.porro_number,
                                                      self.pi_number)



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

        #https://stackoverflow.com/questions/5890250/on-delete-cascade-in-sqlite3
        self.c.execute('PRAGMA foreign_keys = ON')
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `user` (\n" +
            "  userid INTEGER PRIMARY KEY ASC,\n" +
            "  twitter_user TEXT,\n" +
            "  ping_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  nude_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  animal_number INTEGER NOT NULL DEFAULT 0\n" +
            ")"
        )

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS `user_group` (\n" +
            "  userid INTEGER NOT NULL,\n" +
            "  groupid INTEGER NOT NULL,\n" +
            "  message_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  pole_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  porro_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  pi_number INTEGER NOT NULL DEFAULT 0,\n" +
            "  CONSTRAINT user_group_pk PRIMARY KEY (userid ASC, groupid ASC),\n" +
            "  CONSTRAINT user_group_fk FOREIGN KEY (userid) REFERENCES user ON DELETE CASCADE\n" +
            ")"
        )

        self.db.commit()

    def close(self):
        """Cierra la conexión con la base de datos"""
        self.db.close()

    def __checc(self, user):
        if not isinstance(user, User):
            raise AttributeError("El parámetro debe ser de tipo almacenamiento.User")

    def __clocc(self, user_group):
        if not isinstance(user_group, UserGroup):
            raise AttributeError("El parámetro debe ser de tipo almacenamiento.UserGroup")

    def obtener_usuario(self, user):
        """Busca un usuario por id o por usuario de twitter"""
        self.__checc(user)
        userid = user.userid
        twitter_user = user.twitter_user
        if userid != None:
            self.c.execute("SELECT * FROM `user` WHERE `userid` = ?", (userid,))
            res = self.c.fetchall()
            return None if len(res) == 0 else User(res[0])
        elif twitter_user != None:
            self.c.execute("SELECT * FROM `user` WHERE `twitter_user` = ?", (twitter_user,))
            return None if len(res) == 0 else User(res[0])
        else:
            raise AttributeError("No se ha declarado buscar por userid o por user de twitter")

    def insertar_usuario(self, user):
        """Inserta un usuario"""
        self.__checc(user)
        self.c.execute('INSERT INTO user VALUES (?,?,?,?,?)', (user.userid, user.twitter_user ,
                                                               user.ping_number, user.nude_number,
                                                               user.animal_number))
        self.db.commit()

    def eliminar_usuario(self, user):
        """Elimina un usuario. Solo es necesario el parámetro userid"""
        self.__checc(user)
        self.c.execute('DELETE FROM user WHERE userid = ?', (user.userid,))
        self.db.commit()
        return self.c.rowcount != 0

    def modificar_usuario(self, user):
        """Modifica un usuario"""
        self.__checc(user)
        oldUser = self.obtener_usuario(user)
        if oldUser.twitter_user != user.twitter_user:
            self.c.execute('UPDATE user SET twitter_user = ? WHERE userid = ?', (user.twitter_user, user.userid))
        if oldUser.ping_number != user.ping_number:
            self.c.execute('UPDATE user SET ping_number = ? WHERE userid = ?', (user.ping_number, user.userid))
        if oldUser.nude_number != user.nude_number:
            self.c.execute('UPDATE user SET nude_number = ? WHERE userid = ?', (user.nude_number, user.userid))
        if oldUser.animal_number != user.animal_number:
            self.c.execute('UPDATE user SET animal_number = ? WHERE userid = ?', (user.animal_number, user.userid))
        self.db.commit()

    def aumentar_ping_number(self, user):
        """Aumenta el ping_number de un usuario. Obligatorio el campo userid, el resto no es necesario"""
        self.__checc(user)
        u = self.obtener_usuario(user)
        u.ping_number += 1
        self.modificar_usuario(u)

    def aumentar_nude_number(self, user):
        """Aumenta el nude_number de un usuario. Obligatorio el campo userid, el resto no es necesario"""
        self.__checc(user)
        u = self.obtener_usuario(user)
        u.nude_number += 1
        self.modificar_usuario(u)

    def aumentar_animal_number(self, user):
        """Aumenta el animal_number de un usuario. Obligatorio el campo userid, el resto no es necesario"""
        self.__checc(user)
        u = self.obtener_usuario(user)
        u.animal_number += 1
        self.modificar_usuario(u)


    def obtener_usuario_del_grupo(self, user_group):
        """Busca un usuario del grupo por id"""
        self.__clocc(user_group)
        self.c.execute("SELECT * FROM `user_group` WHERE `userid` = ? AND `groupid` = ?", (user_group.userid, user_group.groupid))
        res = self.c.fetchall()
        return None if len(res) == 0 else UserGroup(res[0], None)

    def insertar_usuario_del_grupo(self, user_group):
        """Inserta info de un usuario de un grupo"""
        self.__clocc(user_group)
        self.c.execute('INSERT INTO `user_group` VALUES (?,?,?,?,?,?)', (user_group.userid,
                                                                         user_group.groupid, user_group.message_number,
                                                                         user_group.pole_number, user_group.porro_number,
                                                                         user_group.pi_number))
        self.db.commit()

    def eliminar_usuario_del_grupo(self, user_group):
        """Elimina un usuario de un grupo. Solo es necesario el parámetro userid y el groupid"""
        self.__clocc(user_group)
        self.c.execute('DELETE FROM `user_group` WHERE userid = ? AND groupid = ?', (user_group.userid, user_group.groupid))
        self.db.commit()
        return self.c.rowcount != 0

    def modificar_usuario_del_grupo(self, user_group):
        """Modifica info de un usuario de un grupo"""
        self.__clocc(user_group)
        oldUser = self.obtener_usuario_del_grupo(user_group)
        if oldUser.message_number != user_group.message_number:
            self.c.execute('UPDATE `user_group` SET message_number = ? WHERE userid = ? AND groupid = ?', (user_group.message_number, user_group.userid, user_group.groupid))
        if oldUser.pole_number != user_group.pole_number:
            self.c.execute('UPDATE `user_group` SET pole_number = ? WHERE userid = ? AND groupid = ?', (user_group.pole_number, user_group.userid, user_group.groupid))
        if oldUser.porro_number != user_group.porro_number:
            self.c.execute('UPDATE `user_group` SET porro_number = ? WHERE userid = ? AND groupid = ?', (user_group.porro_number, user_group.userid, user_group.groupid))
        if oldUser.pi_number != user_group.pi_number:
            self.c.execute('UPDATE `user_group` SET pi_number = ? WHERE userid = ? AND groupid = ?', (user_group.pi_number, user_group.userid, user_group.groupid))
        self.db.commit()

    def aumentar_message_number(self, user_group):
        """Aumentar el message_number de un usuario en un grupo. Se requiere userid y groupid, el resto no"""
        self.__clocc(user_group)
        ug = self.obtener_usuario_del_grupo(user_group)
        ug.message_number += 1
        self.modificar_usuario_del_grupo(ug)

    def aumentar_pole_number(self, user_group):
        """Aumentar el pole_number de un usuario en un grupo. Se requiere userid y groupid, el resto no"""
        self.__clocc(user_group)
        ug = self.obtener_usuario_del_grupo(user_group)
        ug.pole_number += 1
        self.modificar_usuario_del_grupo(ug)

    def aumentar_porro_number(self, user_group):
        """Aumentar el porro_number de un usuario en un grupo. Se requiere userid y groupid, el resto no"""
        self.__clocc(user_group)
        ug = self.obtener_usuario_del_grupo(user_group)
        ug.porro_number += 1
        self.modificar_usuario_del_grupo(ug)

    def aumentar_pi_number(self, user_group):
        """Aumentar el pi_number de un usuario en un grupo. Se requiere userid y groupid, el resto no"""
        self.__clocc(user_group)
        ug = self.obtener_usuario_del_grupo(user_group)
        ug.pi_number += 1
        self.modificar_usuario_del_grupo(ug)
