#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wand.image import Image
from wand.drawing import Drawing


class SpecialActions():

    @staticmethod
    def create_image_search(image_name, text):
        """Create an image with the given string"""
        with Image(filename=image_name) as img:
            with img.clone() as cloned:
                cloned.format = 'png'
                with Drawing() as draw:
                    draw.font_family = 'italic'
                    draw.font_size = 30
                    text = SpecialActions.simplifying(text)
                    draw.text(160, 785, text)
                    draw(cloned)
                    cloned.save(filename="generated_meme_search.png")

    @staticmethod
    def simplifying(text):
        """Tokenizes the text by fragments of 15s chars"""
        str(text)
        size = len(text) / 15
        i = 0
        while i < (size - 1):
            text += text[size*0:size*1] + "\n"
            i += 1
        return text

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
