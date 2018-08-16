#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wand.image import Image
from wand.drawing import Drawing


class SpecialActions(object):

    @staticmethod
    def create_image_search(image_name, saved_image, text):
        """Create an image with the given string"""
        with Image(filename=image_name) as img:
            with img.clone() as cloned:
                cloned.format = 'png'
                with Drawing() as draw:
                    draw.font_family = 'Liberation Mono'
                    draw.font_size = 30
                    text = SpecialActions.simplifying(text)
                    draw.text(155, 785, text)
                    draw(cloned)
                    cloned.save(filename=saved_image)

    @staticmethod
    def simplifying(text):
        """Tokenizes the text by fragments of 15s chars"""
        str(text)
        max_chars = 20
        size = len(text) // max_chars
        i = 0
        fragments = []
        while i <= size:
            fragments.append(text[max_chars * i:max_chars * (i + 1)])
            i += 1
        return '\n'.join(fragments)

    @staticmethod
    def preparing_text_cabezas(text):
        aux_text = u''
        lista = []
        for items in text:
            if text == "\n":
                lista.append(aux_text)
            else:
                aux_text += items
        i = 0
        while i < len(lista):
            aux_var = lista[i]
            aux_var = SpecialActions.simplifying(aux_var)
            lista[i] = aux_var
            i += 1
        return lista

    @staticmethod
    def create_image_cabezas(image_name, text):
        pass
        # lista = SpecialActions.preparing_text_cabezas(text)
        # not finished
